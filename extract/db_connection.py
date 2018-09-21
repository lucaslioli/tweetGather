import sys
import pymysql
import pymysql.cursors

class DbConnecion(object):

    mysqlCon = pymysql.connect(
        host        = '127.0.0.1', 
        user        = 'root', 
        password    = '', 
        db          = 'tweetgather', 
        charset     = 'utf8mb4', 
        cursorclass = pymysql.cursors.DictCursor
    )

    def insert_user(self, user):
        if 'id' in user:
            user_id          = user["id"]
            user_name        = user["name"]
            user_screen_name = user["screen_name"]
            user_following   = user["friends_count"]
            user_language    = user["lang"]

            with self.mysqlCon.cursor() as cur:
                sql = "SELECT `user_id` FROM `user` WHERE `user_id` = %s"
                
                cur.execute(sql, (user_id))
                
                result = cur.fetchone()

                cur.close()

                if(result is None):
                    with self.mysqlCon.cursor() as cur:
                        sql = "INSERT INTO user (user_id, user_name, user_screen_name, user_following, user_language) VALUES (%s, %s, %s, %s, %s)"

                        cur.execute(sql, (user_id, user_name, user_screen_name, user_following, user_language))
                        
                        self.mysqlCon.commit()

                        cur.close()

            return True

        else: 
            return False

    def insert_tweet(self, tweet):
        if 'id' in tweet:
            tweet_id            = tweet["id"]
            tweet_text          = tweet["text"]
            tweet_datetime      = tweet["created_at"]
            tweet_language      = tweet["lang"]
            tweet_retweets      = tweet["retweet_count"]
            tweet_likes         = tweet["favorite_count"]
            tweet_replies       = tweet["reply_count"]
            tweet_replied_to    = tweet["in_reply_to_status_id"]
            tweet_polarity      = round(tweet["polarity"], 6)
            tweet_subjectivity  = round(tweet["subjectivity"], 6)
            tweet_url           = 0 if tweet_text.find('http') == -1 else 1
            tweet_hashtag       = 0 if tweet_text.find('#') == -1 else 1
            tweet_RT            = 0 if tweet_text.find('RT', 0, 2) == -1 else 1
            tweet_size          = len(tweet_text)
            tweet_for_elections = tweet["for_elections"]
            user_id = tweet["user_id"]
            # user_ followers_diff = atomático por SQL

            with self.mysqlCon.cursor() as cur:
                sql = "SELECT `tweet_id` FROM `tweet` WHERE `tweet_id` = %s"

                cur.execute(sql, (tweet_id))
                
                result = cur.fetchone()

                cur.close()

                if(result is None):
                    with self.mysqlCon.cursor() as cur:
                        sql = "INSERT INTO tweet (tweet_id, tweet_text, tweet_datetime, tweet_language, tweet_retweets, tweet_likes, tweet_replies, tweet_replied_to, tweet_polarity, tweet_subjectivity, tweet_url, tweet_hashtag, tweet_RT, tweet_size, tweet_for_elections, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                        cur.execute(sql, (tweet_id, tweet_text, tweet_datetime, tweet_language, tweet_retweets, tweet_likes, tweet_replies, tweet_replied_to, tweet_polarity, tweet_subjectivity, tweet_url, tweet_hashtag, tweet_RT, tweet_size, tweet_for_elections, user_id))
                        
                        self.mysqlCon.commit()

                        cur.close()

                return True

        else: 
            return False

    def insert_user_followers_history(self, user):
        if 'id' in user:
            user_id          = user["id"]
            user_followers   = user["followers_count"]
            # user_ followers_diff = atomático por SQL
            # date_time = automático por SQL

            with self.mysqlCon.cursor() as cur:
                sql = "INSERT INTO user_followers_history (user_id, user_followers, difference, date_time) VALUES (%s, %s, (SELECT %s-u1.user_followers FROM user_followers_history u1 WHERE u1.user_id = %s ORDER BY u1.date_time DESC LIMIT 1), NOW())"
                
                cur.execute(sql, (user_id, user_followers, user_followers, user_id))
                
                self.mysqlCon.commit()

                cur.close()

        else: 
            return False

    def tweet_list(self, where = ''):
        sql = "SELECT tweet_id as id, tweet_text as txt, tweet_language as lang, tweet_retweets as retweets, tweet_likes as likes, deleted FROM tweet " + where

        cur = self.mysqlCon.cursor()

        cur.execute(sql)
        
        result = cur.fetchall()

        cur.close()

        return result

    def update_sentiment(self, tweet_id, polarity, subjectivity):
        sql = "UPDATE tweet SET tweet_polarity = %s, tweet_subjectivity = %s WHERE tweet_id = %s"

        cur = self.mysqlCon.cursor()

        try:
            cur.execute(sql, (polarity, subjectivity, tweet_id))

            self.mysqlCon.commit()

            result = "Ok"

        except:
            result = 'EXEPTION occurred!' + str(sys.exc_info()[1])
            print(result)

        cur.close()

        return result

    def update_tweet(self, tweet_id, deleted = 0, retweets = -1, likes = -1, text_after = '', ban_100 = -1, ban_1000 = -1, ban_3000 = -1):
            
        sql = "UPDATE tweet SET deleted = %s, tweet_retweets = %s, tweet_likes = %s, tweet_text_after = %s, tweet_ban_100 = %s, tweet_ban_1000 = %s, tweet_ban_3000 = %s WHERE tweet_id = %s"

        cur = self.mysqlCon.cursor()

        try:
            cur.execute(sql, (deleted, retweets, likes, text_after, ban_100, ban_1000, ban_3000, tweet_id))
            
            self.mysqlCon.commit()

            result = "Ok"

        except:
            result = 'EXEPTION occurred!' + str(sys.exc_info()[1])

        cur.close()

        return result

    def auto_update_tweet(self):
        cur = self.mysqlCon.cursor()

        print("Updating usage of URLs...")
        # cur.execute("UPDATE tweet AS t SET t.tweet_url = 0 WHERE t.tweet_text NOT LIKE '%http%'")
        # cur.execute("UPDATE tweet AS t SET t.tweet_url = 1 WHERE t.tweet_text LIKE '%http%'")

        self.mysqlCon.commit()

        cur.close()


    def tweets_attr(self, rate, conf=0):
        sql = """SELECT 
                    t.tweet_text_after as txt,
                    IF(t.tweet_polarity IS NOT NULL, CAST(t.tweet_polarity AS DEC(4,2)), 0.00) AS polarity,
                    IF(t.tweet_url = 1, 'yes', 'no') as url, 
                    IF(t.tweet_hashtag = 1, 'yes', 'no') as hashtag, 
                    IF(t.tweet_RT = 1, 'yes', 'no') as RT, 
                    t.tweet_size,
                    IF(t.tweet_ban_3000 IS NOT NULL, CAST(t.tweet_ban_3000 AS DEC(4,2)), 0.00) AS banality,
                    IF(((t.tweet_likes+t.tweet_retweets)/t.user_followers*100)>%s, 'yes', 'no') as popular
                from tweet as t 
                where t.tweet_language = 'en' and tweet_text_after is not null"""

        if(conf):
            sql = "SELECT popular, count(*) as count from (" + sql + ") as test group by popular"

        cur = self.mysqlCon.cursor()

        cur.execute(sql, rate)
        
        result = cur.fetchall()

        cur.close()

        return result