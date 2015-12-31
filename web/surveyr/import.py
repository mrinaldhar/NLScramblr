import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'surveyr.settings'

from survey.models import *

f = open('../../data/len_15.conll', 'r')
data = f.read()
sents = [x for x in data.split('\n\n') if x]

s = Survey(name = 'Scramble Generations', description = 'To study common scramble structures')
s.save()

for sent in sents:
	q = Question(survey = s, question = sent)
	q.save()
