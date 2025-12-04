import os
import sys
from facebook_mcp_server.server import FacebookManager, load_facebook_config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    try:
        page_id, page_access_token = load_facebook_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        return

    manager = FacebookManager(page_id, page_access_token)
    
    print(f"Fetching posts for Page ID: {page_id}...")
    posts_data = manager.get_page_posts()
    
    if 'data' in posts_data:
        posts = posts_data['data']
        print(f"Found {len(posts)} posts.")
        
        # Get last two posts
        last_two = posts[:2]
        
        for i, post in enumerate(last_two, 1):
            print(f"\n--- Post {i} ---")
            print(f"ID: {post.get('id')}")
            print(f"Created Time: {post.get('created_time')}")
            print(f"Message: {post.get('message', '[No message]')}")
    else:
        print("No 'data' field in response.")
        print(posts_data)

if __name__ == "__main__":
    main()

