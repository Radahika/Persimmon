# Summarizer based on Flipboard's blog post: http://engineering.flipboard.com/2014/10/summarization/

'''

1) Model the document as a graph, with each sentence of the document as a node and the relationships as weighted edges.
  a) Sentences are bags of words, and the strength of interaction between two sentences is the similarity betwene their word-sets.
  b) Jaccard similarity/Hamming distance as edge weights
  c) (Normalize edge weights)

2) Compute the PageRank centrality measure for each sentence.
3) Sort sentences by their scores, select the top n, and reorder them by appearance

'''

import pdb

from pattern.en import tokenize
from pattern.vector import Document, LEMMA

def summarize(raw_text):
    tokens = tokenize(raw_text)
    print tokens

    documents = []
    for position, sentence in enumerate(tokens):
        if len(sentence.split(" ")) > 5:
            document = Document(string=sentence, name=position, stemmer=LEMMA)
            documents.append(document)

    print documents


if __name__ == "__main__":
    f = open("samples/alaska.txt", "r")
    text = f.read()
    print summarize(text)
