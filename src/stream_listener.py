import sys
import tweepy
import datetime

from textblob import TextBlob

sys.path.append('./helper')
from authenticate import api_tokens
from db_connection import DbConnecion
from log import logfile

# Override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if(status.lang != 'en'):
            return False
        elif(status.author.followers_count < 10000):
            return False
        # elif(status.author.id not in api.friends_ids()):
        #     return False
        else:
            process_status(status)

        print("-----------------------------------------")
        print("Date:", status.created_at)
        print("User:", status.author.screen_name)
        print("Text:", api.get_status(status.id, tweet_mode='extended').full_text)
        # print("Followers:", status.author.followers_count)

        message = "INSERT tweet " + str(status.id) + " for user " + status.author.name
        logfile(message)

        return False; # Don't kill the stream

    def on_error(self, status_code):
        message = 'Encountered error with status code:' + str(status_code)

        print(sys.stderr, message)
        print("-----------------------------------------")
        logfile(message)

        if status_code == 420:
            return False

        return True # Don't kill the stream

    def on_timeout(self):
        message = sys.stderr + 'Timeout...'

        print(message)
        print("-----------------------------------------")
        logfile(message)

        return True # Don't kill the stream

def process_status(status):
    conn = DbConnecion()

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
    tweet_insert["id"]                    = status.id
    tweet_insert["text"]                  = status.text
    tweet_insert["created_at"]            = status.created_at
    tweet_insert["lang"]                  = status.lang
    tweet_insert["retweet_count"]         = status.retweet_count
    tweet_insert["favorite_count"]        = status.favorite_count
    tweet_insert["reply_count"]           = status.reply_count
    tweet_insert["in_reply_to_status_id"] = status.in_reply_to_status_id
    tweet_insert["for_elections"]         = 0

    tweet_insert["user_id"]         = status.author.id
    tweet_insert["followers_count"] = status.author.followers_count
    tweet_insert["statuses_count"]  = status.author.statuses_count

    # Get the sentiment polarity of the message
    text = TextBlob(status.text)

    # Try to translate the message
    if status.lang != 'en':
        try:
            text = TextBlob(str(text.translate(from_lang = status.lang, to='en')))
        except:
            message = "WARING: " + str(status.id) + "The text can not be translated."

            print("-----------------------------------------")
            print(message)
            logfile(message)
            print("-----------------------------------------")

    tweet_insert["polarity"]     = text.sentiment.polarity
    tweet_insert["subjectivity"] = text.sentiment.subjectivity

    # Insert the message into database
    conn.insert_tweet(tweet_insert)

# Start the Stream Listener
def start_stream(query):
    message = "---------- STARTING STREAMING -----------"

    print (message)
    logfile(message)

    while True:
        try:
            myStream = tweepy.streaming.Stream(api.auth, MyStreamListener())
            myStream.filter(track=query)

        except:
            message = 'ERROR: Exeption occurred!' + sys.exc_info()[1]

            print(message)
            print("-----------------------------------------")
            logfile(message)

            continue

if __name__ == '__main__': # COMPILE WITH: # python3 stream_listener.py CREDENTIALS
    if(len(sys.argv) < 2):
        print("You need to inform the user credentials to access.")
        exit(1)

    else:
        keys = api_tokens(sys.argv[1])
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

    query = [] # Query to filter bay de users screen name
    for friend in api.friends(count=99):
        query.append("@"+friend.screen_name)
        query.append(friend.screen_name)

    start_stream(query)