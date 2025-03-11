# This program is free software: you can redistribute it and/or modify it under the terms of 
# the GNU General Public License as published by the Free Software Foundation, either 
# version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this
# program. If not, see <https://www.gnu.org/licenses/>. 

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