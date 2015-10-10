from __future__ import unicode_literals, print_function
from spacy.en import English
from collections import Counter
from spacy.parts_of_speech import *
import random

quiddict = {
		0: 'WHAT ',
		28061: 'WHAT person ',
		1499631: 'WHAT place ',
		164860: 'WHAT facility ',
		202115: 'WHAT organization ',
		85248: 'WHAT place ',
		39247: 'WHAT law ',
		17764: 'HOW MANY ',
		55719: 'HOW MANY ',
		81537: 'WHAT place ',
		87482: 'WHAT place ',
		202115: 'WHAT place ',
		354826: "HOW many "

	}

nlp = English()

fil = open("sampletext.txt")
t= fil.read().splitlines()
test=''
for i in t:
	test+=i+" "


# contains sentence and answer, runs stuff on that
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

	def fillwhat(self):
		prompt=''
		for w in self.sentence.abwords:
			if w in self.chunkanswer.words:
				prompt+="____"
			else:
				prompt+=w.text+" "
		_length = ''
		for c in prompt:
			if c == '_':
				_length += '_'
		if self.chunkanswer.root():
			return prompt[:prompt.find(_length)] + quiddict[self.chunkanswer.root().ent_type] + prompt[prompt.find(_length) + len(_length):] + "\n" + str(Word(self.chunkanswer.root(), 5,2).distractors())

	

# sentence!
class Sentence:
	#span = abstraction of sentence
	#parent = paragraph
	#c = list of nounchunks in sentence
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

	#displays usage of every word in sentence
	def displayusage(self):
		for w in self.words:

			w.displayusage() 


	#prints sentence

	def display(self):
		s=''
		for w in self.words:
			s+=w.text + " "
		print(s)

#interprets NO
def listdic(lis,inp):
	for dup in lis:
		if dup[0]==inp:
			return dup[1]



class Chunk:
	def __init__(self,span):
		#abstract nounchunk
		self.abstraction=span
		#abstract words in nounchunk
		self.words=[w for w in span]
		#nounchunk string
		self.text=span.text

		self.use()
	def use(self):
		for w in self.words:
			if w.ent_type!=0:
				self.useable=True
				return
		self.useable=False
	def root(self):
		w = self.words[0]
		while w.head in self.words:
			w = w.head
		return w
class NumChunk(Chunk):
	def __init__(self,w):
		self.words=[w]
		self.text=w.text
		self.useable=True


#is not a paragraph

class Paragraph:
	def __init__(self,t):
		self.abstraction=nlp(t)
		self.listchunks()
		self.sentences=[Sentence(s,self,self.findchunksinsentence(s)) for s in self.abstraction.sents]
		
		self.text=self.abstraction.text

	def showblank(self):
		[[print(q.fillblank()) for q in s.questions] for s in self.sentences]
	def showwhat(self):
		[[print(q.fillwhat()) for q in s.questions if q.fillwhat()] for s in self.sentences]
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
		self.entity = token.ent_type
		self.paragraph = paragraph
	def display(self):
		print(self.text)
	def sethead(self,h):
		self.head=h
	def setchildren(self,ch=[]):
		self.children=c
	def addchild(self,c):
		self.children.append(c)
	def displayusage(self):
		print(self.text,self.usage)
	def distractors(self):
		similarity = [t for t in paragraph.abstraction]
		similarity.sort(key = lambda x: self.abstraction.similarity(x))
		similarity.reverse()
		similarity = [t.text for t in similarity if t.pos == self.abstraction.pos]
		newlist = []
		for x in similarity:
			if not (x in newlist):
				newlist.append(x)
		return newlist[:10]


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

