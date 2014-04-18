from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class DeleteEntryView(View):

	def get(self, request, thesis_id):
		if request.session.get('f_id') and not request.user.is_superuser:
			to_delete = Thesis.objects.get(pk=thesis_id)
			to_delete.delete()
			request.session['alert'] = str(to_delete.title) + ' successfully deleted.'
			return redirect('theses_sys:session-theses')
		else:
			raise PermissionDenied