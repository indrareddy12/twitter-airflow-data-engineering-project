import tweepy
import pandas as pd 
import json
import os
from datetime import datetime
import s3fs 
from xquik_export import load_xquik_rows

def run_twitter_etl():

    xquik_export_path = os.getenv("XQUIK_EXPORT_PATH", "").strip()
    if xquik_export_path:
        df = pd.DataFrame(load_xquik_rows(xquik_export_path))
        df.to_csv(os.getenv("X_OUTPUT_PATH", "refined_tweets.csv"), index=False)
        return df

    access_key = os.getenv("TWITTER_ACCESS_KEY", "")
    access_secret = os.getenv("TWITTER_ACCESS_SECRET", "")
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY", "")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET", "")


    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)   
    auth.set_access_token(consumer_key, consumer_secret) 

    # # # Creating an API object 
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@elonmusk', 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )

    tweet_rows = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}
        
        tweet_rows.append(refined_tweet)

    df = pd.DataFrame(tweet_rows)
    df.to_csv(os.getenv("X_OUTPUT_PATH", "refined_tweets.csv"), index=False)
    return df
