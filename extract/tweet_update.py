import sys
import tweepy
import time

from authenticate import api_tokens
from db_connection import DbConnecion
from text_processing import text_cleaner
from dictionary import *


def calc_banality(text, lang):
    if(lang != 'en'):
        return {'100': -1, '1000':-1, '3000': -1}

    ban_100 = 0
    ban_1000 = 0
    ban_3000 = 0
    
    for word in text.split():
        if(word in commonwords_100()):
            ban_100 = +1

        if(word in commonwords_1000()):
            ban_1000 = +1

        if(word in commonwords_3000()):
            ban_3000 = +1

    counter = len(text.split())

    if(ban_100 != 0):
        ban_100 = ban_100/counter

    if(ban_1000 != 0):
        ban_1000 = ban_1000/counter

    if(ban_3000 != 0):
        ban_3000 = ban_3000/counter

    return {'100': ban_100, '1000':ban_1000, '3000': ban_3000}


# Variables that contains the user credentials to access Twitter API
if(len(sys.argv) < 2):
    print ("Necessario indicar a conta de autenticação!")
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

    # WHERE tweet_datetime BETWEEN DATE_SUB(NOW(), INTERVAL 15 DAY) AND NOW()
    # Para atualizar todos: WHERE deleted = 0
    tweets = conn.tweet_list("")

    i = len(tweets)

    for tw in tweets:

        try:
            # Search for the original tweet by id
            original = api.get_status(tw['id'])

            # Process de the tweet message to clean the text
            text_after = text_cleaner(original.text)

            # Extracts the banality from the text processed for english language tweets
            ban = calc_banality(text_after, original.lang)

            # Update the information recorded in database
            # conn.update_tweet(tw['id'], original.retweet_count, original.favorite_count, text_after, ban['100'], ban['1000'], ban['3000'])

            print("\n", "Nº: ", i, tw['id'], "=>", original.created_at)
            print(" RTs =>", original.retweet_count)
            print(" Likes =>", original.favorite_count)
            print(" Text 1 =>", original.text.replace('\n', ' ').replace('\r', ''))
            print(" Text 2 =>", text_after)
            print(" Lang => ", original.lang)
            print(" Banlity 100 =>", ban['100'], " | 1000 => ", ban['1000'], " | 3000 => ", ban['3000'])
            # print(" Replies: ", "=>", original.reply_count) # reply_count only for premium
        
        except:
            conn.update_tweet(tw['id'])

            print("\n", "Nº: ", i, tw['id'], " ERRO: ", sys.exc_info()[1])

        i -= 1
        time.sleep(0.5)

    print("\n")