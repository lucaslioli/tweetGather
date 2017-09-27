import sys
import tweepy
import time
from authenticate import api_tokens

# Variables that contains the user credentials to access Twitter API
if(len(sys.argv) < 2):
	print ("You need to inform the user credentials to access.")
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

	api = tweepy.API(auth)

	#override tweepy.StreamListener to add logic to on_status
	class MyStreamListener(tweepy.StreamListener):

		def on_status(self, status):
			print(status.author.screen_name, "Favourites: "+str(status.favorite_count), "Retweets: "+str(status.retweet_count), "Replies: "+str(status.reply_count), status.created_at, status.text, "\n\n")

		def on_error(self, status_code):
			print >> sys.stderr, 'Encountered error with status code:', status_code
			return True # Don't kill the stream

		def on_timeout(self):
			print >> sys.stderr, 'Timeout...'
			return True # Don't kill the stream

	user  = api.me()
	
	follow_list = []
	for friend in user.friends():
		follow_list.append(str(friend.id))

	myStream = tweepy.streaming.Stream(auth, MyStreamListener())
	myStream.userstream(_with='followings')