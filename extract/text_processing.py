import re
import string                                   # Remove the ponctuation from the texts
import unicodedata                              # Remove the accents from the texts
from nltk.corpus import stopwords               # Methods to remove stop words
from nltk.stem.wordnet import WordNetLemmatizer # Methods to lemmatize the textsZ

def text_cleaner(text):

    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\xf0\x9f\x98\x86"
        u"\xe2\x80\xa6"
        u"\u2026"
        u"\u200d"
        "]+", flags=re.UNICODE)

    # Getting the set of stop words
    stop = set(stopwords.words('portuguese'))

    # Getting the set of punctuation
    pont=set(string.punctuation)

    # Instance an object lemmatizer
    lemma = WordNetLemmatizer()

    # Removes the line breaks
    text = text.replace('\n', ' ').replace('\r', '')

    # To make the text minuscule
    text = text.lower()

    # To remove URLs, mentions and hashtags from the text
    text = re.sub(r'http\S+|@\S+|#\S+', '', text)

    # To remove laughs from the string
    text = re.sub(r'\b(a*ha+h[ha]*|o?l+o+l+[ol]*)\b', '', text)

    # To remove words (laughs) that have a sigle letter (e.g. kkkkk)
    text = ' '.join(w for w in text.split() if len(''.join(c for c in w if c != w[0]))>1)

    # To remove the emojis from the text
    text = emoji_pattern.sub(r'', text)

    # To remove the stop words from the text
    text = ' '.join([w for w in text.split() if w not in stop])

    # To remove the ponctuation from the text
    text = ''.join(c for c in text if c not in pont)

    # Lemmatizes the text
    #text = ' '.join(lemma.lemmatize(w) for w in text.split())

    # To remove the accents from the text
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
          if unicodedata.category(c) != 'Mn')

    # To remove number from the text
    text = ''.join([c for c in text if not c.isdigit()])

    # To remove words with only one character
    text = ' '.join( [w for w in text.split() if len(w)>1])

    # To remove duplicate letters - STAND BY
    # text = re.sub(r'(\w)\1+', r'\1', text)

    # To remove the white spaces in the beginning and in the end of the text
    text = text.lstrip().rstrip()

    return text