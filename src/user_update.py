import sys
import tweepy

sys.path.append('./')
from helper.authenticate import api_tokens
from helper.db_connection import DbConnection

DELIMITER = "-" * 99

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

    conn = DbConnection()

    users = conn.users_list()
    i = len(users)

    for user_id in users.keys():
        try:
            user = api.get_user(user_id)

            info = {}
            info['following'] = user.friends_count
            info['followers'] = user.followers_count
            info['lang'] = user.lang
            info['created_at'] = user.created_at
            info['location'] = user.location
            info['description'] = user.description

            cur = conn.update_user(user_id, info)

            print("\n Nº: {} \n Result: {}".format(i, cur))
            print(" User: {} - {}".format(user.name, user_id))
            print("\n Created at:", user.created_at)
            print(" Location:", user.location)
            print(" Description:", user.description[:99])
            print("\n {}".format(DELIMITER))
        
        except Exception as e:
            print("\n Nº:", i)
            print(" User: {} - {}".format(users[user_id], user_id))
            print(" > ERROR while tried to get user information:", e)
            print("\n {}".format(DELIMITER))

        i -= 1        

    exit()
