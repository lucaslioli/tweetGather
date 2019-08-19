import sys
import time
import tweepy
import datetime
import progressbar
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

        user_info = "{} User: {} - {}".format(count, tw['user_id'], tw['user_name'])
                
        logfile(user_info)
        print(user_info)

        try:
            newest =  api.user_timeline(user_id=tw['user_id'], count=1)[0]
            total = diff = newest.author.statuses_count - tw['counter']

            bar = progressbar.ProgressBar(max_value=total)

            while diff > 0:
                # The maximum count = 200
                statuses =  api.user_timeline(user_id=tw['user_id'], since_id=tw['tweet_id'], max_id=newest.id, count=200)
                
                logfile("{} # List size: {}".format(user_info, len(statuses)))

                for st in statuses:
                    try:
                        # process_status(conn, st, False)
                        message = "{} > Inserted tweet {} - {} - {}".format(user_info, st.id, st.created_at, diff)
                    
                    except Exception as e:
                        message = "{} > ERROR to insert Tweet {}: {}".format(user_info, st.id, e)

                    bar.update(total-diff)
                    newest = st 
                    diff -= 1

                    logfile(message)
                    time.sleep(0.1)

        except Exception as e:
            logfile("{} > ERROR to get user timeline: {}".format(user_info, e))

        logfile(count, user_info, "< END")
        count -= 1
