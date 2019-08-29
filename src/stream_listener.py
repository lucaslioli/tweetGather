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
DELIMITER = "-" * 99
HALF_DELIMITER = ("-"*40)

# Override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # Extra variable myfriends_ids created in main
        if(status.author.id not in api.myfriends_ids):
            # Tweet skipped because it isn't from a friend account
            return True # Don't kill the stream
        
        try:
            conn = DbConnecion()
            process_status(conn, status)

            print("Date:", status.created_at)
            print("User:", status.author.screen_name)
            print("Text:", status.text[:99], "[...]")

            message = "INSERTED tweet {}, from author {}".format(status.id, status.author.name)
            print_and_log(message, LOGNAME)

        except Exception as e:
            message = "ERROR: While inserting tweet {} = {}".format(status.id, e)

            print_and_log(message, LOGNAME)
        
        print(DELIMITER)

        return True # Don't kill the stream

    def on_error(self, status_code):
        message = 'Encountered error with status code: ' + str(status_code)

        print_and_log(message, LOGNAME)
        print(DELIMITER)

        if status_code == 420:
            return False

        return True # Don't kill the stream

    def on_timeout(self):
        message = sys.stderr + 'Timeout...'

        print_and_log(message, LOGNAME)
        print(DELIMITER)

        return True # Don't kill the stream
    
    def on_limit(self):
        message = 'Rate Limit Exceeded, Sleep for 15 Mins'

        print_and_log(message, LOGNAME)
        print(DELIMITER)

        time.sleep(15 * 60)
        return True # Don't kill the stream
    
    # END

def process_status(conn, status, streamed = True, insert_user = True):
    if(insert_user):
        if(status.author.id not in conn.users_list().keys()):
            insert_new_user(conn, status.author)

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

    # END

def insert_new_user(conn, author):
    # Information related about the status' author
    user_insert = {}
    user_insert['id']            = author.id
    user_insert["name"]          = author.name
    user_insert["screen_name"]   = author.screen_name
    user_insert['friends_count'] = author.friends_count
    user_insert["lang"]          = author.lang

    # For now, all the users have already been inserted
    conn.insert_user(user_insert)

# Start the Stream Listener
def start_stream(query = None):
    
    while True:
        try:
            myStream = tweepy.streaming.Stream(api.auth, MyStreamListener())
            myStream.filter(follow=query)

        except Exception as e:
            message = "ERROR: Exeption occurred! {}".format(e)

            print_and_log(message, LOGNAME)
            print(DELIMITER)

            continue

        time.sleep(10)

        message = "{0} (RE)STARTING STREAMING {0}".format(HALF_DELIMITER)
        print_and_log(message, LOGNAME)
    
    # END

# COMPILE WITH: $ python3 stream_listener.py
if __name__ == '__main__':
    keys = api_tokens()
    # Obtenção das chaves de atenticação da API
    access_token        = keys['access_token']
    access_token_secret = keys['access_token_secret']
    consumer_key        = keys['consumer_key']
    consumer_secret     = keys['consumer_secret']

    # Autenticação com a API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Variable created to avoid multiple requests for friends ids
    api.myfriends_ids = api.friends_ids()
    api.myfriends_ids.append(api.me().id)

    # Users to stream
    query = list(map(str, api.myfriends_ids))

    # Added own account id to make tests
    query.append(str(api.me().id))

    print ("\nQuery being tracked =", query)

    message = "{0} STARTING STREAMING {0}".format(HALF_DELIMITER)
    print_and_log(message, LOGNAME)

    start_stream(query)

    # END