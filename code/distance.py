#! /usr/bin/python

'''
	Script to calculate distance and sign
	of incorrectly parsed sents
'''
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import json

f = open(sys.argv[1], 'r')

data = f.read()
data = json.loads(data)

for scrm in data:
	print scrm
	print '-'*30
	for each in data[scrm]:
		print each, '\t', data[scrm][each]
	print
	print '='*50
	print