import os
import re
import sys
import string
import math
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

sys.path.append('./')
from helper.db_connection import DbConnection
from helper.prepare_dataset import get_data

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
                if word not in self.vocab: continue

                # add Laplace smoothing
                log_w_given_spam = math.log( (self.word_counts['spam'].get(word, 0.0) + 1) / (self.num_messages['spam'] + len(self.vocab)) )
                log_w_given_ham = math.log( (self.word_counts['ham'].get(word, 0.0) + 1) / (self.num_messages['ham'] + len(self.vocab)) )

                spam_score += log_w_given_spam
                ham_score += log_w_given_ham

            spam_score += self.log_class_priors['spam']
            ham_score += self.log_class_priors['ham']

            if spam_score > ham_score:
                result.append(1)
            else:
                result.append(0)
        return result

if __name__ == '__main__': # COMPILE WITH: python3 naive_bayes.py RATE USER

    arg_names = ['command','rate', 'user']
    args = dict(zip(arg_names, sys.argv))

    if('rate' not in args):
        args['rate'] = 0.02 # Minimum value of engagement rate to consider an tweet as popular
    else:
        args['rate'] = float(args['rate'])

    if('user' not in args):
        args['user'] = 0 # The ID of specific user author

    attr, label, popular = get_data(args['rate'], args['user'], 1)

    # Divide the tweets into train and test lists
    attr_train, attr_test, label_train, label_test = train_test_split(attr, label, test_size=0.40, random_state=42)

    # print(*attr_test, sep='\n')
    print(" Attr Train:", len(attr_train), "\tLabel Train:", len(label_train), "\t60% \n",
        "Attr Test:", len(attr_test), "\tLabel Test:", len(label_test), "\t40% \n")

    count_pop_train = sum(1 for i in range(len(label_train)) if label_train[i] == 1)
    count_unpop_train = (len(label_train) - count_pop_train)
    count_pop_test = sum(1 for i in range(len(label_test)) if label_train[i] == 0)
    count_unpop_test = (len(label_test) - count_pop_test)

    print(" Popular Train:", count_pop_train, "\tUnpopular Train:", count_unpop_train, "\n",
        "Popular Test:", count_pop_test, "\tUnpopular Test:", count_unpop_test, "\n")

    MNB = PopularDetector()
    MNB.fit(attr_train, label_train)

    pred = MNB.predict(attr_test)
    true = label_test

    accuracy = sum(1 for i in range(len(pred)) if pred[i] == true[i]) / float(len(pred))
    pop_accuracy = sum(1 for i in range(len(pred)) if pred[i] == true[i] and true[i] == 1) / sum(1 for i in range(len(pred)) if true[i] == 1)
    unp_accuracy = sum(1 for i in range(len(pred)) if pred[i] == true[i] and true[i] == 0) / sum(1 for i in range(len(pred)) if true[i] == 0)

    print("---------------- Accuracy ----------------")
    print(" |General", "\t|Popular", "\t|Unpopular")
    print(" |{0:.4f}".format(accuracy), "\t|{0:.4f}".format(pop_accuracy), "\t|{0:.4f}".format(unp_accuracy))

    print("\nConfusion Matrix: \n")
    print(confusion_matrix(label_test, pred))
