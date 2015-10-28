"""
Utility file with globally required functions
"""

def renumber_chunks(sent):			# Takes one chunked sentence
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

def print_data(sent):
	for chunk in sent:
		for line in chunk:
			print '\t'.join(line)
		print

def dump_data(sent):
	ans = ''
	for chunk in sent:
		for line in chunk:
			ans += '\t'.join(line)
		ans == '\n'

def chunker(sent):			# Requires raw sent.
	sent_parts = sent_breakdown(sent)
	print sent_parts
	sent = sent_parts
	sent_chunks = []
	chunk = []
	old_ch_id = False
	for line in sent:
		if len(line) < 5:
			break
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
	return sent_chunks


def process_piped(line):
	temp_data = line[5].split('|')
	piped_data = {}
	for each in temp_data:
		piped_data[each.split('-')[0]] = each.split('-')[1]
	return piped_data


def readfile(filename):
	fp = open(filename, 'r')
	sents = fp.read().split('\n\n')
	sents.pop()
	return sents

def sent_breakdown(sent):
	parts = []
	for every in sent.split('\n'):
		parts.append(every.split('\t'))
	return parts
