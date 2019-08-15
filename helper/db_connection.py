import sys
import pymysql
import pymysql.cursors

class DbConnecion(object):

    mysqlCon = pymysql.connect(
        host        = '127.0.0.1',
        user        = 'root',
        password    = '321',
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
                        sql = """INSERT INTO tweet (tweet_id, tweet_text, tweet_datetime, tweet_language, tweet_retweets, tweet_likes, tweet_replies, tweet_replied_to, tweet_polarity, tweet_subjectivity, tweet_url, tweet_hashtag, tweet_RT, tweet_size, tweet_for_elections, user_id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

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
                sql = """INSERT INTO user_followers_history (user_id, user_followers, date_time, difference) 
                        VALUES (%s, %s, NOW(),
                            (SELECT %s-u1.user_followers 
                            FROM user_followers_history u1 
                            WHERE u1.user_id = %s 
                            ORDER BY u1.date_time DESC 
                            LIMIT 1))"""

                cur.execute(sql, (user_id, user_followers, user_followers, user_id))
                self.mysqlCon.commit()
                cur.close()

        else:
            return False

    def tweet_list(self, where = ''):
        sql = """SELECT tweet_id as id, tweet_text as txt, tweet_language as lang, tweet_retweets as retweets, tweet_likes as likes, deleted 
                FROM tweet """ + where

        cur = self.mysqlCon.cursor()

        cur.execute(sql)
        result = cur.fetchall()
        cur.close()

        return result

    def last_tweets_list(self):
        sql = """SELECT u.user_id, u.user_name, t.tweet_id, t.user_tweet_counter
                FROM tweet as t
                JOIN user as u on u.user_id = t.user_id
                WHERE tweet_id in (select MAX(t2.tweet_id) from tweet as t2 group by t2.user_id)
                GROUP BY user_id"""

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

    def update_tweet(self, tweet_id, deleted=0, retweets=-1, likes=-1, text='', text_after='', ban_100=-1, ban_1000=-1, ban_3000=-1):

        sql = """UPDATE tweet SET 
                    deleted = %s, 
                    tweet_retweets = %s, 
                    tweet_likes = %s, 
                    tweet_text = %s, 
                    tweet_text_after = %s, 
                    tweet_ban_100 = %s, 
                    tweet_ban_1000 = %s, 
                    tweet_ban_3000 = %s 
                WHERE tweet_id = %s"""

        cur = self.mysqlCon.cursor()

        try:
            cur.execute(sql, (deleted, retweets, likes, text, text_after, ban_100, ban_1000, ban_3000, tweet_id))
            self.mysqlCon.commit()
            result = "Ok"

        except:
            result = 'EXEPTION occurred!' + str(sys.exc_info()[1])

        cur.close()

        return result

    def auto_update_tweet(self):
        cur = self.mysqlCon.cursor()

        try:
            print("Updating tweet text to remove the borring emoji...")
            cur.execute("UPDATE tweet SET tweet_text_after = REPLACE(tweet_text_after, '⃣', '') WHERE tweet_text_after like '%⃣%'")

            print("Updating usage of URLs...")
            cur.execute("UPDATE tweet AS t SET t.tweet_url = 0 WHERE t.tweet_text NOT LIKE '%http%'")
            cur.execute("UPDATE tweet AS t SET t.tweet_url = 1 WHERE t.tweet_text LIKE '%http%'")

            print("Updating usage of Hashtags...")
            cur.execute("UPDATE tweet SET tweet_hashtag = 0 WHERE tweet_text NOT LIKE '%#%'")
            cur.execute("UPDATE tweet SET tweet_hashtag = 1 WHERE tweet_text LIKE '%#%'")

            print("Updating tweets when they are retweets...")
            cur.execute("UPDATE tweet SET tweet_RT = 0 WHERE tweet_text NOT LIKE 'RT @%'")
            cur.execute("UPDATE tweet SET tweet_RT = 1 WHERE tweet_text LIKE 'RT @%'")

            print("Updating the size range of each message...")
            cur.execute("UPDATE tweet SET tweet_size = 0 WHERE LENGTH(tweet_text) = 0")
            cur.execute("UPDATE tweet SET tweet_size = 10 WHERE LENGTH(tweet_text) <= 10 AND LENGTH(tweet_text) > 0")
            cur.execute("UPDATE tweet SET tweet_size = 20 WHERE LENGTH(tweet_text) <= 20 AND LENGTH(tweet_text) > 10")
            cur.execute("UPDATE tweet SET tweet_size = 30 WHERE LENGTH(tweet_text) <= 30 AND LENGTH(tweet_text) > 20")
            cur.execute("UPDATE tweet SET tweet_size = 40 WHERE LENGTH(tweet_text) <= 40 AND LENGTH(tweet_text) > 30")
            cur.execute("UPDATE tweet SET tweet_size = 50 WHERE LENGTH(tweet_text) <= 50 AND LENGTH(tweet_text) > 40")
            cur.execute("UPDATE tweet SET tweet_size = 60 WHERE LENGTH(tweet_text) <= 60 AND LENGTH(tweet_text) > 50")
            cur.execute("UPDATE tweet SET tweet_size = 70 WHERE LENGTH(tweet_text) <= 70 AND LENGTH(tweet_text) > 60")
            cur.execute("UPDATE tweet SET tweet_size = 80 WHERE LENGTH(tweet_text) <= 80 AND LENGTH(tweet_text) > 70")
            cur.execute("UPDATE tweet SET tweet_size = 90 WHERE LENGTH(tweet_text) <= 90 AND LENGTH(tweet_text) > 80")
            cur.execute("UPDATE tweet SET tweet_size = 100 WHERE LENGTH(tweet_text) <= 100 AND LENGTH(tweet_text) > 90")
            cur.execute("UPDATE tweet SET tweet_size = 110 WHERE LENGTH(tweet_text) <= 110 AND LENGTH(tweet_text) > 100")
            cur.execute("UPDATE tweet SET tweet_size = 120 WHERE LENGTH(tweet_text) <= 120 AND LENGTH(tweet_text) > 110")
            cur.execute("UPDATE tweet SET tweet_size = 130 WHERE LENGTH(tweet_text) <= 130 AND LENGTH(tweet_text) > 120")
            cur.execute("UPDATE tweet SET tweet_size = 140 WHERE LENGTH(tweet_text) <= 140 AND LENGTH(tweet_text) > 130")
            cur.execute("UPDATE tweet SET tweet_size = 150 WHERE LENGTH(tweet_text) <= 150 AND LENGTH(tweet_text) > 140")
            cur.execute("UPDATE tweet SET tweet_size = 160 WHERE LENGTH(tweet_text) <= 160 AND LENGTH(tweet_text) > 150")
            cur.execute("UPDATE tweet SET tweet_size = 170 WHERE LENGTH(tweet_text) <= 170 AND LENGTH(tweet_text) > 160")
            cur.execute("UPDATE tweet SET tweet_size = 180 WHERE LENGTH(tweet_text) <= 180 AND LENGTH(tweet_text) > 170")
            cur.execute("UPDATE tweet SET tweet_size = 190 WHERE LENGTH(tweet_text) <= 190 AND LENGTH(tweet_text) > 180")
            cur.execute("UPDATE tweet SET tweet_size = 200 WHERE LENGTH(tweet_text) <= 200 AND LENGTH(tweet_text) > 190")
            cur.execute("UPDATE tweet SET tweet_size = 210 WHERE LENGTH(tweet_text) <= 210 AND LENGTH(tweet_text) > 200")
            cur.execute("UPDATE tweet SET tweet_size = 210 WHERE LENGTH(tweet_text) <= 210 AND LENGTH(tweet_text) > 210")
            cur.execute("UPDATE tweet SET tweet_size = 230 WHERE LENGTH(tweet_text) <= 230 AND LENGTH(tweet_text) > 220")
            cur.execute("UPDATE tweet SET tweet_size = 240 WHERE LENGTH(tweet_text) <= 240 AND LENGTH(tweet_text) > 230")
            cur.execute("UPDATE tweet SET tweet_size = 250 WHERE LENGTH(tweet_text) <= 250 AND LENGTH(tweet_text) > 240")
            cur.execute("UPDATE tweet SET tweet_size = 255 WHERE LENGTH(tweet_text) <= 255 AND LENGTH(tweet_text) > 250")

            self.mysqlCon.commit()

        except:
            print('EXEPTION occurred! ' + str(sys.exc_info()[1]))

        cur.close()

    def tweets_attr(self, rate, user=0, counter=0):
        sql = """SELECT
                    t.tweet_text_after as txt,
                    IF(t.tweet_polarity IS NOT NULL, CAST(t.tweet_polarity AS DEC(4,2)), 0.00) AS polarity,
                    IF(t.tweet_url = 1, 1, 0) as url,
                    IF(t.tweet_hashtag = 1, 1, 0) as hashtag,
                    IF(t.tweet_RT = 1, 1, 0) as RT,
                    t.tweet_size,
                    IF(t.tweet_ban_3000 IS NOT NULL, CAST(t.tweet_ban_3000 AS DEC(4,2)), 0.00) AS banality,
                    IF(((t.tweet_likes+t.tweet_retweets)/t.user_followers*100)>%s, 1, 0) as popular
                FROM tweet as t
                WHERE t.tweet_language = 'en'
                    AND tweet_text_after != ''
                    AND user_followers > 10000"""

        if(user != 0):
            sql = sql + " AND t.user_id = %s "

        if(counter):
            sql = "SELECT popular, count(*) as count from (" + sql + ") as test group by popular order by popular"

        cur = self.mysqlCon.cursor()

        if(user != 0):
            cur.execute(sql, (rate, user))
        else:
            cur.execute(sql, rate)

        result = cur.fetchall()

        cur.close()

        return result