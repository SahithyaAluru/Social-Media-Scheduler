import schedule
import time
import requests
import json

# Example social media API integration (Placeholder URLs & Tokens)
PLATFORM_APIS = {
    "twitter": "https://api.twitter.com/2/tweets",
    "facebook": "https://graph.facebook.com/v12.0/me/feed",
    "linkedin": "https://api.linkedin.com/v2/ugcPosts"
}

ACCESS_TOKENS = {
    "twitter": "YOUR_TWITTER_ACCESS_TOKEN",
    "facebook": "YOUR_FACEBOOK_ACCESS_TOKEN",
    "linkedin": "YOUR_LINKEDIN_ACCESS_TOKEN"
}

def post_content(platform, message):
    """Posts content to the specified platform."""
    url = PLATFORM_APIS.get(platform)
    token = ACCESS_TOKENS.get(platform)
    
    if not url or not token:
        print(f"Invalid platform or missing access token for {platform}")
        return
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {}
    
    if platform == "twitter":
        data = {"text": message}
    elif platform == "facebook":
        data = {"message": message}
    elif platform == "linkedin":
        data = {"author": "urn:li:person:YOUR_PERSON_ID", "lifecycleState": "PUBLISHED", "specificContent": {"com.linkedin.ugc.ShareContent": {"shareCommentary": {"text": message}, "shareMediaCategory": "NONE"}}, "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200 or response.status_code == 201:
        print(f"Successfully posted to {platform}.")
    else:
        print(f"Failed to post to {platform}: {response.text}")

def schedule_post(platform, message, post_time):
    """Schedules a post for a specific time."""
    schedule.every().day.at(post_time).do(post_content, platform, message)
    print(f"Scheduled post for {platform} at {post_time}")

def main():
    print("Social Media Scheduler")
    while True:
        print("1. Schedule a Post")
        print("2. Run Scheduled Posts")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            platform = input("Enter platform (twitter/facebook/linkedin): ").strip().lower()
            message = input("Enter message: ")
            post_time = input("Enter posting time (HH:MM, 24-hour format): ")
            schedule_post(platform, message, post_time)
        elif choice == "2":
            print("Running scheduled posts...")
            while True:
                schedule.run_pending()
                time.sleep(60)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
