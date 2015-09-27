#! /usr/bin/python

import operator

def sent_gen(root, sent):

	'''
	Given a dependency structure tree
	regenerates the surface form.
	'''

	for dep in root.deps:
		if not (dep.parentREL.startswith('lwg') or dep.parentREL == 'rsym'):
			sent = sent_gen(dep, sent)

	sent += root.value[1] + ' ' 

	for dep in root.deps:
		if (dep.parentREL.startswith('lwg') or dep.parentREL == 'rsym'):
			sent = sent_gen(dep, sent)
	
	return sent

def tree_sort(root):

	'''
	Given a dependency structure tree
	sorts the branches by sentence id
	'''
	root.deps.sort(key=operator.attrgetter('ID'))
	for dep in root.deps:
		tree_sort(dep)
