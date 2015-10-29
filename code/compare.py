import separatr as sep
import sys
import treegen as tree
def makeTree(sent):
	lines = {'0':'0'}
	rels = {}
	for line in sent:
		lines[line[0]] = line[1]
	for line in sent:
		parent = line[6]
		rel = line[7]
		rels[line[1]+lines[parent]+rel] = 1 
	
	return rels

def compare(sen1, sen2):
	tree1 = makeTree(sen1)
	tree2 = makeTree(sen2)
	if len(tree1.keys()) != len(tree2.keys()):
		print "HI"
		return 0
	for each in tree1.keys():
		if each not in tree2.keys():
#print each 
			return 0
	return 1

if __name__=="__main__":
	sep.init(sys.argv[1])
	sents1 = sep.sents_parts
	sep.init(sys.argv[2])
	sents2 = sep.sents_parts
	correct = 0
	total = len(sents1)
	for i in xrange(total):
		result = compare(sents1[i], sents2[i])
		correct += result
		if result == 0:
			tree.print_data([sents1[i]])
			tree.print_data([sents2[i]])
	print "Accuracy: ", 100.0*correct/total
	'''
	for sent in sents:
		tree = makeTree(sent)
		for each in tree.keys():
			print each
			for every in tree[each]:
				print "\t", every
			print "="*50
	'''
