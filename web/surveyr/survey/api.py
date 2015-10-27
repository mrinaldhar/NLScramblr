from survey.models import Question, Answer


def parse_question(question):

	return {
		'id' : question.id,
		'question' : question.question
	}

def next_question(user, survey):
	for question in survey.question_set.all():
		flag = True
		for answer in question.answer_set.all():
			if user == answer.user:
				flag = False
				break
		if flag:
		 	return parse_question(question)

def parse_survey(survey):
	return {
		'id': survey.id,
		'name' : survey.name,
		'desc' : survey.description,
		'nop' : survey.participants
	}

def survey_list():
	surveys = []
	for each in Survey.objects.all():
		surveys.append(parse_survey(each))
	return surveys

