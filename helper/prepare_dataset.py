import os
import sys
import numpy as np

from sklearn.model_selection import train_test_split

from helper.db_connection import DbConnection

def get_data(rate, user = 0, getText = 0):
    print("\n Engagement Rate:", (rate*100), "%")
    print(" User:", user)

    conn = DbConnection()

    # Get all the tweets with the attributes
    tweets = conn.tweets_attr(rate, user)

    # Shuffle the list of tweets
    np.random.shuffle(tweets)

    # Get the number of popular and unpopular tweets considering the rate
    n_popular = conn.tweets_attr(rate, user, 1)

    n_pop = [] # Array with counter of both classes
    n_pop.append(n_popular[0]["count"]) # Number of popular tweets considering the rate
    n_pop.append(n_popular[1]["count"]) # Number of unpopular tweets considering the rate

    # Variable to control the balance between the classes
    max_class = n_pop[0] if n_pop[0] < n_pop[1] else n_pop[1]

    data, target = [], []

    count_pop = 0
    count_unpop = 0

    for tw in tweets:

        if((count_pop == max_class and tw['popular'] == 1) or
            (count_unpop == max_class and tw['popular'] == 0)):
            continue

        if(getText == 1):
            data.append(tw['txt'])

        else:
            data.append({
                "polarity": float(tw['polarity']),
                "url": tw['url'],
                "hashtag": tw['hashtag'],
                "RT": tw['RT'],
                "tweet_size": tw['tweet_size'],
                "banality": float(tw['banality'])
            })

        target.append(tw['popular'])

        if(tw['popular'] == 1):
            count_pop += 1
        else:
            count_unpop += 1

        if(len(target) == max_class*2):
            break

    print(" Total of tweets:", (n_pop[0] + n_pop[1]), "\t\tTotal used: ", len(target), "\n")

    print(" Total of Popular:", n_pop[1], "\tUnpopular:", n_pop[0])

    print(" Balanced Popular:", count_pop, "\tUnpopular:", count_unpop, "\n")

    return data, target, n_pop

if __name__ == '__main__': # COMPILE WITH: python3 prepare_dataset.py RATE USEFOR USER GETTEXT

    arg_names = ['command','rate', 'useFor', 'user', 'getText']
    args = dict(zip(arg_names, sys.argv))

    if('rate' not in args):
        args['rate'] = 0.02 # Minimum value of engagement rate to consider an tweet as popular
    else:
        args['rate'] = float(args['rate'])

    if('useFor' not in args):
        args['useFor'] = "weka" # Identifies if the dataset will be used at Weka

    if('user' not in args):
        args['user'] = 0 # The ID of specific user author

    if('getText' not in args):
        args['getText'] = 0 # Indicate if the text will be used

    # Data attributes, label classes, number of each class
    attr, label, n_pop = get_data(args['rate'], args['user'], args['getText'])

    # Records ARFF file for using at Weka
    if(args['useFor'] == "weka"):
        if not os.path.exists("ARFF/"+ str(args['user'])):
            os.makedirs("ARFF/"+ str(args['user']))

        file_name = "user_" + str(args['user']) + "_rate_" + str(args['rate']) +'.arff'

        f = open("ARFF/"+ str(args['user']) + "/" +file_name,'w')

        f.write("@RELATION tweetGather\n\n")

        f.write("@ATTRIBUTE polarity NUMERIC\n")
        f.write("@ATTRIBUTE hashtag {yes, no}\n")
        f.write("@ATTRIBUTE RT {yes, no}\n")
        f.write("@ATTRIBUTE tweet_size NUMERIC\n")
        f.write("@ATTRIBUTE banality NUMERIC\n")
        f.write("@ATTRIBUTE popular {yes, no}\n\n")

        f.write("@DATA\n")

        for i, tw in enumerate(attr):
            tw['hashtag'] = 'yes' if tw['polarity'] == 1 else 'no'
            tw['RT'] = 'yes' if tw['RT'] == 1 else 'no'
            tw['popular'] = 'yes' if label[i] == 1 else 'no'

            f.write(str(tw['polarity']) + ", " + tw['hashtag'] + ", " + tw['RT'] +
                ", " + str(tw['tweet_size']) + ", " + str(tw['banality']) + ", " + tw['popular'] + "\n")

        f.close()

        print(" ARFF File generated: " + file_name + "\n")