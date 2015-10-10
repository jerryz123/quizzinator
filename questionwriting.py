from __future__ import unicode_literals, print_function
from spacy.en import English
def nsubj(ntoken, strsentence):
	subjdict = {
		'person': 'Who',
		'norp': 'Which group',
		'facility': 'Which structure',
		'org': 'Which organization',
		'loc': 'Which place',
		'law': 'Which law'
	}
	text = nounchunk(ntoken)
	if quidnoun(ntoken):
		return strsentence[:strsentence.find(text)] + subjdict[quidnoun(ntoken)] + strsentence[strsentence.find(text) + len(text):]


def quidnoun(t):
	ent = t.ent_type
	word = t.text
	quiddict = {
		0: None,
		28061: 'person',
		1499631: 'norp',
		164860: 'facility',
		202115: 'org',
		85248: 'loc',
		39247: 'law',
	}
	return 

def nounchunk(ntoken):
	sigh = [t.text for t in ntoken.subtree]
	return ' '.join(sigh)