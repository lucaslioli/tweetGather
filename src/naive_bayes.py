import os
import re
import sys
import string
import math
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

sys.path.append('./')
from helper.db_connection import DbConnection
from prepare_dataset import get_data


class PopularDetector(object):
    """Implementation of Naive Bayes for binary classification"""
    def clean(self, s):
        translator = str.maketrans("", "", string.punctuation)
        return s.translate(translator)

    def tokenize(self, text):
        text = self.clean(text).lower()
        return re.split("\W+", text)

    def get_word_counts(self, words):
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0.0) + 1.0
        return word_counts

    def fit(self, X, Y):
        """Fit our classifier
        Arguments:
            X {list} -- list of document contents
            y {list} -- correct labels
        """
        self.num_messages = {}
        self.log_class_priors = {}
        self.word_counts = {}
        self.vocab = set()

        n = len(X)
        self.num_messages['spam'] = sum(1 for label in Y if label == 1)
        self.num_messages['ham'] = sum(1 for label in Y if label == 0)
        self.log_class_priors['spam'] = math.log(self.num_messages['spam'] / n)
        self.log_class_priors['ham'] = math.log(self.num_messages['ham'] / n)
        self.word_counts['spam'] = {}
        self.word_counts['ham'] = {}

        for x, y in zip(X, Y):
            c = 'spam' if y == 1 else 'ham'
            counts = self.get_word_counts(self.tokenize(x))
            for word, count in counts.items():
                if word not in self.vocab:
                    self.vocab.add(word)
                if word not in self.word_counts[c]:
                    self.word_counts[c][word] = 0.0

                self.word_counts[c][word] += count

    def predict(self, X):
        result = []
        for x in X:
            counts = self.get_word_counts(self.tokenize(x))
            spam_score = 0
            ham_score = 0
            for word, _ in counts.items():
                if word not in self.vocab:
                    continue

                # add Laplace smoothing
                log_w_given_spam = math.log((
                    self.word_counts['spam'].get(word, 0.0) + 1) /
                    (self.num_messages['spam'] + len(self.vocab)))

                log_w_given_ham = math.log((
                    self.word_counts['ham'].get(word, 0.0) + 1) /
                    (self.num_messages['ham'] + len(self.vocab)))

                spam_score += log_w_given_spam
                ham_score += log_w_given_ham

            spam_score += self.log_class_priors['spam']
            ham_score += self.log_class_priors['ham']

            if spam_score > ham_score:
                result.append(1)
            else:
                result.append(0)
        return result

# COMPILE WITH: python3 naive_bayes.py RATE USER
if __name__ == '__main__':

    arg_names = ['command', 'rate', 'user']
    args = dict(zip(arg_names, sys.argv))

    # Minimum value of engagement rate to consider an tweet as popular
    if('rate' not in args):
        args['rate'] = 0.02
    else:
        args['rate'] = float(args['rate'])

    # The ID of specific user author
    if('user' not in args):
        args['user'] = 0

    attr, label, popular = get_data(args['rate'], args['user'], 1)

    # Divide the tweets into train and test lists
    attr_train, attr_test, label_train, label_test = \
        train_test_split(attr, label, test_size=0.40, random_state=42)

    # print(*attr_test, sep='\n')
    print(" Attr Train: {} \tLabel Train: {} \t60%".format(
        len(attr_train), len(label_train)))
    print(" Attr Test: {} \tLabel Test: {} \t40% \n".format(
        len(attr_test), len(label_test)))

    count_pop_train = sum(1 for i in range(len(label_train)) if label_train[i] == 1)
    count_unpop_train = (len(label_train) - count_pop_train)

    count_pop_test = sum(1 for i in range(len(label_test)) if label_train[i] == 0)
    count_unpop_test = (len(label_test) - count_pop_test)

    print(" Popular Train: {} \tUnpopular Train: {}".format(
           count_pop_train, count_unpop_train))
    print(" Popular Test: {} \tUnpopular Test: {} \n".format(
          count_pop_test, count_unpop_test))

    MNB = PopularDetector()
    MNB.fit(attr_train, label_train)

    y_pred = MNB.predict(attr_test)
    y_true = label_test

    dashs = "-" * 23
    print("{0} METRICS {0}\n".format(dashs))

    print(classification_report(y_true, y_pred, labels=[0, 1]))

    print(confusion_matrix(y_true, y_pred))
