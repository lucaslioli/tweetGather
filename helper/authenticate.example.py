
def api_tokens():

	keys = {}

	keys['consumer_key'] 		= "xxxxxxxxxxxxxxxxxxxxxxxxx"
	keys['consumer_secret'] 	= "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
	keys['access_token'] 		= "xxxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
	keys['access_token_secret'] = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

	return keys

def db_connection_data():

	conn = {}

	conn['host']    	= '127.0.0.1',
	conn['user']    	= 'root',
	conn['password']	= '',
	conn['db']      	= 'tweetgather',
	conn['charset'] 	= 'utf8mb4',
	
	return conn