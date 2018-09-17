import sys
import tweepy
import datetime

from textblob import TextBlob
from authenticate import api_tokens
from db_connection import DbConnecion
from log import logfile

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        print("-----------------------------------------")
        print("Date:", status.created_at)
        print("User:", status.author.screen_name)
        print("Text:", status.text)

        conn = DbConnecion()

        user_insert = {}
        user_insert['id']            = status.author.id
        user_insert["name"]          = status.author.name
        user_insert["screen_name"]   = status.author.screen_name
        user_insert['friends_count'] = status.author.friends_count
        user_insert["lang"]          = status.author.lang

        conn.insert_user(user_insert)

        tweet_insert = {}
        tweet_insert["id"]                    = status.id
        tweet_insert["text"]                  = status.text
        tweet_insert["created_at"]            = status.created_at
        tweet_insert["lang"]                  = status.lang
        tweet_insert["retweet_count"]         = status.retweet_count
        tweet_insert["favorite_count"]        = status.favorite_count
        tweet_insert["reply_count"]           = status.reply_count
        tweet_insert["in_reply_to_status_id"] = status.in_reply_to_status_id
        tweet_insert["for_elections"]         = 1

        tweet_insert["user_id"]         = status.author.id
        tweet_insert["followers_count"] = status.author.followers_count
        tweet_insert["statuses_count"]  = status.author.statuses_count

        text = TextBlob(status.text)
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

        conn.insert_tweet(tweet_insert)

        message = "INSERT tweet " + str(status.id) + " for user " + status.author.name
        logfile(message)

        return True; # Don't kill the stream

    def on_error(self, status_code):
        message = 'Encountered error with status code:' + str(status_code)
        
        print(sys.stderr, message)
        print("-----------------------------------------")
        logfile(message)
        
        return True # Don't kill the stream

    def on_timeout(self):
        message = sys.stderr + 'Timeout...'

        print(message)
        print("-----------------------------------------")
        logfile(message)

        return True # Don't kill the stream

# Start the Stream Listener
def start_stream():
    message = "---------- STARTING STREAMING -----------"
    
    print (message)
    logfile(message)

    while True:
        try:
            myStream = tweepy.streaming.Stream(auth, MyStreamListener())
            myStream.filter(track=["Aldo Rebelo", "@aldorebelo", "Alvaro Dias", "@alvarodias_", "Ciro Gomes", "@cirogomes", "Cristovam Buarque", "@Sen_Cristovam", "José Maria Eymael", "@Eymaeloficial", "Fernando Collor", "@Collor", "Flavio Rocha", "@flaviogr", "Geraldo Alckmin", "@geraldoalckmin", "Guilherme Boulos", "@GuilhermeBoulos", "Henrique Meirelles", "@meirelles", "Jair Bolsonaro", "@jairbolsonaro", "João Amoêdo", "@joaoamoedonovo", "João Vicente Goulart", "@joaovgoulart64", "Levy Fidelix", "@levyfidelix", "Luiz Inácio Lula da Silva", "@LulapeloBrasil", "Manuela D'Ávila", "@ManuelaDavila", "Marina Silva", "@silva_marina", "Michel Temer", "@MichelTemer", "Paulo Rabello de Castro", "@PRabello", "Rodrigo Maia", "@RodrigoMaia", "Valéria Monteiro", "@mntvaleria", "Vera Lúcia", "@verapstu", "@77solidariedade", "@podemos_19", "@PDT_nacional", "@pps23", "@psdcnacional", "@PRB10", "@Rede45", "@psol50", "@MDB_Nacional", "@partidonovo30", "@PartidoPPL", "@prtboficial", "@ptbrasil", "@PCdoB_Oficial", "@pscnacional", "@democratas", "@pmn33nacional", "@pstu"])
        
        except:
            message = 'ERROR: Exeption occurred!' + sys.exc_info()[1]

            print(message)
            print("-----------------------------------------")
            logfile(message)
            
            continue

# Variables that contains the user credentials to access Twitter API
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

if __name__ == '__main__':
    # Autenticação com a API Tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Autenticação com a API
    api = tweepy.API(auth)

    start_stream()
