from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class PrintAccountView(View):

	def get(self, request, acct_id):
		if request.session.get('f_id') and not request.user.is_superuser:
			data = {}
			accounts = request.POST.getlist('acct_id')
			list_to_print = []
			for acct_id in accounts:
				list_to_print.append(FacultySession.objects.get(pk=acct_id))
			data['accounts'] = list_to_print
			return render(request, 'theses_sys/print.html', data)
		else:
			PermissionDenied