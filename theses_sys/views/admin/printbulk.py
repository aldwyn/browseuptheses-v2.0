from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class PrintAccountsView(View):

	def get(self, request):
		if request.session.get('f_id') and not request.user.is_superuser:
			data = {}
			data['accounts'] = FacultySession.objects.filter(pk=acct_id)
			return render(request, 'theses_sys/print.html', data)
		else:
			raise PermissionDenied