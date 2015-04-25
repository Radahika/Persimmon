import nltk
from nltk.stem import *
from nltk.stem.porter import *
from textblob import TextBlob
from nltk.corpus import stopwords

stemmer = SnowballStemmer("english")
f = open('sentiment/negative_words.txt', 'r')
negative = set(f.read().split('\n'))
stop = set(stopwords.words('english'))

def tokenize(text):
    words = TextBlob(text).words.lower()
    words = filter(lambda w: not w in stop, words)
    tokens = [0]*len(words)
    i = 0
    while i < len(words):
        if words[i] in negative:
            try:
                tokens[i+1] = '!' + stemmer.stem(words[i+1])
                tokens[i] = stemmer.stem(words[i])
                tokens[i-1] = '!' + stemmer.stem(words[i-1])
                i += 2
                continue
            except IndexError:
                pass
        tokens[i] = stemmer.stem(words[i])
        #tokens[i] = words[i]
        i += 1
    return tokens

