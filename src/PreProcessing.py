import re
import string

from nltk.corpus import stopwords


def make_lowercase(text):
    return text.lower()


def remove_numeric(text):
    result = re.sub(r'\d+', '', text)
    return result


def remove_punctuation_marks(text):
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    text = text.replace("<br />", " ")
    formatter = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    return text.translate(formatter)


def remove_extra_space(text):
    return " ".join(text.split())


def remove_english_stop_words(text):
    text = ' '.join([word for word in text.split() if word not in (stopwords.words('english'))])
    return text


def pre_process_text(text):
    text = make_lowercase(text)
    text = remove_numeric(text)
    text = remove_punctuation_marks(text)
    text = remove_extra_space(text)
    # text = remove_english_stop_words(text)
    return text

# Removing stop words can actually be more harmful in sentiment analysis
# text = pre_process_text("This is not at all acceptable")
# print(text)
