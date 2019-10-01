import sys
import pymysql
import pymysql.cursors


class DbConnection(object):

    # # # # # # # # # # # # # # # # CONNECTION # # # # # # # # # # # # # # # #
    def __init__(self):
        try:
            self.mysqlCon = pymysql.connect(
                host        = '127.0.0.1',
                user        = 'root',
                password    = '321',
                db          = 'tweetgather',
                charset     = 'utf8mb4',
                cursorclass = pymysql.cursors.DictCursor
            )
        except Exception as e:
            print("Não foi possível estabelecer conexão com o banco!\
                \nERROR:", str(e))
            exit()

    # # # # # # # # # # # # # # # WRITE OPERATIONS # # # # # # # # # # # # # #

    def insert_user(self, user):
        if 'id' in user:
            user_id          = user["id"]
            user_name        = user["name"]
            user_screen_name = user["screen_name"]
            user_following   = user["friends_count"]
            user_language    = user["lang"]

            with self.mysqlCon.cursor() as cur:
                sql = """INSERT INTO user (user_id, user_name,
                        user_screen_name, user_following, user_language)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE user_id = user_id"""

                cur.execute(sql, (user_id, user_name, user_screen_name,
                                  user_following, user_language))

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
            tweet_media         = tweet['has_media']
            tweet_streamed      = tweet['streamed']
            tweet_polarity      = round(tweet["polarity"], 6)
            tweet_subjectivity  = round(tweet["subjectivity"], 6)
            tweet_url           = 0 if tweet_text.find('http') == -1 else 1
            tweet_hashtag       = 0 if tweet_text.find('#') == -1 else 1
            tweet_RT            = 0 if tweet_text.find('RT', 0, 2) == -1 else 1
            tweet_size          = len(tweet_text)

            user_id             = tweet["user_id"]
            user_tweet_counter  = tweet["statuses_count"]
            user_followers  = tweet["followers_count"]

            with self.mysqlCon.cursor() as cur:
                sql = "SELECT `tweet_id` FROM `tweet` WHERE `tweet_id` = %s"

                cur.execute(sql, (tweet_id))
                result = cur.fetchone()
                cur.close()

                if(result is None):
                    with self.mysqlCon.cursor() as cur:
                        sql = """INSERT INTO tweet (tweet_id, tweet_text,
                            tweet_datetime, tweet_language, tweet_retweets,
                            tweet_likes, tweet_polarity, tweet_subjectivity,
                            tweet_url, tweet_hashtag, tweet_media,
                            tweet_streamed, tweet_RT, tweet_size, user_id,
                            user_tweet_counter, user_followers)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE tweet_id=tweet_id"""

                        cur.execute(sql, (tweet_id, tweet_text, tweet_datetime,
                                          tweet_language, tweet_retweets,
                                          tweet_likes, tweet_polarity,
                                          tweet_subjectivity, tweet_url,
                                          tweet_hashtag, tweet_media,
                                          tweet_streamed, tweet_RT, tweet_size,
                                          user_id, user_tweet_counter,
                                          user_followers))

                        self.mysqlCon.commit()
                        cur.close()

                return True

        else:
            return False

    def update_tweet(self, tweet_id, deleted=0, media=0, retweets=-1, likes=-1,
                     text='', text_after='', ban_100=-1, ban_1k=-1, ban_3k=-1):

        sql = """UPDATE tweet SET deleted = %s, tweet_media = %s,
                    tweet_retweets = %s, tweet_likes = %s,
                    tweet_text = %s, tweet_text_after = %s,
                    tweet_ban_100 = %s, tweet_ban_1000 = %s,
                    tweet_ban_3000 = %s
                WHERE tweet_id = %s"""

        cur = self.mysqlCon.cursor()

        try:
            cur.execute(sql, (deleted, media, retweets, likes, text,
                              text_after, ban_100, ban_1k, ban_3k, tweet_id))

            self.mysqlCon.commit()
            result = "Ok"

        except:
            result = 'EXEPTION occurred!' + str(sys.exc_info()[1])
            self.mysqlCon.rollback()

        cur.close()

        return result

    def update_tweet_text_after(self, tweet_id, text_after=''):

        sql = "UPDATE tweet SET tweet_text_after = %s WHERE tweet_id = %s"

        cur = self.mysqlCon.cursor()

        try:
            cur.execute(sql, (text_after, tweet_id))
            self.mysqlCon.commit()
            result = "Ok"

        except:
            self.mysqlCon.rollback()
            result = 'EXEPTION occurred!' + str(sys.exc_info()[1])

        cur.close()

        return result

    def auto_update_tweet(self):
        cur = self.mysqlCon.cursor()

        try:
            print("Updating tweet text to remove the borring emoji '⃣'...")
            cur.execute("UPDATE tweet SET \
                tweet_text_after = REPLACE(tweet_text_after, '⃣', '') \
                WHERE tweet_text_after like '%⃣%'")

            print("Updating usage of URLs...")
            cur.execute("UPDATE tweet AS t SET tweet_url = 0 \
                WHERE tweet_text NOT LIKE '%http%'")

            cur.execute("UPDATE tweet AS t SET tweet_url = 1 \
                WHERE tweet_text LIKE '%http%'")

            print("Updating usage of Hashtags...")
            cur.execute("UPDATE tweet SET tweet_hashtag = 0 \
                WHERE tweet_text NOT LIKE '%#%'")

            cur.execute("UPDATE tweet SET tweet_hashtag = 1 \
                WHERE tweet_text LIKE '%#%'")

            print("Updating tweets when they are retweets...")
            cur.execute("UPDATE tweet SET tweet_RT = 0 \
                WHERE tweet_text NOT LIKE 'RT @%'")

            cur.execute("UPDATE tweet SET tweet_RT = 1 \
                WHERE tweet_text LIKE 'RT @%'")

            print("Updating the size range of each message...")
            cur.execute("UPDATE tweet SET tweet_size = 0 \
                WHERE LENGTH(tweet_text) = 0")

            for i in range(1, 26):
                j = i*10
                cur.execute("UPDATE tweet SET tweet_size = {0} \
                    WHERE LENGTH(tweet_text) <= {0} \
                    AND LENGTH(tweet_text) > {1}".format(j, j-10))

            cur.execute("UPDATE tweet SET tweet_size = 255 \
                WHERE LENGTH(tweet_text) <= 255 AND LENGTH(tweet_text) > 250")

            self.mysqlCon.commit()

        except:
            self.mysqlCon.rollback()
            print('EXEPTION occurred! ' + str(sys.exc_info()[1]))

        cur.close()

    def update_user(self, user_id, info):
        sql = """UPDATE user SET user_following = %s,
                    user_followers = %s, user_created_at = %s,
                    user_location = %s, user_description = %s
                WHERE user_id = %s"""

        cur = self.mysqlCon.cursor()

        try:
            cur.execute(sql, (info['following'], info['followers'],
                              info['created_at'], info['location'],
                              info['description'], user_id))

            self.mysqlCon.commit()
            result = "Ok"

        except:
            result = 'EXEPTION occurred!' + str(sys.exc_info()[1])
            self.mysqlCon.rollback()

        cur.close()

        return result

    # # # # # # # # # # # # # # # READ OPERATIONS # # # # # # # # # # # # # # #

    def tweet_list(self, where=''):
        sql = """SELECT tweet_id as id, tweet_text as txt,
                    tweet_language as lang, tweet_retweets as retweets,
                    tweet_likes as likes, deleted
                FROM tweet """ + where

        cur = self.mysqlCon.cursor()

        cur.execute(sql)
        result = cur.fetchall()
        cur.close()

        return result

    def last_tweets_list(self):
        sql = """SELECT u.user_id, u.user_name, t.tweet_id,
                    t.user_tweet_counter as tweet_counter,
                    (SELECT MAX(t3.user_tweet_counter) FROM tweet AS t3 WHERE t3.user_id = t.user_id AND t3.tweet_streamed = 0) AS counter_max,
                    (SELECT COUNT(*) FROM tweet AS t3 WHERE t3.user_id = t.user_id AND t3.tweet_streamed = 0) AS counter_diff,
                    (SELECT MIN(t3.tweet_id) FROM tweet AS t3 WHERE t3.user_id = t.user_id AND t3.tweet_streamed = 0) AS max_id
                FROM tweet as t
                JOIN user as u on u.user_id = t.user_id
                WHERE tweet_id in (select MAX(t2.tweet_id) from tweet as t2 where t2.tweet_streamed = 1 group by t2.user_id)
                GROUP BY user_id"""

        cur = self.mysqlCon.cursor()

        cur.execute(sql)
        result = cur.fetchall()
        cur.close()

        return result

    def users_list(self, where=''):
        sql = """SELECT * FROM user """ + where

        cur = self.mysqlCon.cursor()

        cur.execute(sql)
        allUsers = cur.fetchall()
        cur.close()

        result = {}

        for user in allUsers:
            result[user['user_id']] = user['user_name']

        return result

    def tweets_attr(self, rate, user=0, counter=0):
        sql = """SELECT
                    t.tweet_text_after as txt,
                    IF(t.tweet_polarity IS NOT NULL, CAST(t.tweet_polarity AS DEC(4,2)), 0.00) AS polarity,
                    IF(t.tweet_url = 1, 1, 0) as url,
                    IF(t.tweet_hashtag = 1, 1, 0) as hashtag,
                    IF(t.tweet_RT = 1, 1, 0) as RT,
                    t.tweet_size,
                    IF(t.tweet_ban_3000 IS NOT NULL, CAST(t.tweet_ban_3000 AS DEC(4,2)), 0.00) AS banality,
                    IF(((t.tweet_likes+t.tweet_retweets)/u.user_followers*100)>%s, 1, 0) as popular
                FROM tweet as t
                JOIN user as u ON t.user_id = u.user_id
                WHERE t.tweet_language = 'en'
                    AND tweet_text_after != ''"""

        if(user != 0):
            sql = sql + " AND t.user_id = %s "

        if(counter):
            sql = "SELECT popular, count(*) as count \
                FROM (" + sql + ") as test GROUP BY popular ORDER BY popular"

        cur = self.mysqlCon.cursor()

        if(user != 0):
            cur.execute(sql, (rate, user))
        else:
            cur.execute(sql, rate)

        result = cur.fetchall()

        cur.close()

        return result
