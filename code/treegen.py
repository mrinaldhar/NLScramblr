'''
Generates a dependency tree 
given a sentence in conll
'''

import separatr as sep
import sys

class Node(object):
	def __init__(self):
		self.deps = []
		self.value = []
		self.ID = 0
		self.parentID = 0
		self.parentREL = 0

#	def __lt__(self, other):
#		return self.ID < other.ID

	def addNewDep(self, depNode):
		self.deps.append(depNode)

def print_data(sents):
	for sent in sents:
		for line in sent:
			print line[1],
	print

def print_tree(node, level):
	print "\t"*level, node.value[1]
	for each in node.deps:
		print_tree(each, level+1)

def putInPlace(root, node):
	if node.parentID == root.ID:
		root.addNewDep(node)
		return True
	for each in root.deps:
		success = putInPlace(each, node)
		if success == True:
			return True

def makeTree(sent):
	nodes = {}
	rootNode = 0
	for x in xrange(len(sent)):
		line = sent[x]
		node = Node()
		node.ID = int(line[0])
		node.parentID = int(line[6])
		node.value = line
		node.parentREL = line[7]
		if node.parentID == 0:
			rootNode = node.ID
		if nodes.has_key(node.parentID):
			nodes[node.parentID].addNewDep(node)
		else:
			nodes[node.ID] = node
	x = len(nodes.keys())
	while (x > 1):
		deletion = []
		for each in nodes.keys():
			for every in nodes.keys():
				if each!=every and each!=rootNode:
					success = putInPlace(nodes[every], nodes[each])
					if success == True:
						deletion.append(each)
						break
		for each in deletion:
			del nodes[each]
		x = len(nodes.keys())
	for each in nodes.keys():
		return nodes[each]

def init(filename):
	sep.init(filename)
	sents = sep.sents_parts
	trees = []
	for sent in sents:
		tree = makeTree(sent)
		trees.append(tree)
	return trees

if __name__=="__main__":
	trees = init(sys.argv[1])
	for each in trees:
		print_tree(each, 0)
		print "="*100

