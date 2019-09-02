import sys
import time
import tweepy
import datetime
import progressbar
from textblob import TextBlob

sys.path.append('./')
from helper.authenticate import api_tokens
from helper.db_connection import DbConnecion
from helper.log import logfile, print_and_log
from src.stream_listener import process_status, insert_new_user

# The API can only return up to 3,200 of a user's most recent Tweets
TWEETS_LIMIT = 3200
CONTROL_FLAG_LIMIT = 5
LOGNAME = "-recovery"

def period_recovery(conn, api):
    last_tweets = conn.last_tweets_list()

    count = len(last_tweets)
    for tw in last_tweets:

        user_info = " {0:<3} User: {1} - {2}".format(count, tw['user_id'], tw['user_name'])

        print_and_log(user_info, LOGNAME)

        control_flag = 0
        progress = 0

        try:
            if(tw['max_id'] is None):
                newest = api.user_timeline(user_id=tw['user_id'], count=1)[0]
                max_id = newest.id
                diff = max(0, (newest.author.statuses_count - tw['tweet_counter']))
                max_diff = TWEETS_LIMIT

            else:
                max_id = tw['max_id']-1
                diff = max(0, (tw['counter_max'] - tw['tweet_counter'] - tw['counter_diff']))
                max_diff = max(0, (TWEETS_LIMIT - tw['counter_diff']))
            
            diff = max_diff = min(diff, max_diff)
        
        except Exception as e:
            print_and_log("{} > ERROR while handling user timeline: {}".format(user_info, e), LOGNAME, "\n")
            count -= 1
            continue

        if(max_diff):
            bar = progressbar.ProgressBar(max_value=max_diff)

        while diff > 0:
            # The maximum count = 200
            statuses =  api.user_timeline(user_id=tw['user_id'], since_id=tw['tweet_id'], max_id=max_id, count=200)
            
            if(control_flag == CONTROL_FLAG_LIMIT):
                print_and_log("{} # Control flag limit reached ({})!".format(user_info, control_flag), LOGNAME, "\n")
                diff = 0
                continue

            logfile("{} # Tweets left: {} # List size: {}".format(user_info, diff, len(statuses)), LOGNAME)

            if(len(statuses) <= 1):
                control_flag += 1
            
            for st in statuses:
                try:
                    process_status(conn, st, False, False)
                    message = "{} > Inserted tweet {} - {} - {}".format(user_info, st.id, st.created_at, diff)
                
                except Exception as e:
                    message = "{} > ERROR to insert Tweet {}: {}".format(user_info, st.id, e)

                diff -= 1
                progress += 1
                max_id = st.id-1

                if(progress <= max_diff):
                    bar.update(progress)

                logfile(message, LOGNAME)

                time.sleep(0.1) # For each insertion

            time.sleep(5) # For each API request

        time.sleep(1) # For each user searched

        if(control_flag == CONTROL_FLAG_LIMIT or diff == 0):
            print_and_log("{} # It's Done! Maximum possible tweets retrived!".format(user_info), LOGNAME, "\n")

        count -= 1

def user_timeline_recovery(conn, api):
    all_users = api.friends_ids()
    inserted_users = conn.users_list()

    count = len(all_users)

    for user_id in all_users:
        # Initial information to start the collection
        try:
            control_flag = 0
            progress = 0

            newest = api.user_timeline(user_id=user_id, count=1)[0]
            max_id = newest.id
            max_diff = diff = min(newest.author.statuses_count, TWEETS_LIMIT)

            user_info = "> {} User: {} - {}".format(count, user_id, newest.author.name)

            print_and_log(user_info, LOGNAME)

        except Exception as e:
            user_info = "{} User: {}".format(count, user_id)
            print_and_log("{} > ERROR while handling user timeline: {}".format(user_info, e), LOGNAME, "\n")
            count -= 1
            continue

        # In case that the user has not been inserted
        if(user_id not in inserted_users.keys()):
            try:
                insert_new_user(conn, newest.author)
                message = "{} > Inserted new user!".format(user_info)
                inserted_users[user_id] = user_id
            
            except Exception as e:
                message = "{} > ERROR to insert user!".format(user_info)
                continue
            
            logfile(message, LOGNAME)

        # Start the progress bar if necessary
        if(max_diff):
            bar = progressbar.ProgressBar(max_value=max_diff)

        # Collet tweets until the difference be zero
        while diff > 0:
            # The maximum count allwed by Twitter is 200
            statuses =  api.user_timeline(user_id=user_id, max_id=max_id, count=200)
            
            # Controller to don't be trapped into only one user for so long
            if(control_flag == CONTROL_FLAG_LIMIT):
                message = "{} # Control flag limit ({}) reached!".format(user_info, control_flag)
                logfile(message, LOGNAME)
                
                diff = 0
                continue

            logfile("{} # Tweets left: {} # List size: {}".format(user_info, diff, len(statuses)), LOGNAME)

            diff = max(diff, len(statuses))

            if(len(statuses) <= 1):
                control_flag += 1
            
            # Process all tweets from the current block collected
            for st in statuses:
                try:
                    process_status(conn, st, False, False)
                    message = "{} > Inserted tweet {} - {} - {}".format(user_info, st.id, st.created_at, diff)
                
                except Exception as e:
                    message = "{} > ERROR to insert Tweet {}: {}".format(user_info, st.id, e)

                diff -= 1
                progress += 1
                max_id = st.id-1

                if(progress <= max_diff):
                    bar.update(progress)

                logfile(message, LOGNAME)

                time.sleep(0.1) # For each insertion

            time.sleep(5) # For each API request

        time.sleep(1) # For each user searched

        if(control_flag == CONTROL_FLAG_LIMIT or diff == 0):
            print_and_log(" {} # It's Done! Maximum possible tweets retrived!".format(user_info), LOGNAME, "\n")

        count -= 1

# COMPILE WITH: $ python3 tweet_recovery.py [--user]
# Before start this process for the first time, all tweets must have the column tweet_streamed filled with 1
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

    # Recovery user period of tweets (since and max id)
    if(len(sys.argv) < 2):
        period_recovery(conn, api)

    # Recovery all user timeline as possible
    else:
        user_timeline_recovery(conn, api)

    exit()
