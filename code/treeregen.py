#!/usr/bin/python
# -*- coding: utf-8 -*- 

import operator

def sent_gen(root, sent):

	'''
	Given a dependency structure tree
	regenerates the surface form.
	'''

	for dep in root.deps:
		if not (dep.parentREL.startswith('lwg') or dep.parentREL.startswith('rsym')):
			sent = sent_gen(dep, sent)

	sent += '\t'.join(root.value) + '\n' 

	for dep in root.deps:
		if (dep.parentREL.startswith('lwg') or dep.parentREL.startswith('rsym')):
			sent = sent_gen(dep, sent)
	
	return sent

def shuffle_vb(root):

	'''
	Given a dependency structure tree
	regenerates several surface forms
	by moving the verb.
	'''

	def make_sent(root, before, after, sent):
		for dep in before:
			sent = sent_gen(dep, sent)
		sent += '\t'.join(root.value) + '\n'
		for dep in root.deps:
			if (dep.parentREL.startswith('lwg') or dep.parentREL.startswith('rsym') and dep.value[1] != '।'):
				sent = sent_gen(dep, sent)
		for dep in after:
			sent = sent_gen(dep, sent)
		for dep in root.deps:
			if dep.value[1] == '।':
				sent = sent_gen(dep, sent)
		
		return sent

	sents = []
	vb_args = [dep for dep in root.deps if not (dep.parentREL.startswith('lwg') or dep.parentREL.startswith('rsym'))]
	for i in xrange(len(vb_args)+1):
		before = vb_args[:i]
		after = vb_args[i:]
		sents.append(make_sent(root, before, after, ''))
	return sents


def tree_sort(root):

	'''
	Given a dependency structure tree
	sorts the branches by sentence id
	'''

	root.deps.sort(key=operator.attrgetter('ID'))
	for dep in root.deps:
		tree_sort(dep)
