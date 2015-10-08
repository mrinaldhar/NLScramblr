from django.shortcuts import render
from django.views.generic import View
from django.template import RequestContext
import json

from django.http import HttpResponse

def home(request):
	return HttpResponse("HELLO")
	return render_to_response('survey/index.html', context_instance=RequestContext(request))

class survey(View):
	'''
		AJAX endpoint to get questions
		and post answers
	'''

	def get(self, request, *args, **kwargs):
		pass
	
