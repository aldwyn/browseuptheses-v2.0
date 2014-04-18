from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class ThesisView(View):

	def get(self, request, slug):
		data = {}
		if request.session.get('alert'):
			data['alert'] = request.session.pop('alert')
		if request.session.get('f_id'):
			data['f_id'] = request.session['f_id']
			data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
		data['thesis'] = Thesis.objects.get(slug=slug)
		return render(request, 'theses_sys/thesis.html', data)