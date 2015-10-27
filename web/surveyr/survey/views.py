from django.shortcuts import render_to_response
from django.views.generic import View
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
import json

from django.http import HttpResponse

def home(request):
	return render_to_response('survey/index.html', context_instance=RequestContext(request, {'user': request.user, 'request': request}))

class login(View):
	template_name = 'survey/login.html'

	@method_decorator(csrf_protect)
	def post(self, request, *args, **kwargs):
		response = {'status' : 0}
		login_data = request.POST
		user = None
		try:
			uname = login_data['uname']
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
	
	@method_decorator(ensure_csrf_cookie)	
	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return redirect('home')
		return render_to_response(self.template_name, context_instance=RequestContext(request))

class signup(View):
	@method_decorator(csrf_protect)
	def post(self, request, *args, **kwargs):
		response = {'status' : 0}
		user_data = request.POST
		try:
			with transaction.atomic():
				username = user_data['username']
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
			return redirect('home')
		return redirect('/accounts/login#signup')


class surveys(View):
	'''
		AJAX endpoint to get questions
		and post answers
	'''

	def get(self, request, *args, **kwargs):
		pass	
