# Summarizer based on Flipboard's blog post: http://engineering.flipboard.com/2014/10/summarization/

'''
1) Model the document as a graph, with each sentence of the document as a node and the relationships as weighted edges.
  a) Sentences are bags of words, and the strength of interaction between two sentences is the similarity betwene their word-sets.
  b) Jaccard similarity/Hamming distance as edge weights
  c) (Normalize edge weights)

2) Compute the PageRank centrality measure for each sentence.
3) Sort sentences by their scores, select the top n, and reorder them by appearance

'''

