# 🔌 Connecting to Claude Desktop - Complete Guide

## ✅ Configuration Complete!

Your Claude Desktop is now configured with all three social media MCP servers!

## 🔄 Next Steps

### 1. Restart Claude Desktop

**IMPORTANT:** You must completely quit and restart Claude Desktop for the changes to take effect.

**On macOS:**
```bash
# Quit Claude Desktop completely (Cmd+Q)
# Or force quit:
killall Claude

# Then reopen Claude Desktop from Applications
```

### 2. Verify Servers Are Connected

After restarting Claude Desktop, look for the **MCP icon** (🔌) in the interface. You should see:
- ✅ desktop-commander
- ✅ facebook
- ✅ linkedin  
- ✅ telegram

**If you see these 4 servers, you're ready to go!**

### 3. Check Available Tools

In your next Claude chat, ask:
```
What MCP tools do I have available?
```

You should see tools from all platforms:
- **Facebook:** post_media, get_page_posts, reply_to_comment, etc.
- **LinkedIn:** linkedin_create_text_post, linkedin_create_image_post, etc.
- **Telegram:** telegram_send_message, telegram_send_photo, etc.

## 🎯 Testing Your Setup

### Quick Test Commands

**Test Facebook/Instagram:**
```
Use the Facebook MCP server to post a test message: "Testing my new MCP setup! #test"
```

**Test LinkedIn:**
```
Use LinkedIn to create a text post: "Testing LinkedIn MCP integration #test"
```

**Test Telegram:**
```
Use Telegram to send a test message: "MCP integration working! #success"
```

## 📝 Example: Create Your First Cross-Platform Post

Once connected, try this:

```
I want to post the same message across all three platforms:

Message: "Excited to announce our new product launch! 🚀"
Hashtags: #productlaunch #innovation #technology

Please post this to:
1. Facebook and Instagram (as a text post)
2. LinkedIn (as a text post)
3. Telegram (as a message)
```

Claude will use your MCP servers to post across all platforms!

## 🖼️ Example: Post with Images

```
I have an image at: https://example.com/product.jpg

Post this image with caption "Our new product is here!" to:
1. Facebook and Instagram (single image post with #newproduct #launch)
2. LinkedIn (single image post with #product #announcement)
3. Telegram (photo with #launch #product)
```

## 📊 Example: Create a Carousel Post

```
I have 3 images:
- https://example.com/img1.jpg
- https://example.com/img2.jpg
- https://example.com/img3.jpg

Create carousel posts with caption "Product showcase" across:
1. Facebook with #showcase #products
2. LinkedIn carousel with #portfolio #work
3. Telegram media group with #gallery #products
```

## 🔗 About Other AI Models (Gemini, Codex, Qwen)

**Important:** MCP (Model Context Protocol) servers are currently **only supported by Claude Desktop**.

Other AI models like:
- ❌ Gemini - No MCP support
- ❌ OpenAI Codex - No MCP support  
- ❌ Qwen - No MCP support

**However**, you can still use these servers through:
1. **API Integration** - Call the tools programmatically
2. **Custom Wrappers** - Build your own integration layer
3. **Wait for MCP adoption** - Other platforms may add support in future

## 🛠️ Troubleshooting

### Servers Not Showing in Claude

1. **Verify config file location:**
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Check for syntax errors:**
   - Must be valid JSON
   - All quotes must be straight quotes, not curly
   - Paths must be absolute (no ~)

3. **Verify env files exist:**
   ```bash
   ls -la /Users/kapilthakare/Projects/facebook-mcp-server/.env.*
   ```

4. **Test Docker images:**
   ```bash
   docker run --rm -i --env-file .env.facebook facebook-mcp-server:latest
   ```
   Press Ctrl+C to exit if it waits for input.

### Tools Not Working

1. **Check credentials in env files:**
   ```bash
   nano .env.facebook
   nano .env.linkedin
   nano .env.telegram
   ```

2. **Verify tokens are valid:**
   - Facebook: Test with Graph API Explorer
   - LinkedIn: Check token expiration
   - Telegram: Message your bot to verify

3. **Check Claude Desktop logs:**
   ```bash
   # macOS logs location
   ~/Library/Logs/Claude/
   ```

### Permission Errors

If you get permission errors:
```bash
chmod 644 /Users/kapilthakare/Projects/facebook-mcp-server/.env.*
```

## 🎓 Pro Tips for Primes & Zooms

### 1. Create Posting Templates

Save common posts as templates in Claude:
```
Save this as my "product launch template":
- Caption: [PRODUCT_NAME] is now available!
- Hashtags: #launch #newproduct #innovation
- Platforms: Facebook, LinkedIn, Telegram
```

### 2. Batch Posting

Post to all platforms at once:
```
Post this across all platforms: "[message]"
Use hashtags: [tags]
```

### 3. Schedule Content

While MCP doesn't have built-in scheduling, you can:
- Prepare posts in advance
- Copy the command Claude generates
- Run it later via script or cron

### 4. Monitor Engagement

```
Check my recent posts and comments on all platforms
```

## 📱 Mobile Posting

Currently, MCP servers only work through Claude Desktop. For mobile:
- Use platform native apps
- Or build a custom API wrapper
- Or wait for Claude mobile MCP support

## 🚀 You're Ready!

Your setup is complete! Just:
1. ✅ Restart Claude Desktop
2. ✅ Verify servers are connected
3. ✅ Start posting!

**Next:** Open a new chat in Claude Desktop and try the test commands above!
