import sys
import tweepy

from authenticate import api_tokens
from db_connection import DbConnecion

# Variables that contains the user credentials to access Twitter API
if(len(sys.argv) < 2):
    print ("Necessario passar o codigo de acesso e tambem o usuario seed.")
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
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # Pega o usuário da conta seed
        
    conn = DbConnecion()

    tweets = conn.tweet_list("")

    i = len(tweets)

    for tw in tweets:

        try:
            original = api.get_status(tw['id'])

            conn.update_tweet(tw['id'], original.created_at, original.retweet_count, original.favorite_count)

            print("\n", "Nº: ", i, tw['id'], "=>", original.created_at)
            print(" RTs: ", "=>", original.retweet_count)
            print(" Likes: ", "=>", original.favorite_count)
        
        except:
            conn.update_tweet(tw['id'], '')

            print("\n", "Nº: ", i, tw['id'], "=> NULL")

        i -= 1

    print("\n")
