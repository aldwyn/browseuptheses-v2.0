from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class UpdateAccountView(View):

	def get(self, request):
		if request.session.get('f_id') and not request.user.is_superuser:
			password = request.POST['password']
			confirm_password = request.POST['confirm_password']
			if password == confirm_password:
				user_auth = FacultySession.objects.get(pk=request.session['f_id'])
				department = Department.objects.get(pk=request.POST['department'])
				first_name = request.POST['first_name']
				middle_name = request.POST['middle_name']
				last_name = request.POST['last_name']
				username = request.POST['username']
				gender = request.POST['gender']
				new_profile = FacultyProfile(user_auth=user_auth, first_name=first_name, middle_name=middle_name, last_name=last_name, gender=gender, department=department)
				new_profile.save()
				user_auth.username = username
				user_auth.password = password
				user_auth.save()
				return redirect('theses_sys:home')
			else:
				return redirect('theses_sys:set-profile')
		else:
			raise PermissionDenied