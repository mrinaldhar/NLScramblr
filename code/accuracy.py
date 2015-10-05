'''
Script that measures the accuracy of a parser 
using gold treebank data and comparing with 
parser output.

Checks implemented: 
	1. Multiple assignments.
	2. Wrongly assigned dependencies.
'''

import os, sys, json

class Sentence(object):
	def __init__(self, data):
		self.value = data
		self.process(self.value)

	def process(self, data):
		self.cmpList = []
		for line in data.split('\n'):
			tags = line.split('\t')
			self.cmpList.append(tags[0:2]+tags[-4:])
			try:
				if tags[-3] == 'root' or tags[-3] == 'main':
					self.root = tags[0]
			except: 
				pass
		if self.cmpList == [['']]:
			self.cmpList = [['_', '_', '_', '_', '_', '_']]

def measure():
	num_error = 0
	num_totalChecks = 0
	sents_GOLD = []
	sents_TEST = []
	errors = {}
	num_wrong = 0
	total_sents = 0
	for i in xrange(len(fileList_GOLD)):
		fp = open(dir_GOLD+fileList_GOLD[i], 'r')
		data_GOLD = fp.read()
		fp = open(dir_TEST+fileList_TEST[i], 'r')
		data_TEST = fp.read()
		data_GOLD = data_GOLD.split('\n\n')
		data_TEST = data_TEST.split('\n\n')
		data_GOLD = [x for x in data_GOLD if x != '']
		data_TEST = [x for x in data_TEST if x != '']
		assert(len(data_GOLD) == len(data_TEST))
		for x in xrange(len(data_GOLD)):
			sent_GOLD = Sentence(data_GOLD[x])
			sent_TEST = Sentence(data_TEST[x])
			sents_GOLD.append(sent_GOLD)
			sents_TEST.append(sent_TEST)	
			cmp_GOLD = sent_GOLD.cmpList
			cmp_TEST = sent_TEST.cmpList
			# errors[sent_GOLD.value] = {"dep":[], "multiple":[]}
			errors[sent_GOLD.value] = {}
			sentence_tags = {}
			num_totalChecks += len(cmp_GOLD)

			for j in xrange(len(cmp_GOLD)):
				flag = True
				for k in xrange(1, 6):
					cmp_TEST[j][k] = cmp_TEST[j][k].strip('%')
					if k==2 and cmp_GOLD[j][k] == 'main':
						cmp_GOLD[j][k] = 'root'
					if flag and cmp_GOLD[j][k] != cmp_TEST[j][k]:
						num_error += 1
						dist_TEST = int(sent_TEST.root) - int(cmp_TEST[j][0])
						dist_GOLD = int(sent_GOLD.root) - int(cmp_GOLD[j][0])
						errors[sent_GOLD.value]['\t'.join(cmp_TEST[j])] = [dist_TEST, dist_GOLD]
						# errors[sent_GOLD.value]["dep"].append((cmp_GOLD[j][k], cmp_TEST[j][k]))
				if sentence_tags.has_key((cmp_TEST[j][1], cmp_TEST[j][2])):
					num_wrong += 1
					# errors[sent_GOLD.value]["multiple"].append((cmp_TEST[j][1], cmp_TEST[j][2]))
					# print cmp_TEST[j][0], sentence_tags[(cmp_TEST[j][1], cmp_TEST[j][2])], cmp_TEST[j][2]
				else:
					sentence_tags[(cmp_TEST[j][1], cmp_TEST[j][2])] = cmp_TEST[j][0]
	print 
	print "="*50
	print " "*16, "Parser Accuracy"
	print "-"*50
	print "Dependency Error percentage: ",
	print 100.0*num_error/num_totalChecks
	print
	print "Multiple Error percentage: ",
	print 100.0*num_wrong/num_totalChecks
	print "="*50
	print
	return errors

if __name__=="__main__":
	if len(sys.argv) != 6:
		print "USAGE: python accuracy.py [-f | -d; file or directory] [GOLD data file or dir] [TEST data file or dir] [OUTPUT report file] [INPUT sentence file]"
		exit(0)
	inp = open(sys.argv[5], 'r')
	orig_sent = Sentence(inp.read())
	run_mode = sys.argv[1]
	reportFile = open(sys.argv[4], 'w')
	dir_GOLD = sys.argv[2]
	dir_TEST = sys.argv[3]
	if run_mode == '-d':
		fileList_GOLD = sorted(os.listdir(dir_GOLD))
		fileList_TEST = sorted(os.listdir(dir_TEST))
	elif run_mode == '-f':
		fileList_GOLD = ['']
		fileList_TEST = ['']
	assert(len(fileList_TEST) == len(fileList_GOLD))
	errors = measure()
	reportFile.write(json.dumps(errors))
	reportFile.close()
	print "Report has been stored to this file:", sys.argv[4]