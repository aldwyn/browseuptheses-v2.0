from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class DeleteAccountView(View):

	def get(self, request, acct_id):
		if not request.session.get('f_id') and request.user.is_superuser:
			to_delete = FacultySession.objects.get(pk=acct_id)
			to_delete.delete()
			request.session['alert'] = 'You deleted ' + to_delete.username + '.'
			return redirect('theses_sys:admin')
		else:
			raise PermissionDenied