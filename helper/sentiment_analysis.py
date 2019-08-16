from helper.db_connection import DbConnecion
from textblob import TextBlob

conn = DbConnecion()

tweets = conn.tweet_list("WHERE tweet_polarity IS NULL")

i = len(tweets)

for tw in tweets:
    text = TextBlob(tw['txt'])

    if tw['lang'] != 'en':
        try:
            text = TextBlob(str(text.translate(to='en')))
        except:
            continue

    up = conn.update_sentiment(tw['id'], text.sentiment.polarity, text.sentiment.subjectivity)

    print('\nNº: {0} \n - Tweet: {1} \n - Update: {2} \n - {3}'.format(i, tw['id'], up, text.sentiment))

    i -= 1