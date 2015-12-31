from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.generic import View
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.db import transaction

import django.contrib.auth as auth

import json
from survey.api import *
from survey.models import *
from django.contrib.auth.models import User


def index(request):
	data = {
			'surveys' : survey_list(),
			'user': request.user,
			'request': request
			}
	return render_to_response('survey/index.html', context_instance=RequestContext(request, data))

def home(request):
	data = {
			'user': request.user,
			'request': request
			}

	return render_to_response('survey/home.html', context_instance=RequestContext(request, data))

def logout(request):
	auth.logout(request)
	return redirect('index')

class login(View):
	template_name = 'survey/login.html'

	def post(self, request, *args, **kwargs):
		response = {'status' : 0}
		login_data = request.POST
		user = None
		try:
			uname = login_data['username']
			password = login_data['password']
		except:
			response['status'] = 1
			response['message'] = 'Missing details in form.'
			return HttpResponse(json.dumps(response), content_type="application/json")	
		user = auth.authenticate(username = uname, password = password)
		if user:
			auth.login(request, user)
		else:
			response['status'] = 1
			response['message'] = 'The credentials you entered were invalid.'
		return HttpResponse(json.dumps(response), content_type="application/json")
		
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('index')
		return render_to_response(self.template_name, context_instance=RequestContext(request))

class signup(View):
	def post(self, request, *args, **kwargs):
		response = {'status' : 0}
		user_data = request.POST
		try:
			with transaction.atomic():
				username = user_data['username']
				if ' ' in username or username == '':
					raise Exception('Invalid username!') 
				password = user_data['password']
				user = User(
					username = username
					)
				user.set_password(password)
				user.save()
		except Exception as e:
			transaction.rollback()
			response['status'] = 1
			response['message'] = str(e[0])
		return HttpResponse(json.dumps(response), content_type="application/json")

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('index')
		return redirect('/accounts/login#signup')

class question(View):	
	def get(self, request, *args, **kwargs):
		response = {'status' : 0}
		survey_id = request.GET.get('survey', '')
		if survey_id:
			survey = get_object_or_404(Survey, pk = survey_id)
			response['data'] = next_question(request.user, survey)
		else:
			response['status'] = 1
			response['message'] = 'Missing parameter : survey id'
		return HttpResponse(json.dumps(response), content_type="application/json")

class answer(View):
	def post(self, request, *args, **kwargs):
		response = {'status' : 0}
		question_id = request.POST.get('question', '')
		answer = request.POST.get('answer', '')
		if question_id and answer:
			question = get_object_or_404(Question, pk = question_id)
			if save_answer(request.user, question, answer):
				response['data'] = 'Success'
			else:
				response['status'] = 1
				response['data'] = 'Failure'
		else:
			response['status'] = 1
			response['message'] = 'Missing parameters : question and/or answer'
		return HttpResponse(json.dumps(response), content_type="application/json")

class progress(View):
	def get(self, request, *args, **kwargs):
		response   = {'status' : 0}	
		survey_id = request.GET.get('survey', '')
		if survey_id:
			survey = get_object_or_404(Survey, pk = survey_id)
			progress = 0
			total = len(survey.question_set.all())
			for question in survey.question_set.all():
				for answer in question.answer_set.all():
					if answer.user == request.user:
						progress += 1
						break
			response['data'] = {'total' : total, 'completed' : progress}
		else:
			response['status'] = 1
			response['message'] = 'Missing parameter : survey id'
		return HttpResponse(json.dumps(response), content_type="application/json")
