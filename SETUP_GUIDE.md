# Social Media MCP Servers - Complete Setup Guide

## Overview
Three production-ready MCP servers for cross-platform social media posting:
- **Facebook/Instagram**: Images, carousels, videos, reels, text posts
- **LinkedIn**: Text, images, carousels, article links
- **Telegram**: Text, photos, media groups (carousels), link previews

All servers support hashtags and are fully Dockerized for stability.

## Quick Start

### 1. Set Up Environment Files

Copy the example files and fill in your credentials:

```bash
# Facebook/Instagram
cp .env.facebook.example .env.facebook
# Edit .env.facebook with your tokens

# LinkedIn
cp .env.linkedin.example .env.linkedin
# Edit .env.linkedin with your tokens

# Telegram
cp .env.telegram.example .env.telegram
# Edit .env.telegram with your tokens
```

### 2. Run with Docker Compose (RECOMMENDED)

```bash
# Build all containers
docker-compose build

# Start all servers
docker-compose up -d

# Start specific server
docker-compose up -d facebook
docker-compose up -d linkedin
docker-compose up -d telegram

# View logs
docker-compose logs -f facebook
docker-compose logs -f linkedin
docker-compose logs -f telegram

# Stop all servers
docker-compose down

# Stop specific server
docker-compose stop facebook
```

### 3. Run Individually with Docker

```bash
# Facebook
docker build -t facebook-mcp-server:latest -f Dockerfile .
docker run --rm -it --env-file .env.facebook facebook-mcp-server:latest

# LinkedIn
docker build -t linkedin-mcp-server:latest -f Dockerfile.linkedin .
docker run --rm -it --env-file .env.linkedin linkedin-mcp-server:latest

# Telegram
docker build -t telegram-mcp-server:latest -f Dockerfile.telegram .
docker run --rm -it --env-file .env.telegram telegram-mcp-server:latest
```

### 4. Run Locally with UV (Development)

```bash
# Install dependencies
uv sync

# Run servers
uv run facebook-mcp-server
uv run linkedin-mcp-server
uv run telegram-mcp-server
```

## Configuration Persistence

**✅ Your credentials are safe!** Environment files are:
- Stored outside containers
- Mounted at runtime via `env_file` in docker-compose
- Never baked into Docker images
- Gitignored by default

**To update credentials:**
1. Edit your `.env.facebook`, `.env.linkedin`, or `.env.telegram` files
2. Restart the specific container: `docker-compose restart facebook`
3. No rebuild needed!

## Available Tools

### Facebook/Instagram Tools

1. **post_media** - Advanced posting (images, carousels, videos, reels)
   - Single image posts
   - Multiple images (carousel/album)
   - Videos and reels
   - Cross-post to Facebook & Instagram
   - Hashtag support via caption

2. **post_to_facebook** - Simple text posts (legacy)

3. **get_page_posts** - Fetch recent posts

4. **get_post_comments** - Get comments on a post

5. **reply_to_comment** - Reply to comments

6. **filter_negative_comments** - Filter negative comments

7. **delete_post** - Delete a post

8. **delete_comment** - Delete a comment

### LinkedIn Tools

1. **linkedin_create_text_post** - Text posts with hashtags

2. **linkedin_create_image_post** - Single image with caption and hashtags

3. **linkedin_create_carousel_post** - Multiple images (2-10) with hashtags

4. **linkedin_create_link_post** - Share articles/links with hashtags

5. **linkedin_list_posts** - Fetch recent posts

6. **linkedin_comment_on_post** - Comment on posts

7. **linkedin_get_comments** - Get post comments

8. **linkedin_delete_post** - Delete posts

### Telegram Tools

1. **telegram_send_message** - Text messages with hashtags

2. **telegram_send_photo** - Single photo with caption and hashtags

3. **telegram_send_media_group** - Carousel/album (2-10 photos) with hashtags

4. **telegram_send_link** - Links with preview and hashtags

5. **telegram_get_updates** - Fetch bot updates

## Usage Examples

### Creating Posts with Hashtags

**Facebook/Instagram:**
```python
# Single image with hashtags
post_media(
  caption="Check out our new product! #marketing #business #growth",
  media_urls=["https://example.com/image.jpg"],
  media_type="image",
  platforms=["facebook", "instagram"]
)

# Carousel with hashtags
post_media(
  caption="Summer collection is here! #fashion #style #summer",
  media_urls=[
    "https://example.com/img1.jpg",
    "https://example.com/img2.jpg",
    "https://example.com/img3.jpg"
  ],
  media_type="carousel",
  platforms=["facebook", "instagram"]
)
```

**LinkedIn:**
```python
# Text post with hashtags
linkedin_create_text_post(
  text="Exciting company update!",
  hashtags=["tech", "innovation", "startup"]
)

# Image post with hashtags
linkedin_create_image_post(
  text="Our latest achievement",
  image_url="https://example.com/image.jpg",
  hashtags=["success", "teamwork"]
)

# Carousel with hashtags
linkedin_create_carousel_post(
  text="Product showcase",
  image_urls=[
    "https://example.com/img1.jpg",
    "https://example.com/img2.jpg"
  ],
  hashtags=["product", "launch"]
)

# Share article with hashtags
linkedin_create_link_post(
  text="Great article about AI trends",
  link_url="https://example.com/article",
  hashtags=["AI", "technology", "trends"]
)
```

**Telegram:**
```python
# Text with hashtags
telegram_send_message(
  text="New update available!",
  hashtags=["update", "news"]
)

# Single photo with hashtags
telegram_send_photo(
  photo_url="https://example.com/photo.jpg",
  caption="New feature release",
  hashtags=["feature", "release"]
)

# Media group (carousel) with hashtags
telegram_send_media_group(
  media_urls=[
    "https://example.com/img1.jpg",
    "https://example.com/img2.jpg",
    "https://example.com/img3.jpg"
  ],
  caption="Event highlights",
  hashtags=["event", "highlights", "2024"]
)

# Link with preview and hashtags
telegram_send_link(
  text="Check out this article",
  link_url="https://example.com/article",
  hashtags=["article", "mustread"]
)
```

## MCP Client Configuration (Claude Desktop)

Add to your Claude Desktop config at `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "facebook": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--env-file", "/Users/kapilthakare/Projects/facebook-mcp-server/.env.facebook", "facebook-mcp-server:latest"]
    },
    "linkedin": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--env-file", "/Users/kapilthakare/Projects/facebook-mcp-server/.env.linkedin", "linkedin-mcp-server:latest"]
    },
    "telegram": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--env-file", "/Users/kapilthakare/Projects/facebook-mcp-server/.env.telegram", "telegram-mcp-server:latest"]
    }
  }
}
```

**Note:** Adjust the paths to match your setup.

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs facebook

# Verify env file exists
ls -la .env.facebook .env.linkedin .env.telegram

# Test credentials manually
docker run --rm -it --env-file .env.facebook facebook-mcp-server:latest
```

### Update credentials
```bash
# Edit the env file
nano .env.facebook

# Restart the container (no rebuild needed!)
docker-compose restart facebook
```

### Rebuild after code changes
```bash
# Rebuild specific service
docker-compose build facebook

# Rebuild all
docker-compose build

# Rebuild and restart
docker-compose up -d --build facebook
```

### Clean everything and start fresh
```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi facebook-mcp-server:latest
docker rmi linkedin-mcp-server:latest
docker rmi telegram-mcp-server:latest

# Rebuild everything
docker-compose build
docker-compose up -d
```

## Getting API Credentials

### Facebook/Instagram
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create an app and get Page Access Token
3. Get your Page ID from your Facebook Page settings
4. For Instagram: Link Instagram Business Account and get Account ID
5. See `get-AppID-secret-long-short-lived-tokens-process.md` for detailed steps

### LinkedIn
1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create an app and request appropriate permissions
3. Generate OAuth 2.0 access token
4. Get your Organization ID from your LinkedIn Company Page URL

### Telegram
1. Talk to [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Save the bot token
4. Get your Chat ID by messaging your bot and checking updates

## Features Checklist

✅ **All Platforms Support:**
- Text posts with hashtags
- Single image posts with hashtags
- Multiple image posts (carousels) with hashtags
- Link/article sharing with hashtags

✅ **Facebook/Instagram:**
- Video and Reel posting
- Cross-posting to both platforms
- Comment management

✅ **LinkedIn:**
- Organization posting
- Image uploads (not just links)
- Carousel support (2-10 images)

✅ **Telegram:**
- Media groups (2-10 photos)
- Link previews
- Message customization

✅ **Infrastructure:**
- Fully Dockerized
- Config persistence (no rebuild needed)
- Separate env files per platform
- Easy docker-compose management
- Volume mapping for future state persistence

## Next Steps for Primes & Zooms

1. **Set up credentials** for all three platforms
2. **Test each server** with a simple post
3. **Create posting workflow** in Claude Desktop
4. **Schedule regular posts** using your preferred scheduling tool
5. **Monitor and respond** to engagement

Happy posting! 🚀
