# Daily extraction of the number and variation of user's followers by crontab
# 30 19 * * * python3 /var/www/html/tweetGather/extract/basic_extraction.py Gather

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
	access_token 		= keys['access_token']
	access_token_secret = keys['access_token_secret']
	consumer_key 		= keys['consumer_key']
	consumer_secret 	= keys['consumer_secret']

if __name__ == '__main__':
	# Autenticação com a API Tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# Autenticação com a API
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	# Pega o usuário da conta seed
	user  = api.me()

	conn = DbConnecion()

	print ("\n>>>>>>> USERS FOLLOWED AND THEIR FOLLOWERS")
	for friend in user.friends():
		user_insert = {}
		user_insert['id'] = friend.id
		user_insert['followers_count'] = friend.followers_count
		user_insert["name"] = friend.name
		user_insert["screen_name"] = friend.screen_name
		user_insert["friends_count"] = friend.friends_count
		user_insert["lang"] = friend.lang

		
		conn.insert_user(user_insert)
		conn.insert_user_followers_history(user_insert)

		print ("----------------------------------------")
		print ("\tID: " + str(friend.id))
		print ("\tName: " + friend.name)
		print ("\tFollowers: " + str(friend.followers_count))
