'''
	Extract sentences from the
	treebank of a given size
'''

import sys

def extract(sents, size):
	for sent in sents:
		words = sent.split('\n')
		if len(words) == size:
			print sent
			print


if __name__=="__main__":
	if len(sys.argv) != 3:
		print "Usage: python extract.py <size>"
	f = open(sys.argv[1], 'r')
	data = f.read().split('\n\n')
	data = [x for x in data if x != '']
	size = int(sys.argv[2])
	extract(data, size)
