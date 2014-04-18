from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *

class IndexView(View):
	
	def get(self, request):
		return render(request, 'theses_sys/index.html')