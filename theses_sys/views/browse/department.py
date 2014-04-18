from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class DepartmentThesesView(View):

	def get(self, request, department_id):
		data = {}
		data['theses'] = Thesis.objects.filter(faculty__department__id=department_id)
		data['department'] = Department.objects.get(pk=department_id)
		if request.session.get('alert'):
			data['alert'] = request.session.pop('alert')
		if request.session.get('f_id') and not request.user.is_superuser:
			data['f_id'] = request.session['f_id']
			data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
			return render(request, 'theses_sys/department.html', data)
		else:
			raise PermissionDenied