from tokenizer import tokenize
import os, codecs
import pdb

class Trainer:

    def __init__(self):
        self.db = {}
        self.labels = []
        self.doc_counts = {}

        for filename in os.listdir('samples'):
            if filename[0] != '.':
                file_path = os.path.join("samples", filename)
                f = codecs.open(file_path, "r", "utf-8")
                first = f.readline()
                label = first.split()[0]
                text = f.read()
                try:
                    self.train(text, label)
                except UnicodeDecodeError:
                    print "UnicodeDecodeError for filename " + filename

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
        return len(self.doc_counts[label])

    def doc_inverse_count(self, label):
        return float(self.total_doc_count) - self.doc_count(label)

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

    def stem_inverse_label_count(self, label, word):
        return float(self.stem_total_count(word)) - self.stem_label_count(label, word)

    def guess(self, text):
        doc_counts = {}
        doc_inverse_counts = {}
        tokens = tokenize(text)
        scores = {}
        for label in self.labels:
            doc_counts[label] = self.doc_count(label)
            doc_inverse_counts[label] = self.doc_inverse_count(label)
            total = self.total_doc_count()
            logSum = 0.0
            for word in tokens:
                stem_total_count = self.stem_total_count(word)
                if stem_total_count == 0.0:
                    continue
                else:
                    stem_label_count = self.stem_label_count(word, label)
                    stem_inverse_label_count = self.stem_inverse_label_count(word, label)
                    word_prob = stem_label_count / doc_counts[label]
                    word_inverse_prob = stem_inverse_label_count / doc_inverse_count[label]
                    wordicity = word_prob / (word_prob + word_inverse_prob)

                    wordicity = (( 1.0 * 0.5) + (stem_total_count * wordicity) ) / (1.0 + stem_total_count )
                    if wordicity == 0.0:
                        wordicity = 0.01
                    elif wordicity == 1:
                        wordicity = 0.99

                logSum += math.log(1 - wordicity) - math.log(wordicity)
            scores[label] = 1.0 / (1.0 + math.exp(logSum))

trainer = Trainer()

