"""
Update tweets information, based on a query set in a constant.

COMPILE WITH: $ python3 tweet_update.py [-api]

[-api]: Set to make a complete update using Twitter API.
        If not specified, automatic statistics update is performed.

"""

import sys
import tweepy
import time

sys.path.append('./')
from helper.authenticate import api_tokens
from helper.db_connection import DbConnection
from helper.text_processing import text_cleaner
from helper.dictionary import *

# Opt1: WHERE tweet_datetime BETWEEN DATE_SUB(NOW(), INTERVAL 15 DAY) AND NOW()
# Opt2: WHERE tweet_language = 'en'
QUERY = "WHERE tweet_language = 'en'"
DELIMITER = "-" * 99


def calc_banality(text, lang):
    if(lang != 'en'):
        return {'100': -1, '1000': -1, '3000': -1}

    ban_100 = 0
    ban_1000 = 0
    ban_3000 = 0

    for word in text.split():
        if(word in commonwords_100()):
            ban_100 += 1

        if(word in commonwords_1000()):
            ban_1000 += 1

        if(word in commonwords_3000()):
            ban_3000 += 1

    counter = len(text.split())

    if(ban_100 != 0):
        ban_100 = ban_100/counter

    if(ban_1000 != 0):
        ban_1000 = ban_1000/counter

    if(ban_3000 != 0):
        ban_3000 = ban_3000/counter

    return {'100': ban_100, '1000': ban_1000, '3000': ban_3000}


if __name__ == '__main__':

    conn = DbConnection()

    # Auto update without uses Twitter API
    if len(sys.argv) < 2:
        try:
            tweets = conn.tweet_list(QUERY)

            print("Cleaning and updating all the messages...")
            for tw in tweets:
                # Process de the tweet message to clean the text
                new_text = text_cleaner(tw['txt'])

                cur = conn.update_tweet_new_text(tw['id'], new_text)

            conn.auto_update_tweet()

            print("End.")

        except:
            print('EXCEPTION: ', str(sys.exc_info()[1]))

        exit()

    # Complete update
    else:
        keys = api_tokens()

        # API keys
        access_token = keys['access_token']
        access_token_secret = keys['access_token_secret']
        consumer_key = keys['consumer_key']
        consumer_secret = keys['consumer_secret']

    # Tweepy API authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    print("UPDATING TWEETS \nSEARCHING: {} \n {}".format(QUERY, DELIMITER))

    # Return a list with all tweets in the base
    tweets = conn.tweet_list(QUERY)

    i = len(tweets)

    for tw in tweets:
        try:
            # Search for the original status by id
            st = api.get_status(tw['id'], tweet_mode='extended')

            # Process de the tweet message to clean the text
            new_text = text_cleaner(st.full_text)

            # Extracts the banality from the text processed for english tweets
            ban = calc_banality(new_text, tw['lang'])

            # Check if the tweet has media content or not
            has_media = 1 if 'media' in st.entities else 0

            # Update the information recorded in database
            cur = conn.update_tweet(tw['id'], 0, has_media, st.retweet_count,
                                    st.favorite_count, st.full_text, new_text,
                                    ban['100'], ban['1000'], ban['3000'])

            print("\n Nº: {} \n Result: {}".format(i, cur))
            print("\n Id: {} ".format(tw['id']))
            print(" RTs: {} | Likes: {} | Has media: {}".format(
                st.retweet_count, st.favorite_count, has_media))

        except:
            new_text = text_cleaner(tw['txt'])
            ban = calc_banality(new_text, tw['lang'])

            cur = conn.update_tweet(tw['id'], 1, 0, tw['retweets'],
                                    tw['likes'], tw['txt'], new_text,
                                    ban['100'], ban['1000'], ban['3000'])

            print("\n {} \n Result: {} \n ERRO: {} ".format(i, cur,
                  sys.exc_info()[1]))
            print("\n Id: {} ".format(tw['id']))
            print(" RTs: {} | Likes: {}\n".format(tw['retweets'], tw['likes']))

        print(" Banlity 100 => {} | 1000 => {} | 3000 => {} \n".format(
              ban['100'], ban['1000'], ban['3000']))
        print("  Language =>", tw['lang'])
        print(" Full Text =>", tw['txt'].replace('\n', ' ').replace('\r', ''))
        print("  New Text =>", new_text)
        print("\n", DELIMITER)

        i -= 1
        time.sleep(0.5)
    exit()

    # Updates using only SQL
    conn.auto_update_tweet()

    exit()
