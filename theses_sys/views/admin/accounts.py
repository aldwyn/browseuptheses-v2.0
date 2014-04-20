from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class AccountsView(View):

	def get(self, request):
		data = {'accounts': [], 'user': request.user}
		if request.user.is_superuser:
			if request.session.get('alert'):
				data['alert'] = request.session.pop('alert')
			accounts = FacultySession.objects.all()
			for account in accounts:
				profile = FacultyProfile.objects.filter(user_auth=account)
				if profile:
					data['accounts'].append({'account': account, 'profile': profile[0], 'thesis_count': Thesis.objects.filter(faculty=profile).count()})
				else:
					data['accounts'].append({'account': account, 'profile': '', 'thesis_count': 0})
			return render(request, 'theses_sys/admin.html', data)
		else:
			raise PermissionDenied