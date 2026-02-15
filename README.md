# Social Media MCP Servers
<img src="https://badge.mcpx.dev?type=server" title="MCP Server"/>

Production-ready MCP servers for **Facebook, Instagram, LinkedIn, and Telegram** with full support for images, carousels, links, and hashtags.

## 🚀 Quick Start

```bash
# 1. Set up credentials
cp .env.facebook.example .env.facebook  # Edit with your tokens
cp .env.linkedin.example .env.linkedin  # Edit with your tokens
cp .env.telegram.example .env.telegram  # Edit with your tokens

# 2. Run with Docker Compose (RECOMMENDED)
docker-compose up -d

# 3. View logs
docker-compose logs -f
```

**That's it!** Your servers are running and credentials are safely stored.

## 📋 Features

### Facebook & Instagram
- ✅ Text, image, carousel, video, reel posts
- ✅ Cross-post to both platforms
- ✅ Hashtag support
- ✅ Comment management
- ✅ Post moderation

### LinkedIn
- ✅ Text posts with hashtags
- ✅ Single image posts
- ✅ Carousel posts (2-10 images)
- ✅ Article/link sharing
- ✅ Comment management

### Telegram
- ✅ Text messages with hashtags
- ✅ Single photo posts
- ✅ Media groups (carousels, 2-10 photos)
- ✅ Link previews
- ✅ Bot updates

## 🔧 What Makes This Special

**For Semi-Advanced Vibe Coders:**
- ✅ **No Breaking Changes**: Docker isolation protects your setup
- ✅ **Config Persistence**: Update credentials without rebuilding
- ✅ **Exact Working Fix**: All tools tested and functional
- ✅ **Hashtag Support**: Built-in for all platforms
- ✅ **Straightforward API**: Simple, consistent tool interfaces

## 📖 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup and usage guide
- **[get-AppID-secret-long-short-lived-tokens-process.md](get-AppID-secret-long-short-lived-tokens-process.md)** - Facebook/Instagram credentials

## 🎯 Common Use Cases

### Post across all platforms
```bash
# Same content, different platforms
linkedin_create_image_post(text="New product!", image_url="...", hashtags=["launch"])
post_media(caption="New product!", media_urls=["..."], media_type="image", platforms=["facebook", "instagram"])
telegram_send_photo(photo_url="...", caption="New product!", hashtags=["launch"])
```

### Share article/link
```bash
linkedin_create_link_post(text="Must read", link_url="...", hashtags=["article"])
telegram_send_link(text="Must read", link_url="...", hashtags=["article"])
# Facebook: Use post_to_facebook with link in text
```

### Carousel posts
```bash
linkedin_create_carousel_post(text="...", image_urls=[...], hashtags=["..."])
post_media(caption="...", media_urls=[...], media_type="carousel", platforms=["facebook"])
telegram_send_media_group(media_urls=[...], caption="...", hashtags=["..."])
```

## 🐳 Docker Management

```bash
# Start all servers
docker-compose up -d

# Start specific server
docker-compose up -d facebook

# View logs
docker-compose logs -f linkedin

# Restart after config change (NO REBUILD NEEDED!)
docker-compose restart telegram

# Stop all
docker-compose down

# Rebuild after code changes
docker-compose build
docker-compose up -d
```

## 🔐 Config Persistence

Your credentials are:
- ✅ Stored in separate `.env.facebook`, `.env.linkedin`, `.env.telegram` files
- ✅ Mounted at runtime (not baked into images)
- ✅ Safe to update without rebuilding containers
- ✅ Gitignored by default

**To update credentials:**
1. Edit the `.env.*` file
2. Run `docker-compose restart <service>`
3. Done!

## 🛠️ Local Development

```bash
# Install dependencies
uv sync

# Run servers locally
uv run facebook-mcp-server
uv run linkedin-mcp-server
uv run telegram-mcp-server
```

## 📦 MCP Client Config

For Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "facebook": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--env-file", "/path/to/project/.env.facebook", "facebook-mcp-server:latest"]
    },
    "linkedin": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--env-file", "/path/to/project/.env.linkedin", "linkedin-mcp-server:latest"]
    },
    "telegram": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--env-file", "/path/to/project/.env.telegram", "telegram-mcp-server:latest"]
    }
  }
}
```

## 🎓 For Primes & Zooms

Perfect for managing social media across platforms:
1. Set up once with docker-compose
2. Post consistently with simple tool calls
3. Manage engagement and comments
4. Never worry about breaking your setup

## 📝 License

MIT License - See LICENSE for details.

## 🤝 Contributing

Issues and PRs welcome!
