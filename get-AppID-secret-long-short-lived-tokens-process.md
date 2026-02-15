• Here’s a concise, click-through style path to get App ID/Secret, short-lived token, long-lived user token, then Page token/ID:

  - App ID & Secret:
      - Go to https://developers.facebook.com/apps/ → select your app (or create one).
      - In the left nav, open Settings → Basic: copy App ID and App Secret (click “Show”).
  - Short-lived user access token:
      - Go to Tools → Graph API Explorer: https://developers.facebook.com/tools/explorer
      - Pick your app in the top-right dropdown; ensure the user is the right profile.
      - Under Permissions, add what you need (e.g., pages_show_list, pages_read_engagement, pages_manage_posts).
      - Click Generate Access Token → copy the short-lived token.
  - Exchange for a long-lived user token:
      - Hit this URL in a browser (replace placeholders):
        https://graph.facebook.com/v18.0/oauth/access_token?
        grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_LIVED_TOKEN
      - Response JSON contains "access_token" — that’s your long-lived user token.
  - Get Page ID and long-lived Page token:
      - Call: https://graph.facebook.com/v18.0/me/accounts?access_token=YOUR_LONG_LIVED_USER_TOKEN
      - For each Page, you’ll see id (Page ID) and access_token (long-lived Page token). Use these for your .env.
  - Plug into your MCP server:
      - FACEBOOK_PAGE_ID=...
      - FACEBOOK_PAGE_ACCESS_TOKEN=...
  - Security note: keep tokens/secret private; rotate any token you’ve shared or pasted in public contexts.


