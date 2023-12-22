import tweepy
import pandas as pd
from datetime import datetime

# Set up API credentials
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"
access_token = "your_access_token"
access_token_secret = "your_access_token_secret"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def fetch_tweets(keyword, num_tweets=10):
    data = {
        "Username": [],
        "Date Posted": [],
        "Content": [],
        "Likes": [],
        "Retweets": [],
        "Comments": [],
    }

    tweets = tweepy.Cursor(
        api.search, q=keyword, tweet_mode="extended", lang="en"
    ).items(num_tweets)

    for tweet in tweets:
        # Ignore retweets
        if hasattr(tweet, "retweeted_status"):
            continue

        data["Username"].append(tweet.user.screen_name)
        data["Date Posted"].append(tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        data["Content"].append(tweet.full_text)
        data["Likes"].append(tweet.favorite_count)
        data["Retweets"].append(tweet.retweet_count)
        data["Comments"].append(tweet.reply_count)

    return pd.DataFrame(data)


df = fetch_tweets(keyword="ChatGPT", num_tweets=3)
print(df)
