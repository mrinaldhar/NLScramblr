from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
	name = models.CharField(max_length = 50, unique = True)
	description = models.TextField(default = '')
	participants = models.PositiveIntegerField(default = 0)

	def __unicode__(self):
		return self.name

class Question(models.Model):
	survey = models.ForeignKey(Survey)
	question = models.TextField()

	def __unicode__(self):
		return self.question

class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer = models.TextField() #For subjective questions
	score = models.IntegerField() #For scoring questions
	user = models.OneToOneField(User)

	def __unicode__(self):
		return self.question.id + ' : ' + self.answer.id
