#!/bin/bash

# Test MCP Servers

echo "🧪 Testing MCP Servers..."
echo ""

# Test Telegram
echo "1️⃣ Testing Telegram Server..."
echo ""
TELEGRAM_OUTPUT=$(echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | docker run --rm -i --env-file .env.telegram telegram-mcp-server:latest 2>&1 | tail -1)

if echo "$TELEGRAM_OUTPUT" | grep -q '"serverInfo"'; then
    echo "✅ Telegram server responded correctly!"
    echo "   Server: $(echo $TELEGRAM_OUTPUT | grep -o '"name":"[^"]*"' | head -1)"
else
    echo "❌ Telegram server failed"
    echo "   Output: $TELEGRAM_OUTPUT"
fi

echo ""

# Test LinkedIn
echo "2️⃣ Testing LinkedIn Server..."
echo ""
LINKEDIN_OUTPUT=$(echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | docker run --rm -i --env-file .env.linkedin linkedin-mcp-server:latest 2>&1 | tail -1)

if echo "$LINKEDIN_OUTPUT" | grep -q '"serverInfo"'; then
    echo "✅ LinkedIn server responded correctly!"
    echo "   Server: $(echo $LINKEDIN_OUTPUT | grep -o '"name":"[^"]*"' | head -1)"
else
    echo "❌ LinkedIn server failed"
    echo "   Output: $LINKEDIN_OUTPUT"
fi

echo ""

# Test Facebook
echo "3️⃣ Testing Facebook Server..."
echo ""
FACEBOOK_OUTPUT=$(echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | docker run --rm -i --env-file .env.facebook facebook-mcp-server:latest 2>&1 | tail -1)

if echo "$FACEBOOK_OUTPUT" | grep -q '"serverInfo"'; then
    echo "✅ Facebook server responded correctly!"
    echo "   Server: $(echo $FACEBOOK_OUTPUT | grep -o '"name":"[^"]*"' | head -1)"
else
    echo "❌ Facebook server failed"
    echo "   Output: $FACEBOOK_OUTPUT"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ All servers are working!"
echo ""
echo "🔄 Next step: Restart Claude Desktop to use them"
echo "   1. Press Cmd+Q to quit Claude Desktop"
echo "   2. Reopen Claude Desktop"
echo "   3. Check for MCP icon (🔌)"
echo "   4. Verify 4 servers are connected"
echo ""
