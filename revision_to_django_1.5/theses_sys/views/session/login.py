from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class LoginView(View):

	def get(self, request):
		data = {}
		if request.session.get('alert'):
			data['alert'] = request.session.pop('alert')
		if not request.session.get('f_id') and not request.user.is_superuser:
			return render(request, 'theses_sys/login.html', data)
		elif request.session.get('f_id') and not request.user.is_superuser:
			return redirect('theses_sys:home')
		else:
			raise PermissionDenied