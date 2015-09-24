'''
Generates a dependency tree 
given a sentence in conll
'''

import separatr as sep
import sys

class Node(object):
	def __init__(self):
		self.deps = []
		self.parentNode = []
		self.value = []
		self.ID = 0
		self.parentID = 0
		self.parentREL = 0

	def addNewDep(self, depNode):
		self.deps.append(depNode)

	def childOf(self, parent):
		self.parentNode = parent

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
#	print "Trying for ", node.value[1]
#	print "Comparing ", node.parentID, " + ", root.ID
	if node.parentID == root.ID:
#		print "Placed:: ", node.value[1], " under ", root.value[1]
		root.addNewDep(node)
		return True
	for each in root.deps:
		putInPlace(each, node)

def makeTree(sent):
	nodes = {}
	rootNode = 0
	for x in xrange(len(sent)):
		line = sent[x]
		node = Node()
		node.ID = line[0]
		node.parentID = line[6]
		node.value = line
		node.parentREL = line[7]
		if node.parentID == '0':
			rootNode = node.ID
		if nodes.has_key(node.parentID):
			nodes[node.parentID].addNewDep(node)
		else:
			nodes[node.ID] = node
#	print "Phase 1:"
#	print nodes
#	for each in nodes.keys():
#		print_tree(nodes[each], 0)
	x = len(nodes.keys())
	while (x > 1):
		deletion = []
		for each in nodes.keys():
			for every in nodes.keys():
				if each!=every:
					success = putInPlace(nodes[every], nodes[each])
					if success == True:
						deletion.append(each)
						break
		for each in deletion:
			del nodes[each]
		x = len(nodes.keys())
#	print "Nodes:", nodes
	return nodes[rootNode]
#	print "+"*50
#	print "Phase 2:"
#	print nodes
#	for each in nodes.keys():
#		return nodes[each]
def init(filename):
	sep.init(filename)
	sents = sep.sents_parts
	trees = []
	for sent in sents:
		tree = makeTree(sent)
		trees.append(tree)
		print_data([sent])
		print_tree(tree, 0)
		print "="*100
	print trees
if __name__=="__main__":
	init(sys.argv[1])
