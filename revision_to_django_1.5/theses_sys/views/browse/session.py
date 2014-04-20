from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class SessionThesesView(View):

	def get(self, request):
		if request.session.get('f_id') and not request.user.is_superuser:
			data = {}
			if request.session.get('alert'):
				data['alert'] = request.session.pop('alert')
			data['f_id'] = request.session['f_id']
			faculty = FacultyProfile.objects.get(user_auth__id=data['f_id'])
			data['faculty'] = faculty
			data['dept_id'] =faculty.department.id
			data['theses'] = Thesis.objects.filter(faculty__user_auth__id=request.session['f_id'])
			return render(request, 'theses_sys/faculty.html', data)
		else:
			raise PermissionDenied