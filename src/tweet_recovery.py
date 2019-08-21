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

# The API can only return up to 3,200 of a user's most recent Tweets
TWEETS_LIMIT = 3200
CONTROL_FLAG_LIMIT = 5

def print_and_log(message, newline = "\n"):
    logfile(message)
    print(message, newline)

# COMPILE WITH: $ python3 tweet_recovery.py
# Before start this process, all tweets must have the column tweet_streamed filled with 1
if __name__ == '__main__':
    keys = api_tokens()

    # Obtaining API access keys and tokens
    access_token        = keys['access_token']
    access_token_secret = keys['access_token_secret']
    consumer_key        = keys['consumer_key']
    consumer_secret     = keys['consumer_secret']

    # Tweepy API authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # API authentication
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    conn = DbConnecion()

    last_tweets = conn.last_tweets_list()

    count = len(last_tweets)
    for tw in last_tweets:

        user_info = "{} User: {} - {}".format(count, tw['user_id'], tw['user_name'])

        print_and_log(user_info, "")

        control_flag = 0

        try:
            if(tw['max_id'] is None):
                newest = api.user_timeline(user_id=tw['user_id'], count=1)[0]
                max_id = newest.id
                diff = newest.author.statuses_count - tw['tweet_counter']
                max_diff = TWEETS_LIMIT
            else:
                max_id = tw['max_id']-1
                diff = max(0, (tw['counter_max'] - tw['tweet_counter'] - tw['counter_diff']))
                max_diff = max(0, (TWEETS_LIMIT - tw['counter_diff']))
            
            diff = max_diff = min(diff, max_diff)

            if(max_diff):
                bar = progressbar.ProgressBar(max_value=max_diff)

            while diff > 0:
                # The maximum count = 200
                statuses =  api.user_timeline(user_id=tw['user_id'], since_id=tw['tweet_id'], max_id=max_id, count=200)
                
                if(control_flag == CONTROL_FLAG_LIMIT):
                    print_and_log("{} # Control flag limit reached ({})!".format(user_info, control_flag))
                    diff = 0
                    continue

                logfile("{} # Tweets left: {} # List size: {}".format(user_info, diff, len(statuses)))

                if(len(statuses) <= 1):
                    control_flag += 1
                
                for st in statuses:
                    try:
                        process_status(conn, st, False, False)
                        message = "{} > Inserted tweet {} - {} - {}".format(user_info, st.id, st.created_at, diff)
                    
                    except Exception as e:
                        message = "{} > ERROR to insert Tweet {}: {}".format(user_info, st.id, e)

                    diff -= 1
                    max_id = st.id-1
                    bar.update(max_diff-diff-1)

                    logfile(message)

                    time.sleep(0.1) # For each insertion

                time.sleep(5) # For each API request

            time.sleep(1) # For each user searched

        except Exception as e:
            print_and_log("{} > ERROR while handling user timeline: {}".format(user_info, e))
            count -= 1
            continue

        if(control_flag == CONTROL_FLAG_LIMIT):
            print_and_log("{} # It's Done! Maximum possible tweets retrived!".format(user_info))

        count -= 1

    exit()
