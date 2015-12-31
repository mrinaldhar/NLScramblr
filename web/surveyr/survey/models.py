from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
	name = models.CharField(max_length = 50, unique = True)
	description = models.TextField(default = '')

	def __unicode__(self):
		return self.name

class Question(models.Model):
	survey = models.ForeignKey(Survey)
	question = models.TextField()

	class Meta:
		unique_together = (("survey", "question"),)
	
	def __unicode__(self):
		return self.question

class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer = models.TextField(default = '') #For subjective questions
	score = models.IntegerField(default = 0) #For scoring questions
	user = models.ForeignKey(User)

	class Meta:
		unique_together = (("answer", "user"),)

	def __unicode__(self):
		return str(self.question.id) + ' : ' + self.answer
