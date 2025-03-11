from dotenv import load_dotenv
import os
load_dotenv()

import asyncio
from twikit import Client
import json
import sys
    

async def get_tweet(tweet_url):

    client = Client('en-US')
    twitter_username = os.getenv("TWITTER_USERNAME")
    twitter_email = os.getenv("TWITTER_EMAIL")
    twitter_password = os.getenv("TWITTER_PASSWORD")

    if not twitter_username or not twitter_email or not twitter_password:
        print("missing twitter variables!")
        sys.exit(1)

    # must be called using `await`.
    await client.login(
        auth_info_1=twitter_username,
        auth_info_2=twitter_email,
        password=twitter_password
    )
    tweet_id = tweet_url.split("/")[-1]
    tweet = await client.get_tweet_by_id(tweet_id)


    # tweet object is class instance with no easy way to dump. Just grab what we want 
    # into own dict
    tweet_json = {
        'url': tweet_url,
        'user': {
            'id': tweet.user.id,
            'name': tweet.user.name,
            'screen_name': tweet.user.screen_name,
        },
        'text': tweet.text,
        'created_at_datetime': tweet.created_at_datetime.timestamp(),
        'created_at': tweet.created_at
    }
    with open("tweet.json", "w") as f:
        json.dump(tweet_json, f, indent=4)


async def main():

    print("do not use this script! - see README.md")
    sys.exit(1)

    # Example usage
    tweet_url = "https://x.com/elonmusk/status/1519480761749016577"
    await get_tweet(tweet_url)
    print("finished!")     

asyncio.run(main())