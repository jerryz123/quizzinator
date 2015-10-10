from __future__ import unicode_literals, print_function
from spacy.en import English
from collections import Counter
from spacy.parts_of_speech import *
import random

nlp = English()

fil = open("sampletext.txt")
t= fil.read().splitlines()
test=''
for i in t:
	test+=i+" "

class Question:
	def __init__(self,sent,answer):
		self.sentence=sent
		self.chunkanswer=answer
	def fillblank(self):
		prompt=''
		for w in self.sentence.abwords:
			if w in self.chunkanswer.words:
				prompt+="____ "
			else:
				prompt+=w.text+" "
		return prompt

class Sentence:
	def __init__(self,span,parent,c=[]):
		self.abstraction=span
		self.abwords=[w for w in span]
		self.text=span.text
		self.paragraph=parent
		self.makewords()
		self.chunks=c
		self.questions=[Question(self,a) for a in self.chunks if a.useable]+[Question(self,NumChunk(num)) for num in self.abwords if num.like_num]


	def makewords(self):
		d=[[w,Word(w,self,self.paragraph)] for w in self.abstraction]
		for dup in d:
			dup[1].sethead(listdic(d,dup[0].head))
			for c in dup[0].children:
				dup[1].addchild(listdic(d,c))
		self.words=[dup[1] for dup in d]
	def displayusage(self):
		for w in self.words:
			w.displayusage() 
	def display(self):
		s=''
		for w in self.words:
			s+=w.text + " "
		print(s)


def listdic(lis,inp):
	for dup in lis:
		if dup[0]==inp:
			return dup[1]

class Chunk:
	def __init__(self,span):
		self.abstraction=span
		self.words=[w for w in span]
		self.text=span.text
		self.use()
	def use(self):
		for w in self.words:
			if w.ent_type!=0:
				self.useable=True
				return
		self.useable=False
class NumChunk(Chunk):
	def __init__(self,w):
		self.words=[w]
		self.text=w.text
		self.useable=True
class Paragraph:
	def __init__(self,t):
		self.abstraction=nlp(t)
		self.listchunks()
		self.sentences=[Sentence(s,self,self.findchunksinsentence(s)) for s in self.abstraction.sents]
		
		self.text=self.abstraction.text

	def showquestions(self):
		[[print(q.fillblank()) for q in s.questions] for s in self.sentences]
	def findchunksinsentence(self,sent):
		chu=[]
		for c in self.chunks:
			if c.abstraction.start>=sent.start and c.abstraction.start<=sent.end:
				chu.append(c)
		return chu
	def display(self): 
		for s in self.sentences:
			s.display()
	def displayusage(self):
		for s in self.sentences:
			s.displayusage()
	def listchunks(self):
		self.chunks=[Chunk(c) for c in self.abstraction.noun_chunks if len(c)>1]



def displayspan(span):
	for w in span:
		print(w.text,w.dep_)
		




class Word:
	def __init__(self,token,sentence,paragraph):
		self.text=token.text
		self.abstraction=token
		self.children=[]
		self.usage=token.dep_
	def display(self):
		print(self.text)
	def sethead(self,h):
		self.head=h
	def setchildren(self,ch=[]):
		self.children=ch
	def addchild(self,c):
		self.children.append(c)
	def displayusage(self):
		print(self.text,self.usage)


def listify(string):
	text = nlp(string)
	return[Sentence(s) for s in text.sents]



# returns dictionary of noun chunks: occurrences and list of sentences (strings) in a text
def hah():
	text = nlp(input())
	nounchunks = Counter([n.orth_ for n in text.noun_chunks])
	sentences = [s.text for s in text.sents]
	return nounchunks, sentences


def process(nouns):
	n = [ [nouns[x], x] for x in nouns ]
	n.sort(key = lambda x: x[0])
	n.reverse()
	return n

def questions(n, sents):
	for i in range(10):
		word = n[i][1]
		q = random.choice([s for s in sents if word in s])
		print(q[0: q.find(word)] + 'which thing ' + q[q.find(word) + len(word):])

#takes in a string and returns list of lists, where each list is the noun chunks in each sentence 
def sentence_noun_chunks(string):
	sentences = [s for s in nlp(string).sents]
	sentences = [nlp(s.text) for s in sentences]
	chunks = [[ch.text for ch in s.noun_chunks] for s in sentences]
	return chunks

