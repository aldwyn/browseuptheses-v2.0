from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *
from django.contrib.auth.models import BaseUserManager

class GenerateAccountsView(View):

	def get(self, request):
		if not request.session.get('f_id') and request.user.is_superuser:
			quantity = int(request.GET['quantity'])
			entry_count = FacultySession.objects.all().count()
			allowed_chars = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789'
			for i in list(range(entry_count, quantity + entry_count)):
				password = BaseUserManager().make_random_password(length=7, allowed_chars=allowed_chars)
				new_account = FacultySession(username='UPCFACULTY'+str(i), password=password)
				new_account.save()
			request.session['alert'] = 'Admin successfully added ' + str(quantity) + ' accounts.'
			return redirect('theses_sys:admin')
		else:
			raise PermissionDenied