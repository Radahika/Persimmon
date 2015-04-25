from tokenizer import tokenize
import os, codecs, math
import pdb
from nltk.corpus import sentiwordnet as swn

class Trainer:

    def __init__(self):
        self.db = {}
        self.labels = []
        self.doc_counts = {}

        for filename in os.listdir('sentiment/samples/training'):
            if filename[0] != '.':
                file_dir = os.path.join("sentiment", "samples", "training", filename)
                if os.path.isdir(file_dir):
                    for filename in os.listdir(file_dir):
                        file_path = os.path.join(file_dir, filename)
                        self.open_files(file_path)
                elif os.path.isfile(file_dir):
                    self.open_files(file_dir)

    def open_files(self, file_path):
        f = codecs.open(file_path, "r", "utf-8")
        text = f.read()
        i = text.find('\n') + 1
        label, text = text.partition('\n')[0], text[i:]
        self.train(text, label)

    def register_label(self, label):
        """ Adds the LABEL to the "database" (in this case, localStorage) so that we
        can retrieve a list of labels later
        """
        if label not in self.db:
            self.db[label] = {}
            self.labels.append(label)

    def increment_stem(self, word, label):
        """Record the number of times a word was seen for a given label.
        """
        word_dict = self.db[label]
        if word in word_dict:
            word_dict[word] += 1.0
        else:
            word_dict[word] = 1.0

    def increment_doc_count(self, label):
        """
        Record how many documents we've seen for a given label.

        """
        if label in self.doc_counts:
            self.doc_counts[label] += 1.0
        else:
            self.doc_counts[label] = 1.0

    def train(self, text, label):
        self.register_label(label)
        words = tokenize(text)
        for word in words:
            self.increment_stem(word, label)
        self.increment_doc_count(label)

    def doc_count(self, label):
        return self.doc_counts[label]

    def doc_inverse_count(self, label):
        return self.total_doc_count() - self.doc_count(label)

    def total_doc_count(self):
        total = 0
        for doc in self.doc_counts:
            total += self.doc_counts[doc]
        return float(total)

    def stem_total_count(self, word):
        total = 0
        for label in self.labels:
            if word in self.db[label]:
                total += self.db[label][word]
        return float(total)

    def stem_label_count(self, label, word):
        if word in self.db[label]:
            return float(self.db[label][word])
        return 0

    def stem_inverse_label_count(self, label, word):
        return self.stem_total_count(word) - self.stem_label_count(label, word)

    def guess(self, text):
        doc_counts = {}
        doc_inverse_counts = {}
        tokens = tokenize(text)
        scores = {}
        for label in self.labels:
            doc_counts[label] = self.doc_count(label)
            doc_inverse_counts[label] = self.doc_inverse_count(label)
            total = self.total_doc_count()
        for label in self.labels:
            logSum = 0.0
            for word in tokens:
                stem_total_count = self.stem_total_count(word)
                if stem_total_count == 0.0:
                    continue
                else:
                    word_prob = self.stem_label_count(label, word) / doc_counts[label]
                    word_inverse_prob = self.stem_inverse_label_count(label, word) / doc_inverse_counts[label]
                    wordicity = word_prob / (word_prob + word_inverse_prob)

                    wordicity = (( 1.0 * 0.5) + (stem_total_count * wordicity) ) / (1.0 + stem_total_count )
                    if wordicity == 0.0:
                        wordicity = 0.01
                    elif wordicity == 1:
                        wordicity = 0.99
                try:
                    logSum += math.log(1.0 - wordicity) - math.log(wordicity)
                except ValueError:
                    print "ValueError"
            try:
                scores[label] = 1.0 / (1.0 + math.exp(logSum))
            except OverflowError:
                print "OverflowError"
        return scores

    def run_guess_sweep(self):
        for filename in os.listdir('sentiment/samples/guessing/short'):
            if filename[0] != '.':
                file_path = os.path.join("samples/guessing/short", filename)
                f = codecs.open(file_path, "r", "utf-8")
                text = f.read()
                i = text.find('\n') + 1
                label, text = text.partition('\n')[0], text[i:]
                scores = self.guess(text)

    def run_nltk_guess(self, text):
        tokens = tokenize(text)
        doc_counts = {}
        doc_inverse_counts = {}
        scores = {}

        for word in tokens:
            word_swn = swn.senti_synset(word)
            word_prob = self.stem_label_count(label, word) / doc_counts[label]
            print word_prob, word_swn

    def arg_max(self, text):
        scores = self.guess(text)
        mx_label = None
        mx_score = 0
        for label in scores:
            if scores[label] > mx_score:
                mx_label, mx_score = label, scores[label]
        return mx_label, mx_score

trainer = Trainer()


