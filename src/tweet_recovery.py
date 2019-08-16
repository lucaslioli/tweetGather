import sys
import time
import tweepy
import datetime
from textblob import TextBlob

sys.path.append('./')
from helper.authenticate import api_tokens
from helper.db_connection import DbConnecion
from helper.log import logfile
from src.stream_listener import process_status

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

    count = len(last_tweets)
    for tw in last_tweets:

        user_info = "User: {} - {}".format(tw['user_id'], tw['user_name'])
        print("\n\n {} {}".format(count, user_info))

        try:
            # The maximum count = 200
            newest =  api.user_timeline(user_id=tw['user_id'], count=1)[0]
            diff = newest.author.statuses_count - tw['counter']

            while diff > 0:
                statuses =  api.user_timeline(user_id=tw['user_id'], since_id=tw['tweet_id'], max_id=newest.id, count=200)
                print("List size: ", len(statuses))

                for st in statuses:
                    diff -= 1
                    try:
                        process_status(st)
                        message = "{} > Inserted tweet {} - {} - {}".format(user_info, st.id, st.created_at, diff)
                    
                    except Exception as e:
                        message = "{} > Tweet {} not inserted. Error: {}".format(user_info, st.id, e)

                    logfile(message)
                    print(message)

                time.sleep(0.5)

        except Exception as e:
            message = "{} > ERROR: {}".format(user_info, e)
            logfile(message)
            print(message)
        break

        count -= 1