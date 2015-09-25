"""
Scrambles the given rels in the 
sentences in the input data....
"""

import sys
import separatr as sep
import itertools

def head(chunk):
	for each in chunk:
		feats = process_piped(each)
		if feats['chunkType'] == 'head':
			return each[0]
	return -1

def ids(chunk):
	ids = []
	for each in chunk:
		ids.append(each[0])
	return ids

def move_chunk(sent, chunk_l1, chunk_l2, reln):
	sen_len = len(sent)
	ids1 = ids(sent[chunk_l1])
	ids2 = ids(sent[chunk_l2])
	dep_1 = dep_2 = -1
	for k in xrange(sen_len):
		chunk = sent[k]
		for j in xrange(len(chunk)):
			word = chunk[j]
			if word[7] == reln and word[6] in ids1:
				dep_1 = k
			elif word[7] == reln and word[6] in ids2:
				dep_2 = k
	if dep_1 != -1:
		chunk = sent[dep_1]
		sent[dep_1] = []
		sent.insert(chunk_l1, chunk)
		sent.remove([])
		if dep_1 > chunk_l1:
			chunk_l1 += 1
		dep_1 = -1
	if dep_2 != -1:
		chunk = sent[dep_2]
		sent[dep_2] = []
		sent.insert(chunk_l2, chunk)
		sent.remove([])
		if dep_2 > chunk_l2:
			chunk_l2 += 1
		dep_2 = -1
	return (sent, chunk_l1, chunk_l2)

def gen_plaintext_sents(sents):
	plain_sents = []
	for sent in sents:
		new_sent = []
		for chunk in sent:
			for line in chunk:
				new_sent.append(line[1])
		plain_sents.append("".join(new_sent))
	return plain_sents

def scrambler(chunked_sents):
	new_chunked_sents = []
	for i in xrange(len(chunked_sents)):
		sent = chunked_sents[i][:-1]
		new_sents = list(itertools.permutations(sent))
		for x in xrange(len(new_sents)):
			new_sents[x] = list(new_sents[x])
			new_sents[x].append(chunked_sents[i][-1])
		new_chunked_sents.extend(new_sents)
		#IDENTIFY ROOT ID
		'''
		for chunk in sent:
			for word in chunk:
				if word[7] == 'root':
					root_id = word[0]
					break
			if root_id:
				break
		'''
		'''
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

		if chunk_l1 != -1 and chunk_l2 != -1:
			#INTERCHANGE CHUNKS
			temp = sent[chunk_l1]
			sent[chunk_l1] = sent[chunk_l2]
			sent[chunk_l2] = temp

			#MOVE R6 DEPENDENTS
			sent, chunk_l1, chunk_l2 = move_chunk(sent, chunk_l1, chunk_l2, 'r6')
			sent, chunk_l1, chunk_l2 = move_chunk(sent, chunk_l1, chunk_l2, 'nmod')

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
		'''
	return new_chunked_sents

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
	sep.init(sys.argv[1])
	sents = sep.sents_parts
	chunked_sents = chunker(sents)
#print_data(chunked_sents)
	scrambled_sents = scrambler(chunked_sents)
#print_data(scrambled_sents)
	plain_sents = gen_plaintext_sents(scrambled_sents)
	for each in plain_sents:
		print each
