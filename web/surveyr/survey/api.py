from survey.models import Survey, Question, Answer
import utils
import json

def survey_list():
	return Survey.objects.all()

def parse_question(question):
	question = utils.chunker(question)
	chunk_dict = {}
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

def save_answer(user, question, answer):
	question = Question.objects.get(id=question)
	chunk_dict = json.loads(answer)
	utils.renumber_chunks(chunk_dict)
	answer = utils.dump_data(chunk_dict)
	final = Answer(question = question,
			answer = answer,
			user = user)
	Answer.save()
