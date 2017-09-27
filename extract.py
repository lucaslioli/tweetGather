import sys
import tweepy
import pymysql
import pymysql.cursors
import time
from authenticate import api_tokens

# Variables that contains the user credentials to access Twitter API
if(len(sys.argv) < 3):
	print ("Necessario passar o codigo de acesso e tambem o usuario seed.")
	exit(1)
else:
	keys = api_tokens(sys.argv[1])

	access_token 		= keys['access_token']
	access_token_secret = keys['access_token_secret']
	consumer_key 		= keys['consumer_key']
	consumer_secret 	= keys['consumer_secret']

	user_seed = sys.argv[2]

if __name__ == '__main__':
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	public_tweets = api.home_timeline()

	print ("\n\n>>>>>>> HOME TIMELINE TWEETS")
	i = 0
	for tweet in public_tweets:
		print ("\t" + str(i) + ". "+ str(tweet.id) + " == " + tweet.text)
		i += 1

	user = api.get_user(user_seed)
	print ("\n>>>>>>> USER SCREEN NAME: " + user.screen_name)
	print ("\n>>>>>>> USER FOLLOWERS COUNT: " + str(user.friends_count))

	print ("\n>>>>>>> USER FRIENDS SCREAN NAME")
	i = 0
	for friend in user.friends():
		print ("\t" + str(i) + ". " + friend.screen_name + "\t id- " + str(friend.id))
		i += 1