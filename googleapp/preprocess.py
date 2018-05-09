import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def get_words_in_sentences(sentences):
    all_words = []
    for words in sentences:
        all_words.extend(words)
    return all_words


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def preprocess(data):
        sente = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', data)
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(sente)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        sente = re.sub('@[^\s]+', '', str(filtered_sentence))
        # Remove additional white spaces
        sente = re.sub('[\s]+', ' ', sente)
        # Replace #word with word
        sente = re.sub(r'#([^\s]+)', r'\1', sente)
        # trim
        sente = sente.strip('\'"')
        words_filtereds = [e.lower() for e in sente.split() if len(e) >= 3]
        word_features = get_word_features(get_words_in_sentences(words_filtereds))
        return data