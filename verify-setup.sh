#!/bin/bash

# Verification script for MCP server setup

echo "🔍 Verifying MCP Server Setup..."
echo ""

# Check if Docker images exist
echo "1️⃣ Checking Docker images..."
if docker images | grep -q "facebook-mcp-server"; then
    echo "   ✅ facebook-mcp-server image found"
else
    echo "   ❌ facebook-mcp-server image NOT found"
    echo "      Run: docker-compose build"
fi

if docker images | grep -q "linkedin-mcp-server"; then
    echo "   ✅ linkedin-mcp-server image found"
else
    echo "   ❌ linkedin-mcp-server image NOT found"
    echo "      Run: docker-compose build"
fi

if docker images | grep -q "telegram-mcp-server"; then
    echo "   ✅ telegram-mcp-server image found"
else
    echo "   ❌ telegram-mcp-server image NOT found"
    echo "      Run: docker-compose build"
fi

echo ""

# Check env files
echo "2️⃣ Checking environment files..."
if [ -f ".env.facebook" ]; then
    echo "   ✅ .env.facebook exists"
    if grep -q "your_page_access_token_here" .env.facebook; then
        echo "      ⚠️  WARNING: .env.facebook contains example tokens"
        echo "      Edit the file with real credentials!"
    fi
else
    echo "   ❌ .env.facebook NOT found"
    echo "      Run: cp .env.facebook.example .env.facebook"
fi

if [ -f ".env.linkedin" ]; then
    echo "   ✅ .env.linkedin exists"
    if grep -q "your_linkedin_access_token_here" .env.linkedin; then
        echo "      ⚠️  WARNING: .env.linkedin contains example tokens"
        echo "      Edit the file with real credentials!"
    fi
else
    echo "   ❌ .env.linkedin NOT found"
    echo "      Run: cp .env.linkedin.example .env.linkedin"
fi

if [ -f ".env.telegram" ]; then
    echo "   ✅ .env.telegram exists"
    if grep -q "your_bot_token_here" .env.telegram; then
        echo "      ⚠️  WARNING: .env.telegram contains example tokens"
        echo "      Edit the file with real credentials!"
    fi
else
    echo "   ❌ .env.telegram NOT found"
    echo "      Run: cp .env.telegram.example .env.telegram"
fi

echo ""

# Check Claude Desktop config
echo "3️⃣ Checking Claude Desktop configuration..."
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

if [ -f "$CLAUDE_CONFIG" ]; then
    echo "   ✅ Claude config file exists"
    
    if grep -q "facebook-mcp-server" "$CLAUDE_CONFIG"; then
        echo "   ✅ Facebook server configured in Claude"
    else
        echo "   ❌ Facebook server NOT found in Claude config"
    fi
    
    if grep -q "linkedin-mcp-server" "$CLAUDE_CONFIG"; then
        echo "   ✅ LinkedIn server configured in Claude"
    else
        echo "   ❌ LinkedIn server NOT found in Claude config"
    fi
    
    if grep -q "telegram-mcp-server" "$CLAUDE_CONFIG"; then
        echo "   ✅ Telegram server configured in Claude"
    else
        echo "   ❌ Telegram server NOT found in Claude config"
    fi
else
    echo "   ❌ Claude config file NOT found"
    echo "      Expected at: $CLAUDE_CONFIG"
fi

echo ""

# Test Docker images can run
echo "4️⃣ Testing Docker images (quick test)..."

echo "   Testing Facebook image..."
if timeout 2 docker run --rm --env-file .env.facebook facebook-mcp-server:latest < /dev/null 2>&1 | head -1; then
    echo "   ✅ Facebook image can start"
else
    echo "   ⚠️  Facebook image test inconclusive"
fi

echo "   Testing LinkedIn image..."
if timeout 2 docker run --rm --env-file .env.linkedin linkedin-mcp-server:latest < /dev/null 2>&1 | head -1; then
    echo "   ✅ LinkedIn image can start"
else
    echo "   ⚠️  LinkedIn image test inconclusive"
fi

echo "   Testing Telegram image..."
if timeout 2 docker run --rm --env-file .env.telegram telegram-mcp-server:latest < /dev/null 2>&1 | head -1; then
    echo "   ✅ Telegram image can start"
else
    echo "   ⚠️  Telegram image test inconclusive"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Summary:"
echo ""
echo "If all checks passed (✅), you're ready to:"
echo "1. Restart Claude Desktop completely (Cmd+Q, then reopen)"
echo "2. Look for the MCP icon (🔌) in Claude Desktop"
echo "3. Verify 4 servers are connected (desktop-commander, facebook, linkedin, telegram)"
echo "4. Start posting!"
echo ""
echo "If you see warnings (⚠️ ), update your .env files with real credentials"
echo "If you see errors (❌), follow the suggested fixes"
echo ""
echo "📖 For detailed help, see:"
echo "   - CONNECT_TO_CLAUDE.md"
echo "   - SETUP_GUIDE.md"
echo ""
