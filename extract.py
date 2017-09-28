import sys
import tweepy
from authenticate import api_tokens

# Variables that contains the user credentials to access Twitter API
if(len(sys.argv) < 2):
	print ("Necessario passar o codigo de acesso e tambem o usuario seed.")
	exit(1)
else:
	keys = api_tokens(sys.argv[1])

	access_token 		= keys['access_token']
	access_token_secret = keys['access_token_secret']
	consumer_key 		= keys['consumer_key']
	consumer_secret 	= keys['consumer_secret']

if __name__ == '__main__':
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	user  = api.me()

	print ("\n>>>>>>> USERS FOLLOWED AND THEIR FOLLOWERS")
	for friend in user.friends():
		print ("----------------------------------------")
		print ("\tID: " + str(friend.id))
		print ("\tName: " + friend.name)
		print ("\tScreen Name: " + friend.screen_name)
		print ("\tFollowers: " + str(friend.followers_count))
		print ("\tFollowing:" + str(friend.friends_count))
		print ("\tLanguage: " + str(friend.lang))