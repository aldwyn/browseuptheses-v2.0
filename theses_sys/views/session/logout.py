from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class LogoutView(View):

	def get(self, request):
		if request.session.get('f_id') and not request.user.is_superuser:
			request.session.pop('f_id')
			request.session['alert'] = 'You have been logged out.'
			return redirect('theses_sys:login')
		else:
			raise PermissionDenied