from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

def create(request):
	if not request.session.get('f_id') and not request.user.is_superuser:
		username = request.POST['username']
		password = request.POST['password']
		user = FacultySession.objects.filter(username=username, password=password)
		if user:
			request.session['f_id'] = user[0].id
			profile = FacultyProfile.objects.filter(user_auth=user[0])
			if not profile:
				return redirect('theses_sys:set-profile')
			else:
				return redirect('theses_sys:home')
		else:
			request.session['alert'] = 'Incorrect username/password.'
			return redirect('theses_sys:login')
	else:
		raise PermissionDenied

def logout(request):
	if request.session.get('f_id') and not request.user.is_superuser:
		request.session.pop('f_id')
		request.session['alert'] = 'You have been logged out.'
		return redirect('theses_sys:login')
	else:
		raise PermissionDenied