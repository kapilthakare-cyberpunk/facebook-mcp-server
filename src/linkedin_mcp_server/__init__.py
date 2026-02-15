import asyncio
import logging
import os
import sys
from typing import Any, Optional

import mcp.server.stdio
import requests
from dotenv import load_dotenv
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.types as types


# Load environment variables from .env file if present
load_dotenv()

# Reconfigure UnicodeEncodeError prone default (i.e. windows-1252) to utf-8
if sys.platform == "win32" and os.environ.get("PYTHONIOENCODING") is None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("linkedin_mcp_server")

API_BASE_URL = "https://api.linkedin.com/v2"


def load_linkedin_config() -> tuple[str, str]:
    """Ensure required LinkedIn credentials are present."""
    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    org_id = os.environ.get("LINKEDIN_ORGANIZATION_ID")

    missing = [
        name
        for name, value in {
            "LINKEDIN_ACCESS_TOKEN": access_token,
            "LINKEDIN_ORGANIZATION_ID": org_id,
        }.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            "Set them in a .env file or your shell before starting the server."
        )

    return access_token, org_id


class LinkedInManager:
    """Enhanced LinkedIn manager with image, carousel, article, and hashtag support."""

    def __init__(self, access_token: str, organization_id: str) -> None:
        self.access_token = access_token
        self.organization_urn = f"urn:li:organization:{organization_id}"

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

    def _format_text_with_hashtags(self, text: str, hashtags: Optional[list[str]] = None) -> str:
        """Format text with hashtags appended."""
        if not hashtags:
            return text
        
        hashtag_str = " ".join(f"#{tag.lstrip('#')}" for tag in hashtags)
        return f"{text}\n\n{hashtag_str}"

    def create_text_post(self, text: str, hashtags: Optional[list[str]] = None) -> dict[str, Any]:
        """Create a simple text post with optional hashtags."""
        formatted_text = self._format_text_with_hashtags(text, hashtags)
        
        url = f"{API_BASE_URL}/ugcPosts"
        payload = {
            "author": self.organization_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": formatted_text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }
        response = requests.post(url, json=payload, headers=self._headers)
        return response.json()

    def create_image_post(self, text: str, image_url: str, hashtags: Optional[list[str]] = None) -> dict[str, Any]:
        """Create a single image post with optional hashtags."""
        formatted_text = self._format_text_with_hashtags(text, hashtags)
        
        # Step 1: Register the upload
        register_url = f"{API_BASE_URL}/assets?action=registerUpload"
        register_payload = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": self.organization_urn,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }
        register_response = requests.post(register_url, json=register_payload, headers=self._headers)
        register_data = register_response.json()
        
        if "value" not in register_data:
            return {"error": "Failed to register upload", "details": register_data}
        
        asset_id = register_data["value"]["asset"]
        upload_url = register_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        
        # Step 2: Upload the image
        image_data = requests.get(image_url).content
        upload_headers = {"Authorization": f"Bearer {self.access_token}"}
        requests.put(upload_url, data=image_data, headers=upload_headers)
        
        # Step 3: Create the post
        post_url = f"{API_BASE_URL}/ugcPosts"
        post_payload = {
            "author": self.organization_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": formatted_text},
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "media": asset_id
                        }
                    ]
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        response = requests.post(post_url, json=post_payload, headers=self._headers)
        return response.json()

    def create_carousel_post(self, text: str, image_urls: list[str], hashtags: Optional[list[str]] = None) -> dict[str, Any]:
        """Create a carousel post with multiple images and optional hashtags."""
        formatted_text = self._format_text_with_hashtags(text, hashtags)
        
        media_list = []
        
        for image_url in image_urls:
            # Register upload for each image
            register_url = f"{API_BASE_URL}/assets?action=registerUpload"
            register_payload = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": self.organization_urn,
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }
            register_response = requests.post(register_url, json=register_payload, headers=self._headers)
            register_data = register_response.json()
            
            if "value" not in register_data:
                continue
            
            asset_id = register_data["value"]["asset"]
            upload_url = register_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
            
            # Upload image
            image_data = requests.get(image_url).content
            upload_headers = {"Authorization": f"Bearer {self.access_token}"}
            requests.put(upload_url, data=image_data, headers=upload_headers)
            
            media_list.append({
                "status": "READY",
                "media": asset_id
            })
        
        # Create carousel post
        post_url = f"{API_BASE_URL}/ugcPosts"
        post_payload = {
            "author": self.organization_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": formatted_text},
                    "shareMediaCategory": "IMAGE",
                    "media": media_list
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        response = requests.post(post_url, json=post_payload, headers=self._headers)
        return response.json()

    def create_link_post(self, text: str, link_url: str, hashtags: Optional[list[str]] = None) -> dict[str, Any]:
        """Create an article/link sharing post with optional hashtags."""
        formatted_text = self._format_text_with_hashtags(text, hashtags)
        
        url = f"{API_BASE_URL}/ugcPosts"
        payload = {
            "author": self.organization_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": formatted_text},
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "originalUrl": link_url
                        }
                    ]
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        response = requests.post(url, json=payload, headers=self._headers)
        return response.json()

    def list_recent_posts(self, count: int = 5) -> dict[str, Any]:
        """Fetch recent posts for the organization."""
        url = f"{API_BASE_URL}/ugcPosts"
        params = {
            "q": "authors",
            "authors": f"List({self.organization_urn})",
            "sortBy": "LAST_MODIFIED",
            "count": count,
        }
        response = requests.get(url, headers=self._headers, params=params)
        return response.json()

    def comment_on_post(self, post_urn: str, message: str) -> dict[str, Any]:
        """Add a comment to a post."""
        url = f"{API_BASE_URL}/socialActions/{post_urn}/comments"
        payload = {
            "actor": self.organization_urn,
            "message": {"text": message},
        }
        response = requests.post(url, json=payload, headers=self._headers)
        return response.json()

    def get_comments(self, post_urn: str) -> dict[str, Any]:
        """Fetch comments on a post."""
        url = f"{API_BASE_URL}/socialActions/{post_urn}/comments"
        response = requests.get(url, headers=self._headers)
        return response.json()

    def delete_post(self, post_urn: str) -> dict[str, Any]:
        """Delete a post."""
        url = f"{API_BASE_URL}/ugcPosts/{post_urn}"
        response = requests.delete(url, headers=self._headers)
        if response.text:
            return response.json()
        return {"status": response.status_code}


async def main():
    logger.info("Starting LinkedIn MCP Server")

    try:
        access_token, org_id = load_linkedin_config()
    except RuntimeError as exc:
        logger.error(str(exc))
        raise

    manager = LinkedInManager(access_token=access_token, organization_id=org_id)
    server = Server("linkedin-manager")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="linkedin_create_text_post",
                description="Create a LinkedIn text post with optional hashtags",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Post text"},
                        "hashtags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional hashtags (without # symbol)"
                        }
                    },
                    "required": ["text"],
                },
            ),
            types.Tool(
                name="linkedin_create_image_post",
                description="Create a LinkedIn post with a single image and optional hashtags",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Post caption"},
                        "image_url": {"type": "string", "description": "Public URL of the image"},
                        "hashtags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional hashtags"
                        }
                    },
                    "required": ["text", "image_url"],
                },
            ),
            types.Tool(
                name="linkedin_create_carousel_post",
                description="Create a LinkedIn carousel post with multiple images and optional hashtags",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Post caption"},
                        "image_urls": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of public image URLs (2-10 images)"
                        },
                        "hashtags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional hashtags"
                        }
                    },
                    "required": ["text", "image_urls"],
                },
            ),
            types.Tool(
                name="linkedin_create_link_post",
                description="Share an article or link on LinkedIn with optional hashtags",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Post text/commentary"},
                        "link_url": {"type": "string", "description": "URL of the article/link to share"},
                        "hashtags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional hashtags"
                        }
                    },
                    "required": ["text", "link_url"],
                },
            ),
            types.Tool(
                name="linkedin_list_posts",
                description="List recent LinkedIn posts",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "count": {
                            "type": "integer",
                            "description": "Number of posts to fetch (default 5)",
                        },
                    },
                },
            ),
            types.Tool(
                name="linkedin_comment_on_post",
                description="Comment on a LinkedIn post",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "post_urn": {
                            "type": "string",
                            "description": "URN of the LinkedIn post",
                        },
                        "message": {"type": "string", "description": "Comment text"},
                    },
                    "required": ["post_urn", "message"],
                },
            ),
            types.Tool(
                name="linkedin_get_comments",
                description="Get comments for a LinkedIn post",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "post_urn": {
                            "type": "string",
                            "description": "URN of the LinkedIn post",
                        },
                    },
                    "required": ["post_urn"],
                },
            ),
            types.Tool(
                name="linkedin_delete_post",
                description="Delete a LinkedIn post",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "post_urn": {
                            "type": "string",
                            "description": "URN of the LinkedIn post",
                        },
                    },
                    "required": ["post_urn"],
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        try:
            if name == "linkedin_create_text_post":
                hashtags = arguments.get("hashtags") if arguments else None
                result = manager.create_text_post(arguments["text"], hashtags)
            elif name == "linkedin_create_image_post":
                hashtags = arguments.get("hashtags") if arguments else None
                result = manager.create_image_post(arguments["text"], arguments["image_url"], hashtags)
            elif name == "linkedin_create_carousel_post":
                hashtags = arguments.get("hashtags") if arguments else None
                result = manager.create_carousel_post(arguments["text"], arguments["image_urls"], hashtags)
            elif name == "linkedin_create_link_post":
                hashtags = arguments.get("hashtags") if arguments else None
                result = manager.create_link_post(arguments["text"], arguments["link_url"], hashtags)
            elif name == "linkedin_list_posts":
                count = arguments.get("count", 5) if arguments else 5
                result = manager.list_recent_posts(count=count)
            elif name == "linkedin_comment_on_post":
                result = manager.comment_on_post(arguments["post_urn"], arguments["message"])
            elif name == "linkedin_get_comments":
                result = manager.get_comments(arguments["post_urn"])
            elif name == "linkedin_delete_post":
                result = manager.delete_post(arguments["post_urn"])
            else:
                raise ValueError(f"Unknown tool: {name}")
            return [types.TextContent(type="text", text=str(result))]
        except Exception as exc:
            logger.exception("Tool execution failed")
            return [types.TextContent(type="text", text=f"Error: {exc}")]

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("LinkedIn MCP Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="linkedin",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def run():
    """Entry point for the LinkedIn MCP server."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
