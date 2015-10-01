from treegen import *
from treeregen import *
from scramblr import chunker, print_data, process_piped
import separatr as sep
import itertools

import json

def pretty_print(sent):
	for chunk in sent:
		for each in chunk:
			print each[1],
	print

index = 0

def print_sent(new_sent):
	sep.sents = [new_sent]
	sep.i = -1
	sep.sents_parts = []
	sep.breakdown()
	sep.sents_parts[-1].pop()

	sent = sep.sents_parts
	sent = chunker(sent)[0]
	count = 1
	renumber = {'0': '0'}
	ctype = {}
	for k in xrange(len(sent)):
		chunk = sent[k]
		d = process_piped(chunk[0])
		result = ''.join([i for i in d['chunkId'] if not i.isdigit()])
		ctype[result] = ctype.get(result, 0) + 1
		num = ctype[result]
		if num == 1:
			num = ''
		else:
			num = str(num)

		for j in xrange(len(chunk)):
			word = chunk[j]
			if int(word[0]) != count:
				renumber[word[0]] = str(count)
			else:
				renumber[word[0]] = word[0]
			word[0] = str(count)
			count += 1
			d = process_piped(word)
			d['chunkId'] = result + num
			feats = [each+'-'+d[each] for each in d.keys()]
			word[5] = '|'.join(feats)

	
	for k in xrange(len(sent)):
		chunk = sent[k]
		for j in xrange(len(chunk)):
			word = chunk[j]
			word[6] = renumber[word[6]]
	global index
	pretty_print(sent)
	resp = raw_input('[0, 1, 2] : ')
	while resp not in ['0', '1', '2']:
		pretty_print(sent)
		resp = raw_input('[0, 1, 2] : ')
	responses[new_sent] = resp
	index += 1
	if (index % 2 == 0):
		f.seek(0)
		f.write(json.dumps(responses))
	#print_data([sent])

trees = init('../data/one_sample/one_sample.conll')
f = open('response.txt', 'w')
responses = {}

for tree in trees:
	tree_sort(tree)
	orig_sent = sent_gen(tree, '')
	aux = [x for x in tree.deps if (x.parentREL.startswith('lwg') or x.parentREL == 'rsym')]
	rest = [x for x in tree.deps if not (x.parentREL.startswith('lwg') or x.parentREL == 'rsym')]
	rest = list(itertools.permutations(rest))
	permutations = []
	for each in rest:
		each1 = list(each)
		each1.extend(aux)
		permutations.append(each1)

	for each in permutations:
		tree.deps = each
		new_sents= shuffle_vb(tree)
		#new_sents= [sent_gen(tree, '')]
		for new_sent in new_sents:
			print_sent(new_sent)

f.write(json.dumps(responses))
f.close()
