# Summarizer based on Flipboard's blog post: http://engineering.flipboard.com/2014/10/summarization/

'''

1) Model the document as a graph, with each sentence of the document as a node and the relationships as weighted edges.
  a) Sentences are bags of words, and the strength of interaction between two sentences is the similarity betwene their word-sets.
  b) Jaccard similarity/Hamming distance as edge weights
  c) (Normalize edge weights)

2) Compute the PageRank centrality measure for each sentence.
3) Sort sentences by their scores, select the top n, and reorder them by appearance

'''

import os
import sys
import codecs

import pdb

from pattern.en import tokenize
from pattern.vector import Document, LEMMA

import nltk.data

import networkx
import operator

def summarize_file(file_name):
    file_path = os.path.join("samples", file_name)
    f = codecs.open(file_path, "r", "utf-8")
    text = f.read()
    print summarize(text)


def summarize(raw_text):
    tokens = tokenize(raw_text)

    pdb.set_trace()

    documents = []
    for position, sentence in enumerate(tokens):
        if len(sentence.split(" ")) > 5:
            document = Document(string=sentence, name=position, stemmer=LEMMA)
            if len(document.features) > 0:
                documents.append(document)

    edges = []
    for document in documents:
        for other_document in documents:
            if document.name == other_document.name:
                continue
            doc_words = document.features
            other_doc_words = other_document.features
            similarity = jaccard_similarity(doc_words, other_doc_words)
            if similarity > 0:
                edges.append((document.name, other_document.name, similarity))

    graph = networkx.DiGraph()
    graph.add_weighted_edges_from(edges)
    page_rank = networkx.pagerank(graph)

    sorted_ranks = sorted(page_rank.items(), key=operator.itemgetter(1), reverse=True)

    summary = []
    sentence_numbers = []
    for i in range(5):
        node = sorted_ranks[i]
        sentence_numbers.append(node[0])

    sentence_numbers = sorted(sentence_numbers)

    for sentence_number in sentence_numbers:
        sentence = tokens[sentence_number]
        summary.append(sentence)

    return " ".join(summary)

def jaccard_similarity(group1, group2):
    set1 = set(group1)
    set2 = set(group2)
    return float(len(set1.intersection(set2))) / len(set1.union(set2))


if __name__ == "__main__":
    filename = ""
    if len(sys.argv) == 1:
        filename = "alaska.txt"
    else:
        filename = sys.argv[1]
    print summarize_file(filename)
