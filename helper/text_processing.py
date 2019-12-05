import re
import emoji                                     # Remove emojis from text
import string                                    # Remove ponctuation from text
import unicodedata                               # Remove accents from text
from nltk.corpus import stopwords                # Methods to remove stop words
from nltk.stem.wordnet import WordNetLemmatizer  # Methods to lemmatize text


def simple_cleaner(text):
    # Remove line breaks
    text = text.replace('\n', ' ').replace('\r', '')

    # Remove especial characters
    text = text.lstrip().rstrip().replace(u'\ufeff', '')

    # Map ponctuation from the text to space
    translation_table = str.maketrans(string.punctuation, \
        ' ' * len(string.punctuation))

    text = text.translate(translation_table)

    return text


def text_cleaner(text):

    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\u2640-\u2642"
        u"\xf0\x9f\x98\x86"
        u"\xe2\x80\xa6"
        u"\u2026"
        u"\u200d"
        "]+", flags=re.UNICODE)

    # Getting the set of stop words
    stop = set(stopwords.words('portuguese'))

    # Instance an object lemmatizer
    lemma = WordNetLemmatizer()

    # Removes the line breaks
    text = text.replace('\n', ' ').replace('\r', '')

    # To remove special characters identified later
    text = text.replace('“', '').replace('”', '')

    # To make the text minuscule
    text = text.lower()

    # To remove URLs, mentions and hashtags from the text
    text = re.sub(r'http\S+|@\S+|#\S+', '', text)

    # To remove laughs from the string
    text = re.sub(r'\b(a*ha+h[ha]*|o?l+o+l+[ol]*)\b', '', text)

    # To remove words (laughs) that have a sigle letter (e.g. kkkkk)
    text = ' '.join(w for w in text.split()
                    if len(''.join(c for c in w if c != w[0])) > 1)

    # To remove the emojis from the text
    text = emoji.get_emoji_regexp().sub(r'', text)
    text = emoji_pattern.sub(r'', text)

    # To remove the stop words from the text
    text = ' '.join([w for w in text.split() if w not in stop])

    # Map ponctuation from the text to space
    translation_table = str.maketrans(string.punctuation, \
        ' ' * len(string.punctuation))

    text = text.translate(translation_table)

    # Lemmatizes the text
    # text = ' '.join(lemma.lemmatize(w) for w in text.split())

    # To remove the accents from the text
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')

    # To remove number from the text
    text = ''.join(c for c in text if not c.isdigit())

    # To remove words with only one character
    text = ' '.join([w for w in text.split() if len(w) > 1])

    # To remove duplicate letters - STAND BY
    # text = re.sub(r'(\w)\1+', r'\1', text)

    # To remove the white spaces in the beginning and in the end of the text
    text = text.lstrip().rstrip()

    return text
