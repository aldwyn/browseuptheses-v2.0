from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class EditEntryView(View):

	def get(self, request, thesis_id):
		if request.session.get('f_id') and not request.user.is_superuser:
			data = {}
			data['process'] = 1
			data['thesis'] = Thesis.objects.get(pk=thesis_id)
			data['categories'] = Category.objects.all()
			chunks = []
			for chunk in data['thesis'].tags.all():
				chunks.append(chunk.name)
			categories_joined = ', '.join(chunks)
			data['categories_joined'] = categories_joined
			if request.session.get('f_id') and not request.user.is_superuser:
				data['f_id'] = request.session['f_id']
				data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
			if request.session.get('alert'):
				data['alert'] = request.session.pop('alert')
			return render(request, 'theses_sys/entry.html', data)
		else:
			raise PermissionDenied