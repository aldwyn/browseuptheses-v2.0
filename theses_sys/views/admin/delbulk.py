from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class DeleteAccountsView(View):

	def get(self, request):
		if not request.session.get('f_id') and request.user.is_superuser:
			accounts = request.POST.getlist('acct_id')
			size = len(accounts)
			for acct_id in accounts:
				to_delete = FacultySession.objects.get(pk=acct_id)
				to_delete.delete()
			request.session['alert'] = 'You deleted ' + str(size) + ' accounts.'
			return redirect('theses_sys:admin')
		else:
			raise PermissionDenied