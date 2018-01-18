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
            tweet_id           = tweet["id"]
            tweet_text         = tweet["text"]
            tweet_datetime     = tweet["timestamp_ms"]
            tweet_language     = tweet["lang"]
            tweet_retweets     = tweet["retweet_count"]
            tweet_likes        = tweet["favorite_count"]
            tweet_replies      = tweet["reply_count"]
            tweet_replied_to   = tweet["in_reply_to_status_id"]
            tweet_polarity     = tweet["polarity"]
            tweet_subjectivity = tweet["subjectivity"]
            user_id            = tweet["user_id"]
            user_followers     = tweet["followers_count"]
            user_tweet_counter = tweet["statuses_count"]
            # user_ followers_diff = atomático por SQL

            with self.mysqlCon.cursor() as cur:
                sql = "SELECT `tweet_id` FROM `tweet` WHERE `tweet_id` = %s"

                cur.execute(sql, (tweet_id))
                
                result = cur.fetchone()

                cur.close()

                if(result is None):
                    with self.mysqlCon.cursor() as cur:
                        sql = "INSERT INTO tweet (tweet_id, tweet_text, tweet_datetime, tweet_language, tweet_retweets, tweet_likes, tweet_replies, tweet_replied_to, tweet_polarity, tweet_subjectivity, user_id, user_followers, user_tweet_counter, user_followers_diff) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, (SELECT %s-t1.user_followers FROM tweet t1 WHERE t1.user_id = %s ORDER BY t1.tweet_datetime DESC LIMIT 1))"
                        
                        cur.execute(sql, (tweet_id, tweet_text, tweet_datetime, tweet_language, tweet_retweets, tweet_likes, tweet_replies, tweet_replied_to, tweet_polarity, tweet_subjectivity, user_id, user_followers, user_tweet_counter, user_followers, user_id))
                        
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

    def tweet_list(self, where = ""):
        sql = "SELECT tweet_id as id, tweet_text as txt, tweet_language as lang FROM tweet " + where

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

        except ValueError:
            result = ValueError + 'EXEPTION occurred!'

        cur.close()

        return result