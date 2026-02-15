import os
import sys
import json
from facebook_mcp_server.server import FacebookManager, load_facebook_config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    if len(sys.argv) < 3:
        print("Usage: python facebook_cli_tool.py <tool_name> <json_arguments>")
        sys.exit(1)

    tool_name = sys.argv[1]
    
    try:
        tool_args = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print("Error: Invalid JSON arguments provided.")
        sys.exit(1)

    try:
        page_id, page_access_token, instagram_account_id = load_facebook_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

    manager = FacebookManager(
        page_id=page_id,
        access_token=page_access_token,
        instagram_account_id=instagram_account_id
    )
    
    result = None
    try:
        if tool_name == "post_to_facebook":
            result = manager.post_to_facebook(tool_args["message"])
        elif tool_name == "post_media":
            result = manager.post_media(
                caption=tool_args["caption"],
                media_urls=tool_args.get("media_urls", []),
                media_type=tool_args["media_type"],
                platforms=tool_args["platforms"]
            )
        elif tool_name == "reply_to_comment":
            result = manager.reply_to_comment(
                tool_args["post_id"], tool_args["comment_id"], tool_args["message"]
            )
        elif tool_name == "get_page_posts":
            result = manager.get_page_posts()
        elif tool_name == "get_post_comments":
            result = manager.get_post_comments(tool_args["post_id"])
        elif tool_name == "filter_negative_comments":
            comments = manager.get_post_comments(tool_args["post_id"])
            result = manager.filter_negative_comments(comments)
        elif tool_name == "delete_post":
            result = manager.delete_post(tool_args["post_id"])
        elif tool_name == "delete_comment":
            result = manager.delete_comment(tool_args["comment_id"])
        else:
            print(f"Error: Unknown tool name '{tool_name}'")
            sys.exit(1)
        
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error executing tool '{tool_name}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
