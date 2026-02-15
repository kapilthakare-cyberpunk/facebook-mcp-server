import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from .env
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")

GRAPH_API_VERSION = "v18.0"
GRAPH_API_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

def get_instagram_business_account_id(page_id: str, access_token: str) -> str | None:
    """Fetches the connected Instagram Business Account ID for a given Facebook Page ID."""
    url = f"{GRAPH_API_BASE_URL}/{page_id}"
    params = {
        "fields": "instagram_business_account",
        "access_token": access_token,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        
        if "instagram_business_account" in data and "id" in data["instagram_business_account"]:
            return data["instagram_business_account"]["id"]
        else:
            print(f"No Instagram Business Account found for Page ID {page_id}.")
            print(f"API Response: {data}")
            return None
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        print(f"Response content: {err.response.text}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

def main():
    if not PAGE_ID or not PAGE_ACCESS_TOKEN:
        print("Error: FACEBOOK_PAGE_ID or FACEBOOK_PAGE_ACCESS_TOKEN not set in .env")
        sys.exit(1)

    print(f"Fetching Instagram Business Account ID for Facebook Page ID: {PAGE_ID}...")
    instagram_id = get_instagram_business_account_id(PAGE_ID, PAGE_ACCESS_TOKEN)

    if instagram_id:
        print(f"\nYour Instagram Business Account ID is: {instagram_id}")
        print("Please add this to your .env file as: INSTAGRAM_ACCOUNT_ID={id}")
    else:
        print("Could not retrieve Instagram Business Account ID.")

if __name__ == "__main__":
    main()
