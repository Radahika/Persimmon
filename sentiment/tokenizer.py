import nltk
from nltk.stem import *
from nltk.stem.porter import *
from textblob import TextBlob

stemmer = SnowballStemmer("english")
f = open('sentiment/negative_words.txt', 'r')
negative = set(f.read().split('\n'))

def tokenize(text):
    words = TextBlob(text).words.lower()
    tokens = [0]*len(words)
    i = 0
    while i < len(words):
        if words[i] in negative:
            try:
                tokens[i+1] = '!' + stemmer.stem(words[i+1])
                tokens[i] = stemmer.stem(words[i])
                tokens[i-1] = '!' + stemmer.stem(words[i-1])
                #tokens[i+1] = '!' + words[i+1]
                #tokens[i] = words[i]
                #tokens[i-1] = words[i-1]
                i += 2
                continue
            except IndexError:
                pass
        tokens[i] = stemmer.stem(words[i])
        #tokens[i] = words[i]
        i += 1
    return tokens

