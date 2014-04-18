from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class SetAccountView(View):

	def get(self, request):
		if request.session.get('f_id') and not request.user.is_superuser:
			data = {}
			data['session'] = FacultySession.objects.get(pk=request.session['f_id'])
			data['profile'] = FacultyProfile.objects.get(user_auth__id=request.session['f_id'])
			data['departments'] = Department.objects.all()
			data['dept_id'] = data['profile'].department.id
			if request.session.get('alert'):
				data['alert'] = request.session.pop('alert')
			data['f_id'] = request.session['f_id']
			data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
			return render(request, 'theses_sys/set-profile.html', data)
		else:
			raise PermissionDenied