import sys
import time
import tweepy
import datetime
from textblob import TextBlob

sys.path.append('./')
from helper.authenticate import api_tokens
from helper.db_connection import DbConnecion
from helper.log import logfile

# COMPILE WITH: $ python3 tweet_recovery.py
if __name__ == '__main__':
    keys = api_tokens()

    # Obtenção das chaves de atenticação da API
    access_token        = keys['access_token']
    access_token_secret = keys['access_token_secret']
    consumer_key        = keys['consumer_key']
    consumer_secret     = keys['consumer_secret']

    # Autenticação com a API Tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Autenticação com a API
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    conn = DbConnecion()

    last_tweets = conn.last_tweets_list()

    count = 1
    for lt in last_tweets:

        print(count, "User: ", lt['user_id'], "-", lt['user_name'])

        try:
            # The maximum count = 200
            tweets =  api.user_timeline(user_id=lt['user_id'], since_id=lt['tweet_id'], count=2)
            print("  List size: ", len(tweets), "\n")
        
        except Exception as e:
            print('  Failed to upload to ftp: '+ str(e) ,'Probably deactivated account! \n')

        # TO DO
        # Insert all searched tweets until the difference between statuses_count been zero

        # for tw in tweets:
        #     tw.text = tw.text.replace('\n', ' ').replace('\r', '')
        #     print(tw.created_at, " | ", tw.id, " | ", tw.text[:42], "...")

        count += 1
        time.sleep(0.5)
    