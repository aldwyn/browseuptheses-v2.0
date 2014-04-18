from django.views.generic.base import View
from django.http import HttpResponse
from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *
from django.utils.text import slugify

class AddEntryView(View):

	def get(self, request):
		if request.session.get('f_id') and not request.user.is_superuser:
			title = request.POST['title']
			abstract = request.POST['abstract']
			existing_thesis = Thesis.objects.filter(slug=slugify(title)).filter(abstract=abstract)

			if not existing_thesis:
				slug = slugify(title)
				tags = request.POST['tags'].split(',')
				faculty = FacultyProfile.objects.get(pk=request.session['f_id'])
				category = Category.objects.get(pk=request.POST['category'])
				pub_date = request.POST['pub_date']
				acc_date = request.POST['acc_date']
				res_first_name = request.POST.getlist('res_first_name')
				res_middle_name = request.POST.getlist('res_middle_name')
				res_last_name = request.POST.getlist('res_last_name')

				new_thesis = Thesis(title=title, slug=slug, abstract=abstract, faculty=faculty, category=category, pub_date=pub_date, acc_date=acc_date)
				new_thesis.save()

				for i in list(range(len(res_first_name))):
					new_researcher = Researcher(first_name=res_first_name[i],middle_name=res_middle_name[i],last_name=res_last_name[i])
					new_researcher.save()
					new_thesis.researchers.add(new_researcher)
					new_thesis.save()

				for tag in tags:
					new_tag = Tag(name=tag.strip())
					new_tag.save()
					tag_fk = Tags_Added(tag=new_tag, thesis=new_thesis)
					tag_fk.save()

				return redirect('theses_sys:thesis', slug=new_thesis.slug)
			else:
				request.session['alert'] = 'There is an existing thesis with the same title/abstract you provided.'
				return redirect('theses_sys:create-entry')
		else:
			raise PermissionDenied