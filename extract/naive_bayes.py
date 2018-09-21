import sys
import numpy as np

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

from db_connection import DbConnecion

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

    conn = DbConnecion()

    # Get all the tweets with the attributes
    tweets = conn.tweets_attr(rate, conf)

    if(conf):
        print(tweets)
        exit()
    
    # Shuffle the list of tweets
    np.random.shuffle(tweets)

    # Initializes attr and label variables
    attr, label = [], []

    # Divide the tweets into attributes/data and labels
    for tw in tweets:
        attr.append(tw['txt'].split())
        label.append(tw['popular'])

    print(" Engagement Rate:", (rate*100), "%")
    print(" Total of Tweets:", len(attr), "\n")

    # Divide the tweets into train and test lists
    attr_train, attr_test, label_train, label_test = train_test_split(attr, label, test_size=0.20, random_state=42)
    
    # print(*attr_test, sep='\n')
    print(" Attr Test:", len(attr_test), "\tLabel Test:", len(label_test), "\n",
        "Attr Train:", len(attr_train), "\tLabel Train:", len(label_train))

    # Naive Bayes -----
    naive = GaussianNB() 

    naive.fit(np.array(attr_train), label_train)

    predicted = naive.predict(np.array(attr_test))

    print(np.mean(predicted == label_test))

    print(confusion_matrix(label_test, predicted))
