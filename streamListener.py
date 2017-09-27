import sys
import tweepy
from authenticate import api_tokens

# Variables that contains the user credentials to access Twitter API
if(len(sys.argv) < 3):
	print ("You need to inform the user credentials to access.")
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

	#override tweepy.StreamListener to add logic to on_status
	class MyStreamListener(tweepy.StreamListener):

		def on_status(self, status):
			print(status.author.screen_name, status.created_at, status.text)

		def on_error(self, status_code):
			print >> sys.stderr, 'Encountered error with status code:', status_code
			return True # Don't kill the stream

		def on_timeout(self):
			print >> sys.stderr, 'Timeout...'
			return True # Don't kill the stream

	myStream = tweepy.streaming.Stream(auth, MyStreamListener())
	myStream.filter(track=['neymar'])

	return True