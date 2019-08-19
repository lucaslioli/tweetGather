-- Dumping database structure for tweetgather
CREATE DATABASE IF NOT EXISTS `tweetgather` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `tweetgather`;

-- Dumping structure for table tweetgather.tweet
CREATE TABLE IF NOT EXISTS `tweet` (
  `tweet_id` bigint(20) unsigned NOT NULL,
  `tweet_text` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `tweet_text_after` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `tweet_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tweet_language` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `tweet_retweets` int(11) DEFAULT NULL,
  `tweet_likes` int(11) DEFAULT NULL,
  `tweet_polarity` decimal(7,6) DEFAULT NULL,
  `tweet_subjectivity` decimal(7,6) DEFAULT NULL,
  `tweet_url` int(11) unsigned DEFAULT NULL,
  `tweet_hashtag` int(11) unsigned DEFAULT NULL,
  `tweet_media` int(11) unsigned DEFAULT NULL,
  `tweet_RT` int(11) unsigned DEFAULT NULL,
  `tweet_size` int(11) unsigned DEFAULT NULL,
  `tweet_ban_100` decimal(7,6) DEFAULT NULL,
  `tweet_ban_1000` decimal(7,6) DEFAULT NULL,
  `tweet_ban_3000` decimal(7,6) DEFAULT NULL,
  `deleted` int(11) unsigned NOT NULL DEFAULT '0',
  `user_id` bigint(20) unsigned NOT NULL,
  `user_followers` int(11) unsigned DEFAULT NULL,
  `user_followers_diff` int(11) DEFAULT NULL,
  `user_tweet_counter` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`tweet_id`),
  KEY `FK1_user_tweet` (`user_id`),
  CONSTRAINT `FK1_user_tweet` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- Dumping structure for table tweetgather.user
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` bigint(20) unsigned NOT NULL,
  `user_name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `user_screen_name` varchar(255) COLLATE utf8_bin NOT NULL,
  `user_following` int(11) unsigned DEFAULT NULL,
  `user_language` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- Dumping structure for table tweetgather.user_followers_history
CREATE TABLE IF NOT EXISTS `user_followers_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) unsigned NOT NULL,
  `user_followers` int(11) unsigned NOT NULL DEFAULT '0',
  `difference` int(11) DEFAULT '0',
  `date_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK1_user_history` (`user_id`),
  CONSTRAINT `FK1_user_history` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6405 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;