CREATE TABLE `tweet` (
  `tweet_id` bigint(20) NOT NULL,
  `tweet_text` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `tweet_text_after` varchar(255) CHARACTER SET utf8mb4 DEFAULT NULL,
  `tweet_datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tweet_language` varchar(50) COLLATE utf8_bin DEFAULT NULL,
  `tweet_retweets` int(11) DEFAULT NULL,
  `tweet_likes` int(11) DEFAULT NULL,
  `tweet_replies` int(11) DEFAULT NULL,
  `tweet_replied_to` bigint(20) DEFAULT NULL,
  `tweet_polarity` decimal(7,6) DEFAULT NULL,
  `tweet_subjectivity` decimal(7,6) DEFAULT NULL,
  `tweet_url` int(11) DEFAULT NULL,
  `tweet_hashtag` int(11) DEFAULT NULL,
  `tweet_RT` int(11) DEFAULT NULL,
  `tweet_size` int(11) DEFAULT NULL,
  `tweet_ban_100` decimal(7,6) DEFAULT NULL,
  `tweet_ban_1000` decimal(7,6) DEFAULT NULL,
  `tweet_ban_3000` decimal(7,6) DEFAULT NULL,
  `tweet_for_elections` int(11) NOT NULL DEFAULT '0',
  `deleted` int(11) NOT NULL DEFAULT '0',
  `user_id` bigint(20) NOT NULL,
  `user_followers` int(11) DEFAULT NULL,
  `user_followers_diff` int(11) DEFAULT NULL,
  `user_tweet_counter` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `user` (
  `user_id` bigint(20) NOT NULL,
  `user_name` varchar(255) CHARACTER SET utf8mb4 NOT NULL,
  `user_screen_name` varchar(255) COLLATE utf8_bin NOT NULL,
  `user_following` int(11) DEFAULT NULL,
  `user_language` varchar(50) COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `user_followers_history` (
  `id` int(11) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `user_followers` int(11) NOT NULL DEFAULT '0',
  `difference` int(11) DEFAULT '0',
  `date_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

ALTER TABLE `tweet`
  ADD PRIMARY KEY (`tweet_id`),
  ADD KEY `FK1_user_tweet` (`user_id`);

ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

ALTER TABLE `user_followers_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK1_user` (`user_id`);

ALTER TABLE `user_followers_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6405;

ALTER TABLE `tweet`
  ADD CONSTRAINT `FK1_user_tweet` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `user_followers_history`
  ADD CONSTRAINT `FK1_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

ALTER TABLE `tweet` ADD `deleted` INT NOT NULL DEFAULT '0' AFTER `tweet_for_elections`;

UPDATE tweet SET deleted = 1 WHERE tweet_retweets IS NULL;