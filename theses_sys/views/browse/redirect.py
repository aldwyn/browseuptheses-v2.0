from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class SearchRedirectView(View):

	def get(self, request):
		filter = request.POST['filter']
		query = request.POST['query']
		return redirect('theses_sys:search', filter=filter, query=query)