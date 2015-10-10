from __future__ import unicode_literals, print_function
from spacy.en import English


nlp=English()

def process(input):
	return nlp(input)



