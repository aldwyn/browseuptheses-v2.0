from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *
from math import floor

class HomeView(View):

	def get(self, request):
		data = {}
		data['theses'] = Thesis.objects.all().order_by('title')
		if request.session.get('f_id') and not request.user.is_superuser:
			data['f_id'] = request.session['f_id']
			data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id

			if request.session.get('alert'):
				data['alert'] = request.session.pop('alert')

			terms = []
			for tag in Tag.objects.all():
				count = Thesis.objects.filter(tags=tag).count()
				terms.append({'filter': 'tag', 'query': tag.name, 'count': count})
			for category in Category.objects.all():
				count = Thesis.objects.filter(category=category).count()
				terms.append({'filter': 'category', 'query': category.name, 'count': count})
			maximum = 50
			for term in terms:
				percent = floor((term['count'] / maximum) * 100)
				if percent < 10:
					term['class'] = 'smallest'
				elif percent >= 10 and percent < 30:
					term['class'] = 'small'
				elif percent >= 30 and percent < 50:
					term['class'] = 'medium'
				elif percent >= 50 and percent < 70:
					term['class'] = 'large'
				else:
					term['class'] = 'largest'
			data['terms'] = terms
			return render(request, 'theses_sys/home.html', data)
		else:
			raise PermissionDenied