import sys
import tweepy
import datetime
import time
from textblob import TextBlob

sys.path.append('./')
from helper.authenticate import api_tokens
from helper.db_connection import DbConnecion
from helper.log import logfile, print_and_log

LOGNAME = "-stream"

# Override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        print("-----------------------------------------")

        if(status.author.id not in api.friends_ids()):
            message = "Tweet skipped: {} Author: {}".format(status.id, status.author.screen_name)
            print_and_log(message, LOGNAME)
            return False
        else:
            conn = DbConnecion()
            process_status(conn, status)

        print("Date:", status.created_at)
        print("User:", status.author.screen_name)
        print("Text:", api.get_status(status.id, tweet_mode='extended').full_text)
        # print("Followers:", status.author.followers_count)

        message = "INSERT tweet " + str(status.id) + " for user " + status.author.name
        logfile(message, LOGNAME)

        return False # Don't kill the stream

    def on_error(self, status_code):
        message = 'Encountered error with status code: ' + str(status_code)

        print_and_log(message, LOGNAME)
        print("-----------------------------------------")

        if status_code == 420:
            return False

        return True # Don't kill the stream

    def on_timeout(self):
        message = sys.stderr + 'Timeout...'

        print_and_log(message, LOGNAME)
        print("-----------------------------------------")

        return True # Don't kill the stream
    
    def on_limit(self):
        message = 'Rate Limit Exceeded, Sleep for 15 Mins'

        print_and_log(message, LOGNAME)
        print("-----------------------------------------")

        time.sleep(15 * 60)
        return True # Don't kill the stream

def process_status(conn, status, streamed = True, insert_user = True):
    if(insert_user):
        # Information related about the status' author
        user_insert = {}
        user_insert['id']            = status.author.id
        user_insert["name"]          = status.author.name
        user_insert["screen_name"]   = status.author.screen_name
        user_insert['friends_count'] = status.author.friends_count
        user_insert["lang"]          = status.author.lang

        # For now, all the users have already been inserted
        conn.insert_user(user_insert)

    # Information related about the status
    tweet_insert = {}
    tweet_insert["id"]              = status.id
    tweet_insert["text"]            = status.text
    tweet_insert["created_at"]      = status.created_at
    tweet_insert["lang"]            = status.lang
    tweet_insert["retweet_count"]   = status.retweet_count
    tweet_insert["favorite_count"]  = status.favorite_count
    tweet_insert["has_media"]       = 1 if 'media' in status.entities else 0
    tweet_insert["streamed"]        = 1 if streamed else 0

    tweet_insert["user_id"]         = status.author.id
    tweet_insert["followers_count"] = status.author.followers_count
    tweet_insert["statuses_count"]  = status.author.statuses_count

    # Get the sentiment polarity of the message
    text = TextBlob(status.text)

    tweet_insert["polarity"]     = text.sentiment.polarity
    tweet_insert["subjectivity"] = text.sentiment.subjectivity

    # Insert the message into database
    conn.insert_tweet(tweet_insert)

# Start the Stream Listener
def start_stream(query = None):
    message = "---------- STARTING STREAMING -----------"

    print_and_log(message, LOGNAME)

    if(query is None):
        query = list(map(str, api.friends_ids()))

    print ("Query being trackaed =", query)

    while True:
        try:
            myStream = tweepy.streaming.Stream(api.auth, MyStreamListener())
            myStream.filter(follow=query)

        except Exception as e:
            message = "ERROR: Exeption occurred! {}".format(e)

            print_and_log(message, LOGNAME)
            print("-----------------------------------------")

            continue

        time.sleep(10)

# COMPILE WITH: $ python3 stream_listener.py
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
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # query = [] # Query to filter by the user's screen name
    # for friend in api.friends(count=99):
    #     query.append("@"+friend.screen_name)
    #     query.append(friend.screen_name)

    start_stream()
