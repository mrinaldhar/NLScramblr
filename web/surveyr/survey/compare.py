'''
	Rudimentary script to compare
	if two trees are the same
'''

def makeTree(sent):
	lines = {'0':'0'}
	rels = {}
	for line in sent:
		#print line
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
		return 0
	for each in tree1.keys():
		if each not in tree2.keys():
			return 0
	return 1