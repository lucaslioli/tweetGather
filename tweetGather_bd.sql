DROP DATABASE IF EXISTS `tweetgather`;
CREATE DATABASE IF NOT EXISTS `tweetgather`;
USE `tweetgather`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` bigint(20) NOT NULL,
  `user_name` varchar(255) COLLATE utf8_bin NOT NULL,
  `user_screen_name` varchar(255) COLLATE utf8_bin NOT NULL,
  `user_following` int(11) DEFAULT NULL,
  `user_language` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


DROP TABLE IF EXISTS `user_followers_history`;
CREATE TABLE IF NOT EXISTS `user_followers_history` (
  `user_id` bigint(20) NOT NULL,
  `user_followers` int(11) NOT NULL DEFAULT '0',
  `difference` int(11) DEFAULT '0',
  `datetime` DATETIME NOT NULL,
  PRIMARY KEY (`user_id`),
  KEY `FK1_user` (`user_id`),
  CONSTRAINT `FK1_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

DROP TABLE IF EXISTS `tweet`;
CREATE TABLE IF NOT EXISTS `tweet` (
  `tweet_id` bigint(20) NOT NULL,
  `tweet_text` varchar(255) COLLATE utf8_bin NOT NULL,
  `tweet_datetime` timestamp NOT NULL,
  `tweet_language` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `tweet_retweets` int(11) DEFAULT NULL,
  `tweet_likes` int(11) DEFAULT NULL,
  `tweet_replies` int(11) DEFAULT NULL,
  `tweet_replied_to` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  `user_followers` INT NULL DEFAULT NULL,
  `user_followers_diff` INT NULL DEFAULT NULL,
  PRIMARY KEY (`tweet_id`),
  KEY `FK1_user_tweet` (`user_id`),
  CONSTRAINT `FK1_user_tweet` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;