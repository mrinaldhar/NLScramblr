from treegen import *
from treeregen import *
import itertools

trees = init('../data/ten_sample.conll')
responses = {}
ofp = open('results', 'w')
for tree in trees[3:4]:
	tree_sort(tree)
	orig_sent = sent_gen(tree, '')
	print
	responses[orig_sent] = []
	aux = [x for x in tree.deps if (x.parentREL.startswith('lwg') or x.parentREL == 'rsym')]
	rest = [x for x in tree.deps if not (x.parentREL.startswith('lwg') or x.parentREL == 'rsym')]
	rest = list(itertools.permutations(rest))
	permutations = []
	for each in rest:
		each1 = list(each)
		each1.extend(aux)
		permutations.append(each1)
	print len(permutations)
	i = 1
	for each in permutations:
		tree.deps = each
		new_sent= sent_gen(tree, '')
		print i, new_sent
		print
		i += 1
		reply = raw_input("Is it right? [0,1] ")
		ofp.write(new_sent+"\t")
		ofp.write(reply+"\n")
		print "="*50
