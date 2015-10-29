from survey.models import Survey, Question, Answer
import utils
import json
import compare


def survey_list():
	return Survey.objects.all()

def parse_question(question):
	chunk_dict = {'id' : question.id}
	question = utils.chunker(question.question)
	for i in xrange(len(question)):
		chunk_dict[i] = question[i]
	return json.dumps(chunk_dict)

def next_question(user, survey):
	for question in survey.question_set.all():
		flag = True
		for answer in question.answer_set.all():
			if user == answer.user:
				flag = False
				break
		if flag:
		 	return parse_question(question)
	return ''

def save_answer(user, question, answer):
	chunk_dict = json.loads(answer)
	utils.renumber_chunks(chunk_dict)
	answer = utils.dump_data(chunk_dict)
#	if not compare.compare(utils.sent_breakdown(question.question), utils.sent_breakdown(answer)):
#		return False
	if answer == question.question:
		return False
	final = Answer(question = question,
			answer = answer,
			user = user)
	final.save()
	return True
