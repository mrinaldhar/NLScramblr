#!/usr/bin/python
# -*- coding: utf-8 -*- 

'''
Script to find sentences
which contain both a and b markers.
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

final_sents = []
sents_parts = []
i = -1
sents = []

def init(filename):
	global sents, i, final_sents, sents_parts
	fp = open(filename, 'r')
	sents = fp.read().split('\n\n')
	sents.pop()
	final_sents = []
	sents_parts = []
	i = -1
	breakdown()

def breakdown():
	global i, sents, sents_parts
	for each in sents:
		i += 1
		sents_parts.append(each.split('\n'))
		parts = []
		for every in sents_parts[i]:
			parts.append(every.split('\t'))
		sents_parts[i] = parts

def separate_a_b_sents(fp, a, b):
	global sents_parts
	sent_a_b = []
	sent_roots = []
	init(fp)
#if a=='k1' and b=='k2':
	rem = []
	for i in xrange(len(sents_parts)):
		for j in xrange(len(sents_parts[i])):
			part = sents_parts[i][j]
			if(part[1] == 'कि'):
				rem.append(sents_parts[i])
				break
	for each in rem:
		sents_parts.remove(each)

	for i in xrange(len(sents_parts)):
		temp = []
		for j in xrange(len(sents_parts[i])):
			part = sents_parts[i][j]
			#print part
			if part[7] == a:
				temp.append(part[6])
			elif part[7] == b and part[6] in temp:
				sent_a_b.append(sents_parts[i])
				sent_roots.append(part[6])
				break
	return (sent_a_b, sent_roots)

if __name__ == "__main__":
	sent_a_b = separate_a_b_sents(sys.argv[1], 'k1', 'k2')
	print sent_a_b
