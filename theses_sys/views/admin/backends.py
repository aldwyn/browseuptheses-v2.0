from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import BaseUserManager
from theses_sys.models import *

def delbulk(request):
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

def delete(request, acct_id):
	if not request.session.get('f_id') and request.user.is_superuser:
		to_delete = FacultySession.objects.get(pk=acct_id)
		to_delete.delete()
		request.session['alert'] = 'You deleted ' + to_delete.username + '.'
		return redirect('theses_sys:admin')
	else:
		raise PermissionDenied

def generate(request):
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

def printbulk(request):
	if request.session.get('f_id') and not request.user.is_superuser:
		data = {}
		data['accounts'] = FacultySession.objects.filter(pk=acct_id)
		return render(request, 'theses_sys/print.html', data)
	else:
		raise PermissionDenied

def printone(request, acct_id):
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