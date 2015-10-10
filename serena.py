from __future__ import unicode_literals, print_function
from spacy.en import English
from collections import Counter

nlp = English()

# returns dictionary of noun chunks: occurrences and list of sentences (strings) in a text
def hah():
	text = nlp(input())
	nounchunks = Counter([n.orth_.lower() for n in text.noun_chunks])
	sentences = [s.orth_ for s in text.sents]
	return nounchunks, sentences
