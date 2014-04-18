from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class CreateSessionView(View):

	def get(self, request):
		return HttpResponse('Hey')
		if not request.session.get('f_id') and not request.user.is_superuser:
			username = request.POST['username']
			password = request.POST['password']
			user = FacultySession.objects.filter(username=username, password=password)
			if user:
				request.session['f_id'] = user[0].id
				profile = FacultyProfile.objects.filter(user_auth=user[0])
				if not profile:
					return redirect('theses_sys:set-profile')
				else:
					return redirect('theses_sys:home')
			else:
				request.session['alert'] = 'Incorrect username/password.'
				return redirect('theses_sys:login')
		else:
			raise PermissionDenied