from django.shortcuts import *
from django.core.exceptions import PermissionDenied
from theses_sys.models import *
from django.utils.text import slugify

def add(request):
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

def delete(request, thesis_id):
	if request.session.get('f_id') and not request.user.is_superuser:
		to_delete = Thesis.objects.get(pk=thesis_id)
		to_delete.delete()
		request.session['alert'] = str(to_delete.title) + ' successfully deleted.'
		return redirect('theses_sys:session-theses')
	else:
		raise PermissionDenied

def update(request, thesis_id):
	if request.session.get('f_id') and not request.user.is_superuser:
		title = request.POST['title']
		abstract = request.POST['abstract']
		existing_thesis = Thesis.objects.filter(slug=slugify(title)).filter(abstract=abstract)

		if existing_thesis:
			if existing_thesis[0].id == int(thesis_id):
				slug = slugify(title)
				tags = request.POST['tags'].split(',')
				faculty = FacultyProfile.objects.get(pk=request.session['f_id'])
				category = Category.objects.get(pk=request.POST['category'])
				pub_date = request.POST['pub_date']
				acc_date = request.POST['acc_date']
				res_first_name = request.POST.getlist('res_first_name')
				res_middle_name = request.POST.getlist('res_middle_name')
				res_last_name = request.POST.getlist('res_last_name')

				new_thesis = Thesis.objects.get(pk=thesis_id)
				Thesis.objects.filter(pk=thesis_id).update(title=title, slug=slug, abstract=abstract, faculty=faculty, category=category, pub_date=pub_date, acc_date=acc_date)
				new_thesis.researchers.clear()
				new_thesis.tags.clear()

				for i in list(range(len(res_first_name))):
					existing_researcher = Researcher.objects.filter(first_name=res_first_name[i], middle_name=res_middle_name[i], last_name=res_last_name[i])
					if not existing_researcher:
						new_researcher = Researcher(first_name=res_first_name[i], middle_name=res_middle_name[i], last_name=res_last_name[i])
						new_researcher.save()
						new_thesis.researchers.add(new_researcher)
					else:
						new_thesis.researchers.add(existing_researcher[0])
					new_thesis.save()

				for tag in tags:
					existing_tag = Tag.objects.filter(name=tag)
					if not existing_tag:
						new_tag = Tag(name=tag.strip())
						new_tag.save()
						tag_fk = Tags_Added(tag=new_tag, thesis=new_thesis)
						tag_fk.save()
					else:
						tag_fk = Tags_Added(tag=existing_tag[0], thesis=new_thesis)
						tag_fk.save()
				request.session['alert'] = '"' + str(new_thesis.title) + '" was successfully updated.'
				return redirect('theses_sys:thesis', slug=new_thesis.slug)
			else:
				request.session['alert'] = 'There is an existing thesis with the same title/abstract you provided.'
				return redirect('theses_sys:edit-entry', thesis_id=thesis_id)
	else:
		raise PermissionDenied