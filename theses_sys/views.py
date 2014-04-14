from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import signals
from theses_sys.models import Thesis, FacultyProfile, Researcher, Department, Tag, Category

def index(request):
	theses = Thesis.objects.all().order_by('title')
	return render(request, 'theses_sys/index.html', {'theses': theses})

def create_user(request, quantity):
	for i in range(quantity):
		user = User.objects.create_user('john', 'kdjgd')
		user.save()

def show_login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = get_object_or_404(User, username=username)

def show_session_theses(request):
	theses = Thesis.objects.all().order_by('title')
	return render(request, 'theses_sys/index.html', {'theses': theses})

def show_faculty_theses(request, faculty_id):
	theses = Thesis.objects.filter(faculty__user_auth__id=faculty_id)
	return render(request, 'theses_sys/faculty_theses.html', {'theses': theses})

def show_department_theses(request, department_id):
	theses = Thesis.objects.filter(faculty__department__id=department_id)
	return render(request, 'theses_sys/department_theses.html', {'theses': theses})

def search(request, filter, query):
	if filter is 'tag':
		theses = Thesis.objects.filter(tags__name__contains=query)
	elif filter is 'category':
		theses = Thesis.objects.filter(categories__name__contains=query)
	elif filter is 'department':
		theses = Thesis.objects.filter(faculty__department__name__contains=query)
	elif filter is 'researcher':
		theses = Thesis.objects.filter(researchers__first_name__contains=query).filter(researchers__middle_name__contains=query).filter(researchers__last_name__contains=query)
	elif filter is 'faculty':
		theses = Thesis.objects.filter(faculty__first_name__contains=query).filter(faculty__middle_name__contains=query).filter(faculty__last_name__contains=query)
	else:
		theses = Thesis.objects.filter(tags__name__contains=query).filter(categories__name__contains=query).filter().filter(faculty__department__name__contains=query).filter(researchers__first_name__contains=query).filter(researchers__middle_name__contains=query).filter(researchers__last_name__contains=query).filter(faculty__first_name__contains=query).filter(faculty__middle_name__contains=query).filter(faculty__last_name__contains=query)
	return render(request, 'theses_sys/search.html', {'theses': theses})

def show_thesis_info(request, thesis_id):
	thesis = get_object_or_404(Thesis, pk=thesis_id)
	session = request.session.session_key
	return render(request, 'theses_sys/thesis_info.html', {'thesis': thesis, 'session': session})

def create_entry(request):
	categories = Category.objects.all()
	return render(request, 'theses_sys/create_entry.html', {'categories': categories})

def add_thesis(request):
	thesis = {}
	thesis['title'] = request.POST['title']
	thesis['abstract'] = request.POST['abstract']
	thesis['faculty'] = request.session
	thesis['tags'] = request.POST['tags'].split(',')
	thesis['category'] = request.POST['category']
	thesis['pub_date'] = request.POST['pub_date']
	thesis['pub_date'] = request.POST['acc_date']

	# thesis['researchers'] = request.POST['researchers']

	# res_list = []
	# for researcher in researchers:
	# 	new_researcher = Researcher(
	# 			first_name = researcher.first_name,
	# 			middle_name = researcher.middle_name,
	# 			last_name = researcher.last_name
	# 		)
	# 	new_researcher.save()
	# 	res_list.append(new_researcher.id)

	# tag_list = []
	# for tag in tags:
	# 	new_tag = Tag(name=tag.name)
	# 	new_tag.save()
	# 	tag_list.append(new_tag.id)

	# cat_list = []
	# for category in categories:
	# 	new_category = Category(name=category.name)
	# 	new_category.save()
	# 	cat_list.append(new_category.id)

	# new_theses = Thesis(title=title, abstract=abstract, )
	return render(request, 'theses_sys/thesis_info.html', {'thesis': thesis})
