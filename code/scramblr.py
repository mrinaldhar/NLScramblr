"""
Scrambles the given rels in the 
sentences in the input data....
"""

import sys
from separatr import separate_a_b_sents as sep

def scrambler(chunked_sents, l1, l2):
	for sent in chunked_sents:
		#IDENTIFY ROOT ID
		root_id = ''
		for chunk in sent:
			for word in chunk:
				if word[7] == 'root':
					root_id = word[0]
					break
			if root_id:
				break
	
		#FIND l1 & l2 CHUNKS
		chunk_l1 = -1
		chunk_l2 = -1
		for k in xrange(len(sent)):
			chunk = sent[k]
			for j in xrange(len(chunk)):
				word = chunk[j]
				if word[7] == l1 and word[6] == root_id:
					chunk_l1 = k
				if word[7] == l2 and word[6] == root_id:
					chunk_l2 = k
		
		#INTERCHANGE CHUNKS
		temp = sent[chunk_l1]
		sent[chunk_l1] = sent[chunk_l2]
		sent[chunk_l2] = temp

		#RENUMBER
		count = 1
		renumber = {'0': '0'}
		for k in xrange(len(sent)):
			chunk = sent[k]
			for j in xrange(len(chunk)):
				word = chunk[j]
				if int(word[0]) != count:
					renumber[word[0]] = str(count)
				else:
					renumber[word[0]] = word[0]
				word[0] = str(count)
				count += 1
		
		for k in xrange(len(sent)):
			chunk = sent[k]
			for j in xrange(len(chunk)):
				word = chunk[j]
				word[6] = renumber[word[6]]
	return chunked_sents

def print_data(sents):
	for sent in sents:
		for chunk in sent:
			for line in chunk:
				print '\t'.join(line)
		print

def process_piped(line):
	temp_data = line[5].split('|')
	piped_data = {}
	for each in temp_data:
		piped_data[each.split('-')[0]] = each.split('-')[1]
	return piped_data

def chunker(sents):
	for x in xrange(len(sents)):
		sent = sents[x]
		sent_chunks = []
		chunk = []
		old_ch_id = False
		for line in sent:
			piped_data = process_piped(line)	
			ch_id = piped_data['chunkId']
			if (old_ch_id == False):
				old_ch_id = ch_id
			if (old_ch_id == ch_id):
				chunk.append(line)
			else:
				old_ch_id = ch_id
				sent_chunks.append(chunk)
				chunk = []
				chunk.append(line)
		if len(chunk) != 0:
		  	sent_chunks.append(chunk)
		  	chunk = []
		sents[x] = sent_chunks
	return sents

if __name__ == "__main__":
	l1 = sys.argv[2]
	l2 = sys.argv[3]
	sents = sep(sys.argv[1], l1, l2)
	chunked_sents = chunker(sents)
#print_data(chunked_sents)
	scrambled_sents = scrambler(chunked_sents, l1, l2)
	print_data(scrambled_sents)
