import os
import sys
import numpy as np

from sklearn.model_selection import train_test_split

sys.path.append('./')
from helper.db_connection import DbConnection
from helper.text_processing import simple_cleaner


def get_data(rate, user_id=0, get_text=0):
    print("\n Engagement Rate: {:.2f}%".format(rate*100))

    conn = DbConnection()

    if user_id != 0:
        user = conn.users_list('where user_id = {}'.format(user_id))
        user_name = user[int(user_id)]
    else:
        user_name = "Not selected"

    print(" User: {} - {}\n".format(user_id, user_name))

    # Get all the tweets with the attributes
    tweets = conn.tweets_attr(rate, user_id)

    # Shuffle the list of tweets
    np.random.shuffle(tweets)

    # Get the number of popular and unpopular tweets considering the rate
    n_popular = conn.tweets_attr(rate, user_id, 1)

    n_pop = []  # Array with counter of both classes
    
    try:
        n_pop.append(n_popular[0]["count"])  # Unpopular count considering the rate
        n_pop.append(n_popular[1]["count"])  # Popular count considering the rate

    except:
        n_pop.append(0) # No one is popular

    # Variable to control the balance between the classes
    max_class = n_pop[0] if n_pop[0] < n_pop[1] else n_pop[1]

    data, target = [], []

    count_pop = 0
    count_unpop = 0

    for tw in tweets:

        if (count_pop == max_class and tw['popular'] == 1) or \
                (count_unpop == max_class and tw['popular'] == 0):
            continue

        if get_text == "--fullText":
            data.append(tw['full_txt'])

        elif get_text != 0:
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

        if tw['popular'] == 1:
            count_pop += 1
        else:
            count_unpop += 1

        if len(target) == max_class*2:
            break

    total = n_pop[0] + n_pop[1]
    print(" TOTAL OF tweets:  {:<6} Used: {:<6} Lost: {}\n".format(
        total, len(target), (total - len(target))))

    print(" TOTAL OF Popular: {:<6} Unpopular: {} ".format(n_pop[1], n_pop[0]))

    print(" BALANCED Popular: {:<6} Unpopular: {}\n".format(count_pop, count_unpop))

    return data, target, n_pop


def save_file(tweets, user, rate, use, ext):
    rate = str(rate).replace('.', '')
    file_name = "rate_{}_{}.{}".format(rate, use, ext)

    f = open("DATA/{}/{}".format(user, file_name), 'w')

    for tw in tweets:
        f.write(simple_cleaner(tw) + "\n")

    f.close()

    print(" LSTM File generated: " + file_name)

# COMPILE WITH: python3 generate_arff.py [useFor] [rate] [user] [getText]
if __name__ == '__main__':

    arg_names = ['command', 'useFor', 'rate', 'user', 'getText']
    args = dict(zip(arg_names, sys.argv))

    # Identifies if the dataset will be used at Weka
    if 'useFor' not in args:
        args['useFor'] = "weka"

    # Minimum value of engagement rate to consider a tweet as popular
    if 'rate' not in args:
        args['rate'] = 0.02
    else:
        args['rate'] = float(args['rate'])

    # The ID of specific user author
    if 'user' not in args:
        args['user'] = 0

    # Indicate if the text will be used
    if 'getText' not in args:
        args['getText'] = 0

    # Data attributes, classes labels, count of each class
    attr, label, n_pop = get_data(args['rate'], args['user'], args['getText'])

    # Records ARFF file for using at Weka
    if(args['useFor'] == "weka"):
        if not os.path.exists("ARFF/" + str(args['user'])):
            os.makedirs("ARFF/" + str(args['user']))

        file_name = "user_" + str(args['user']) + \
            "_rate_" + str(args['rate']) + '.arff'

        f = open("ARFF/" + str(args['user']) + "/" + file_name, 'w')

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

            f.write(str(tw['polarity']) + ", " + tw['hashtag'] +
                    ", " + tw['RT'] + ", " + str(tw['tweet_size']) +
                    ", " + str(tw['banality']) + ", " + tw['popular'] + "\n")

        f.close()

        print(" ARFF File generated: " + file_name + "\n")

    if(args['useFor'] == "lstm"):
        if not os.path.exists("DATA/" + str(args['user'])):
            os.makedirs("DATA/" + str(args['user']))

        pop, notpop, pop_train, pop_test, not_train, not_test = ([] for i in range(6))

        for i, tw in enumerate(attr):
            if label[i] == 1:
                pop.append(tw)
            else:
                notpop.append(tw)

        attr_train, attr_test, label_train, label_test = \
            train_test_split(attr, label, test_size=0.25, random_state=42)

        print(" Train and Test split: {} - {}\n".format(len(attr_train), len(attr_test)))

        for i, tw in enumerate(attr_train):
            if label[i] == 1:
                pop_train.append(tw)
            else:
                not_train.append(tw)

        for i, tw in enumerate(attr_test):
            if label[i] == 1:
                pop_test.append(tw)
            else:
                not_test.append(tw)

        print(" Train and Test split POP: {} - {}".format(len(pop_train), len(pop_test)))
        print(" Train and Test split NOT: {} - {}\n".format(len(not_train), len(not_test)))

        save_file(pop_train, args['user'], args['rate'], 'train', 'pop')
        save_file(pop_test, args['user'], args['rate'], 'test', 'pop')

        save_file(not_train, args['user'], args['rate'], 'train', 'not')
        save_file(not_test, args['user'], args['rate'], 'test', 'not')

        save_file(pop, args['user'], args['rate'], 'unique', 'pop')
        save_file(notpop, args['user'], args['rate'], 'unique', 'not')
        
        print("")
