def renumber_chunks(sent):
	count = 1
	renumber = {'0': '0'}
	for k in xrange(len(sent)):
		chunk = sent[k]
		for j in xrange(len(chunk)):
			word = chunk[j]
			if int(word[0]) != count:
				renumber[word[0]] = str(count)
			else:
				renumber[word[0]] = word[0]
			word[0] = str(count)
			count += 1
