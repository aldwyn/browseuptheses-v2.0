from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class CreateEntryView(View):

	def get(self, request):
		if request.session.get('f_id') and not request.user.is_superuser:
			data = {}
			data['process'] = 0
			data['categories'] = Category.objects.all()
			if request.session.get('f_id') and not request.user.is_superuser:
				data['f_id'] = request.session['f_id']
				data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
			if request.session.get('alert'):
				data['alert'] = request.session.pop('alert')
			return render(request, 'theses_sys/entry.html', data)
		else:
			raise PermissionDenied