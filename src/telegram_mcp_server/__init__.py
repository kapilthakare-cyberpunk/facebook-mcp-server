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

if sys.platform == "win32" and os.environ.get("PYTHONIOENCODING") is None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("telegram_mcp_server")


def load_telegram_config() -> tuple[str, str]:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    missing = [
        name
        for name, value in {
            "TELEGRAM_BOT_TOKEN": token,
            "TELEGRAM_CHAT_ID": chat_id,
        }.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            "Set them in a .env file or your shell before starting the server."
        )

    return token, chat_id


class TelegramManager:
    """Enhanced Telegram manager with media groups, carousel posts, and link previews."""
    
    def __init__(self, bot_token: str, chat_id: str) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def _format_text_with_hashtags(self, text: str, hashtags: Optional[list[str]] = None) -> str:
        """Format text with hashtags appended."""
        if not hashtags:
            return text
        
        hashtag_str = " ".join(f"#{tag.lstrip('#')}" for tag in hashtags)
        return f"{text}\n\n{hashtag_str}"

    def send_message(self, text: str, hashtags: Optional[list[str]] = None, disable_preview: bool = False) -> dict[str, Any]:
        """Send a text message with optional hashtags and link preview control."""
        formatted_text = self._format_text_with_hashtags(text, hashtags)
        
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id, 
            "text": formatted_text,
            "disable_web_page_preview": disable_preview
        }
        response = requests.post(url, json=payload)
        return response.json()

    def send_photo(self, photo_url: str, caption: str | None = None, hashtags: Optional[list[str]] = None) -> dict[str, Any]:
        """Send a single photo with optional caption and hashtags."""
        if caption:
            formatted_caption = self._format_text_with_hashtags(caption, hashtags)
        else:
            formatted_caption = self._format_text_with_hashtags("", hashtags) if hashtags else None
        
        url = f"{self.base_url}/sendPhoto"
        payload = {"chat_id": self.chat_id, "photo": photo_url}
        if formatted_caption:
            payload["caption"] = formatted_caption
        response = requests.post(url, json=payload)
        return response.json()

    def send_media_group(self, media_urls: list[str], caption: str | None = None, hashtags: Optional[list[str]] = None) -> dict[str, Any]:
        """Send multiple photos as a carousel/album (media group) with optional caption and hashtags."""
        if not media_urls or len(media_urls) < 2:
            return {"error": "Media group requires at least 2 images"}
        
        if len(media_urls) > 10:
            return {"error": "Telegram supports max 10 media items per group"}
        
        # Format caption with hashtags
        formatted_caption = None
        if caption or hashtags:
            formatted_caption = self._format_text_with_hashtags(caption or "", hashtags)
        
        # Build media array - only first item gets caption
        media = []
        for idx, url in enumerate(media_urls):
            media_item = {
                "type": "photo",
                "media": url
            }
            # Add caption only to first item
            if idx == 0 and formatted_caption:
                media_item["caption"] = formatted_caption
            media.append(media_item)
        
        url = f"{self.base_url}/sendMediaGroup"
        payload = {
            "chat_id": self.chat_id,
            "media": media
        }
        response = requests.post(url, json=payload)
        return response.json()

    def send_link_with_preview(self, text: str, link_url: str, hashtags: Optional[list[str]] = None) -> dict[str, Any]:
        """Send a message with link preview enabled and optional hashtags."""
        formatted_text = f"{text}\n\n{link_url}"
        if hashtags:
            formatted_text = self._format_text_with_hashtags(formatted_text, hashtags)
        
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": formatted_text,
            "disable_web_page_preview": False  # Enable preview
        }
        response = requests.post(url, json=payload)
        return response.json()

    def get_updates(self, limit: int = 20) -> dict[str, Any]:
        """Fetch recent updates for the bot."""
        url = f"{self.base_url}/getUpdates"
        params = {"limit": limit}
        response = requests.get(url, params=params)
        return response.json()


async def main():
    logger.info("Starting Telegram MCP Server")
    try:
        token, chat_id = load_telegram_config()
    except RuntimeError as exc:
        logger.error(str(exc))
        raise

    manager = TelegramManager(bot_token=token, chat_id=chat_id)
    server = Server("telegram-manager")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="telegram_send_message",
                description="Send a text message with optional hashtags and link preview control",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Message text"},
                        "hashtags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional hashtags"
                        },
                        "disable_preview": {
                            "type": "boolean",
                            "description": "Disable link preview (default: false)"
                        }
                    },
                    "required": ["text"],
                },
            ),
            types.Tool(
                name="telegram_send_photo",
                description="Send a single photo with optional caption and hashtags",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "photo_url": {"type": "string", "description": "URL of the photo"},
                        "caption": {"type": "string", "description": "Optional caption"},
                        "hashtags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional hashtags"
                        }
                    },
                    "required": ["photo_url"],
                },
            ),
            types.Tool(
                name="telegram_send_media_group",
                description="Send multiple photos as carousel/album (2-10 images) with optional caption and hashtags",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "media_urls": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of image URLs (2-10 images)"
                        },
                        "caption": {"type": "string", "description": "Optional caption for the media group"},
                        "hashtags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional hashtags"
                        }
                    },
                    "required": ["media_urls"],
                },
            ),
            types.Tool(
                name="telegram_send_link",
                description="Send a link with preview enabled and optional hashtags",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Message text to accompany the link"},
                        "link_url": {"type": "string", "description": "URL to share"},
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
                name="telegram_get_updates",
                description="Fetch recent updates for the bot",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Number of updates to fetch (default 20)",
                        },
                    },
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        try:
            if name == "telegram_send_message":
                hashtags = arguments.get("hashtags") if arguments else None
                disable_preview = arguments.get("disable_preview", False) if arguments else False
                result = manager.send_message(arguments["text"], hashtags, disable_preview)
            elif name == "telegram_send_photo":
                caption = arguments.get("caption") if arguments else None
                hashtags = arguments.get("hashtags") if arguments else None
                result = manager.send_photo(arguments["photo_url"], caption, hashtags)
            elif name == "telegram_send_media_group":
                caption = arguments.get("caption") if arguments else None
                hashtags = arguments.get("hashtags") if arguments else None
                result = manager.send_media_group(arguments["media_urls"], caption, hashtags)
            elif name == "telegram_send_link":
                hashtags = arguments.get("hashtags") if arguments else None
                result = manager.send_link_with_preview(arguments["text"], arguments["link_url"], hashtags)
            elif name == "telegram_get_updates":
                limit = arguments.get("limit", 20) if arguments else 20
                result = manager.get_updates(limit=limit)
            else:
                raise ValueError(f"Unknown tool: {name}")
            return [types.TextContent(type="text", text=str(result))]
        except Exception as exc:
            logger.exception("Tool execution failed")
            return [types.TextContent(type="text", text=f"Error: {exc}")]

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Telegram MCP Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="telegram",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def run():
    """Entry point for the Telegram MCP server."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
