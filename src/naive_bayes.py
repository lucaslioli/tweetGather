import os
import re
import sys
import string
import math
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

sys.path.append('../helper')
from db_connection import DbConnecion

# Credits for the help in Naive Bayes algorithm implementation for:
# https://pythonmachinelearning.pro/text-classification-tutorial-with-naive-bayes/

def get_data(conference):
    conn = DbConnecion()

    # Get all the tweets with the attributes
    tweets = conn.tweets_attr(rate, conference)

    if(conference):
        print(tweets)
        exit()
    
    # Shuffle the list of tweets
    np.random.shuffle(tweets)

    data, target = [], []

    for tw in tweets:
        data.append(tw['txt'])
        target.append(tw['popular'])

    return data, target

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
        

if __name__ == '__main__':
    # When conf = 1, the function will return the number for each label
    # rate is the minimum value of engagement rate to consider an tweet as popular
    if(len(sys.argv) < 2):
        rate = 0.02
        conf = 0
    elif(len(sys.argv) < 3):
        rate = float(sys.argv[1])
        conf = 0
    else:
        rate = float(sys.argv[1])
        conf = float(sys.argv[2])
    
    attr, label = get_data(conf)

    print(" Engagement Rate:", (rate*100), "%")
    print(" Total of Tweets:", len(attr), "\n")

    # Divide the tweets into train and test lists
    attr_train, attr_test, label_train, label_test = train_test_split(attr, label, test_size=0.20, random_state=42)

    # print(*attr_test, sep='\n')
    print(" Attr Train:", len(attr_train), "\tLabel Train:", len(label_train), "\t80% \n",
        "Attr Test:", len(attr_test), "\tLabel Test:", len(label_test), "\t20% \n")

    MNB = PopularDetector()
    MNB.fit(attr_train, label_train)

    pred = MNB.predict(attr_test)
    true = label_test

    accuracy = sum(1 for i in range(len(pred)) if pred[i] == true[i]) / float(len(pred))
    print(" Accuracy: ", "{0:.4f}".format(accuracy))

    print("\n Confusion Matrix: \n",confusion_matrix(label_test, pred))
