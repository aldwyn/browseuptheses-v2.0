
from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *

class SearchView(View):

	def get(self, request, filter, query):
		data = {'filter': filter, 'query': query}
		if request.session.get('f_id'):
			data['f_id'] = request.session['f_id']
			data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
		if request.session.get('alert'):
			data['alert'] = request.session.pop('alert')
		if filter == 'title':
			theses = Thesis.objects.filter(title__icontains=query)
		elif filter == 'tag':
			theses = Thesis.objects.filter(tags__name__icontains=query)
		elif filter == 'category':
			theses = Thesis.objects.filter(category__name__icontains=query)
		elif filter == 'year':
			theses = Thesis.objects.filter(pub_date__year=int(query))
		elif filter == 'department':
			theses = Thesis.objects.filter(faculty__department__name__icontains=query)
		elif filter == 'researcher':
			theses = Thesis.objects.filter(researchers__first_name__icontains=query).filter(researchers__middle_name__icontains=query).filter(researchers__last_name__icontains=query)
		elif filter == 'faculty':
			theses = Thesis.objects.filter(faculty__first_name__icontains=query).filter(faculty__middle_name__icontains=query).filter(faculty__last_name__icontains=query)
		else:
			theses = []
			self.add_to_haystack(theses, query, Thesis.objects.filter(title__icontains=query))
			self.add_to_haystack(theses, query, Thesis.objects.filter(tags__name__icontains=query))
			self.add_to_haystack(theses, query, Thesis.objects.filter(category__name__icontains=query))
			self.add_to_haystack(theses, query, Thesis.objects.filter(faculty__department__name__icontains=query))
			self.add_to_haystack(theses, query, Thesis.objects.filter(researchers__first_name__icontains=query).filter(researchers__middle_name__icontains=query).filter(researchers__last_name__icontains=query))
			self.add_to_haystack(theses, query, Thesis.objects.filter(faculty__first_name__icontains=query).filter(faculty__middle_name__icontains=query).filter(faculty__last_name__icontains=query))
			try:
				self.add_to_haystack(theses, query, Thesis.objects.filter(pub_date__year=int(query)))
			except ValueError:
				pass

		data['theses'] = theses
		return render(request, 'theses_sys/search.html', data)

	def add_to_haystack(self, theses, query, pool):
		for thesis in pool:
			if thesis not in theses:
				theses.append(thesis)



def search_redirect(request):
	filter = request.POST['filter']
	query = request.POST['query']
	return redirect('theses_sys:search', filter=filter, query=query)