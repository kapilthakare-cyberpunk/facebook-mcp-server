import asyncio
import logging
import os
import sys
import time
from typing import Any, Optional

import mcp.server.stdio
import requests
from dotenv import load_dotenv
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
import mcp.types as types


# Load environment variables from .env file
load_dotenv()

# Reconfigure UnicodeEncodeError prone default (i.e. windows-1252) to utf-8
if sys.platform == "win32" and os.environ.get('PYTHONIOENCODING') is None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Configure basic logging for easier debugging inside MCP clients
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger('facebook_mcp_server')
logger.info("Starting Facebook MCP Server")

# Facebook Graph API endpoint
GRAPH_API_VERSION = "v18.0"
GRAPH_API_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


def load_facebook_config() -> tuple[str, str, Optional[str]]:
    """Ensure required Facebook credentials are present."""
    page_access_token = os.environ.get("FACEBOOK_PAGE_ACCESS_TOKEN")
    page_id = os.environ.get("FACEBOOK_PAGE_ID")
    instagram_account_id = os.environ.get("INSTAGRAM_ACCOUNT_ID")

    missing = [name for name, value in {
        "FACEBOOK_PAGE_ACCESS_TOKEN": page_access_token,
        "FACEBOOK_PAGE_ID": page_id,
    }.items() if not value]

    if missing:
        raise RuntimeError(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            "Set them in a .env file or your shell before starting the server."
        )

    return page_id, page_access_token, instagram_account_id


class FacebookManager:
    def __init__(self, page_id: str, access_token: str, instagram_account_id: Optional[str] = None) -> None:
        self.page_id = page_id
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id

    def post_to_facebook(self, message: str) -> dict[str, Any]:
        """Posts a simple text message to the Facebook Page."""
        url = f"{GRAPH_API_BASE_URL}/{self.page_id}/feed"
        params = {
            "message": message,
            "access_token": self.access_token,
        }
        response = requests.post(url, params=params)
        return response.json()

    def reply_to_comment(self, post_id: str, comment_id: str, message: str) -> dict[str, Any]:
        """Replies to a comment on a specific post."""
        url = f"{GRAPH_API_BASE_URL}/{comment_id}/comments"
        params = {
            "message": message,
            "access_token": self.access_token,
        }
        response = requests.post(url, params=params)
        return response.json()

    def get_page_posts(self) -> dict[str, Any]:
        """Retrieves posts published on the Facebook Page."""
        url = f"{GRAPH_API_BASE_URL}/{self.page_id}/posts"
        params = {
            "access_token": self.access_token,
            "fields": "id,message,created_time",
        }
        response = requests.get(url, params=params)
        return response.json()

    def get_post_comments(self, post_id: str) -> dict[str, Any]:
        """Retrieves comments for a specific post."""
        url = f"{GRAPH_API_BASE_URL}/{post_id}/comments"
        params = {
            "access_token": self.access_token,
            "fields": "id,message,from,created_time",
        }
        response = requests.get(url, params=params)
        return response.json()

    def filter_negative_comments(self, comments: dict[str, Any]) -> list[dict[str, Any]]:
        """Filters negative comments based on a simple keyword list."""
        negative_keywords = ["bad", "terrible", "awful", "hate", "dislike", "problem", "issue"]
        negative_comments = []
        if 'data' in comments:
            for comment in comments['data']:
                if 'message' in comment:
                    for keyword in negative_keywords:
                        if keyword in comment['message'].lower():
                            negative_comments.append(comment)
                            break
        return negative_comments
    
    def delete_post(self, post_id: str) -> dict[str, Any]:
        """Deletes a post from the Facebook Page."""
        url = f"{GRAPH_API_BASE_URL}/{post_id}"
        params = {
            "access_token": self.access_token,
        }
        response = requests.delete(url, params=params)
        return response.json()

    def delete_comment(self, comment_id: str) -> dict[str, Any]:
        """Deletes a comment from a post."""
        url = f"{GRAPH_API_BASE_URL}/{comment_id}"
        params = {
            "access_token": self.access_token,
        }
        response = requests.delete(url, params=params)
        return response.json()

    # --- Advanced Posting Methods ---

    def post_media(self, caption: str, media_urls: list[str], media_type: str, platforms: list[str]) -> dict[str, Any]:
        """
        Posts media to Facebook and/or Instagram.
        
        :param caption: Text caption for the post.
        :param media_urls: List of URLs for the media (images or video).
        :param media_type: 'image', 'video', 'reel', or 'carousel'.
        :param platforms: List containing 'facebook' and/or 'instagram'.
        """
        results = {}
        
        if "facebook" in platforms:
            try:
                results["facebook"] = self._post_to_facebook_complex(caption, media_urls, media_type)
            except Exception as e:
                results["facebook"] = {"error": str(e)}
        
        if "instagram" in platforms:
            if not self.instagram_account_id:
                results["instagram"] = {"error": "INSTAGRAM_ACCOUNT_ID not configured."}
            else:
                try:
                    results["instagram"] = self._post_to_instagram(caption, media_urls, media_type)
                except Exception as e:
                    results["instagram"] = {"error": str(e)}
        
        return results

    def _post_to_facebook_complex(self, caption: str, media_urls: list[str], media_type: str) -> dict[str, Any]:
        if not media_urls:
            return self.post_to_facebook(caption)

        if media_type == "image":
            if len(media_urls) == 1:
                # Single Photo
                url = f"{GRAPH_API_BASE_URL}/{self.page_id}/photos"
                params = {
                    "url": media_urls[0],
                    "caption": caption,
                    "access_token": self.access_token
                }
                return requests.post(url, params=params).json()
            else:
                # Multi-Photo (Album/Carousel style)
                # 1. Upload photos without publishing
                attached_media = []
                for media_url in media_urls:
                    photo_id = self._upload_fb_photo(media_url, published=False)
                    if photo_id:
                        attached_media.append({"media_fbid": photo_id})
                
                # 2. Publish to feed
                url = f"{GRAPH_API_BASE_URL}/{self.page_id}/feed"
                params = {
                    "message": caption,
                    "attached_media": attached_media,
                    "access_token": self.access_token
                }
                return requests.post(url, json=params).json()

        elif media_type in ["video", "reel"]:
            # For now, treat reel as video for FB (FB Reels API is slightly different but video usually works)
            url = f"{GRAPH_API_BASE_URL}/{self.page_id}/videos"
            params = {
                "file_url": media_urls[0],
                "description": caption,
                "access_token": self.access_token
            }
            return requests.post(url, params=params).json()

        elif media_type == "carousel":
             # Same as multi-image for Facebook
             return self._post_to_facebook_complex(caption, media_urls, "image")
        
        else:
            raise ValueError(f"Unsupported media_type for Facebook: {media_type}")

    def _upload_fb_photo(self, url: str, published: bool = False) -> Optional[str]:
        endpoint = f"{GRAPH_API_BASE_URL}/{self.page_id}/photos"
        params = {
            "url": url,
            "published": published,
            "access_token": self.access_token
        }
        resp = requests.post(endpoint, params=params).json()
        return resp.get("id")

    def _post_to_instagram(self, caption: str, media_urls: list[str], media_type: str) -> dict[str, Any]:
        # Instagram Content Publishing API involves:
        # 1. Create Media Container(s)
        # 2. Publish Container
        
        container_id = None

        if media_type == "image" and len(media_urls) == 1:
            # Single Image
            container_id = self._create_ig_container(image_url=media_urls[0], caption=caption)
            
        elif media_type in ["video", "reel"]:
            # Single Video/Reel
            container_id = self._create_ig_container(video_url=media_urls[0], caption=caption, is_video=True, is_reel=(media_type == "reel"))

        elif media_type == "carousel" or (media_type == "image" and len(media_urls) > 1):
            # Carousel
            child_ids = []
            for url in media_urls:
                # Create item container (no caption for children)
                child_id = self._create_ig_container(image_url=url, is_carousel_item=True)
                if child_id:
                    child_ids.append(child_id)
            
            if child_ids:
                container_id = self._create_ig_carousel_container(child_ids, caption)
        
        else:
             raise ValueError(f"Unsupported media_type for Instagram: {media_type}")

        if container_id:
            return self._publish_ig_media(container_id)
        else:
            raise RuntimeError("Failed to create Instagram media container.")

    def _create_ig_container(self, image_url: str = None, video_url: str = None, caption: str = None, 
                             is_video: bool = False, is_reel: bool = False, is_carousel_item: bool = False) -> Optional[str]:
        url = f"{GRAPH_API_BASE_URL}/{self.instagram_account_id}/media"
        params = {
            "access_token": self.access_token
        }
        if is_video:
            params["media_type"] = "REELS" if is_reel else "VIDEO"
            params["video_url"] = video_url
        else:
            params["image_url"] = image_url
        
        if caption and not is_carousel_item:
            params["caption"] = caption
            
        if is_carousel_item:
            params["is_carousel_item"] = True

        resp = requests.post(url, params=params).json()
        if "id" not in resp:
            logger.error(f"IG Container Error: {resp}")
        return resp.get("id")

    def _create_ig_carousel_container(self, children_ids: list[str], caption: str) -> Optional[str]:
        url = f"{GRAPH_API_BASE_URL}/{self.instagram_account_id}/media"
        params = {
            "media_type": "CAROUSEL",
            "children": ",".join(children_ids),
            "caption": caption,
            "access_token": self.access_token
        }
        resp = requests.post(url, params=params).json()
        return resp.get("id")

    def _publish_ig_media(self, creation_id: str) -> dict[str, Any]:
        url = f"{GRAPH_API_BASE_URL}/{self.instagram_account_id}/media_publish"
        params = {
            "creation_id": creation_id,
            "access_token": self.access_token
        }
        # Publishing might take a moment if processing, usually handled by retries, but we'll do a simple call.
        return requests.post(url, params=params).json()


async def main():
    logger.info("Starting Facebook MCP Server")

    try:
        page_id, page_access_token, instagram_account_id = load_facebook_config()
    except RuntimeError as exc:
        logger.error(str(exc))
        raise

    fb_manager = FacebookManager(page_id=page_id, access_token=page_access_token, instagram_account_id=instagram_account_id)
    server = Server("facebook-manager")

    # Register handlers
    logger.debug("Registering handlers")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        return [
            types.Tool(
                name="post_to_facebook",
                description="Posts a message to the Facebook Page (Legacy - use post_media for advanced features)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "description": "Message to post"},
                    },
                    "required": ["message"],
                },
            ),
             types.Tool(
                name="post_media",
                description="Posts media (images, videos, reels, carousels) to Facebook and/or Instagram.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "caption": {"type": "string", "description": "Caption/Message for the post."},
                        "media_urls": {
                            "type": "array", 
                            "items": {"type": "string"},
                            "description": "List of public URLs for the media files."
                        },
                        "media_type": {
                            "type": "string", 
                            "enum": ["image", "video", "reel", "carousel"],
                            "description": "Type of media to post."
                        },
                        "platforms": {
                            "type": "array",
                            "items": {"type": "string", "enum": ["facebook", "instagram"]},
                            "description": "Platforms to post to."
                        }
                    },
                    "required": ["caption", "media_urls", "media_type", "platforms"],
                },
            ),
            types.Tool(
                name="reply_to_comment",
                description="Replies to a comment on a specific post",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "post_id": {"type": "string", "description": "ID of the post"},
                        "comment_id": {"type": "string", "description": "ID of the comment"},
                        "message": {"type": "string", "description": "Reply message"},
                    },
                    "required": ["post_id", "comment_id", "message"],
                },
            ),
            types.Tool(
                name="get_page_posts",
                description="Retrieves posts published on the Facebook Page",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="get_post_comments",
                description="Retrieves comments for a specific post",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "post_id": {"type": "string", "description": "ID of the post"},
                    },
                    "required": ["post_id"],
                },
            ),
            types.Tool(
                name="filter_negative_comments",
                description="Filters negative comments from a post",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "post_id": {"type": "string", "description": "ID of the post"},
                    },
                    "required": ["post_id"],
                },
            ),
            types.Tool(
                name="delete_post",
                description="Deletes a post from the Facebook Page.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "post_id": {"type": "string", "description": "ID of the post to delete."},
                    },
                    "required": ["post_id"],
                },
            ),
            types.Tool(
                name="delete_comment",
                description="Deletes a comment from a post.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string", "description": "ID of the comment to delete."},
                    },
                    "required": ["comment_id"],
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            if name == "post_to_facebook":
                result = fb_manager.post_to_facebook(arguments["message"])
                return [types.TextContent(type="text", text=str(result))]
            elif name == "post_media":
                result = fb_manager.post_media(
                    caption=arguments["caption"],
                    media_urls=arguments["media_urls"],
                    media_type=arguments["media_type"],
                    platforms=arguments["platforms"]
                )
                return [types.TextContent(type="text", text=str(result))]
            elif name == "reply_to_comment":
                result = fb_manager.reply_to_comment(arguments["post_id"], arguments["comment_id"], arguments["message"])
                return [types.TextContent(type="text", text=str(result))]
            elif name == "get_page_posts":
                result = fb_manager.get_page_posts()
                return [types.TextContent(type="text", text=str(result))]
            elif name == "get_post_comments":
                result = fb_manager.get_post_comments(arguments["post_id"])
                return [types.TextContent(type="text", text=str(result))]
            elif name == "filter_negative_comments":
                comments = fb_manager.get_post_comments(arguments["post_id"])
                result = fb_manager.filter_negative_comments(comments)
                return [types.TextContent(type="text", text=str(result))]
            elif name == "delete_post":
                result = fb_manager.delete_post(arguments["post_id"])
                return [types.TextContent(type="text", text=str(result))]
            elif name == "delete_comment":
                result = fb_manager.delete_comment(arguments["comment_id"])
                return [types.TextContent(type="text", text=str(result))]
            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="facebook",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
