from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from theses_sys.models import Thesis, FacultySession, FacultyProfile, Researcher, Department, Tag, Category, Tags_Added

def index(request):
	return render(request, 'theses_sys/index.html')

def home(request):
	theses = Thesis.objects.all().order_by('title')
	return render(request, 'theses_sys/home.html', {'theses': theses})

def create_user(request, quantity):
	for i in range(quantity):
		user = User.objects.create_user('john', 'kdjgd')
		user.save()

def show_login(request):
	return render(request, 'theses_sys/login.html')

def create_user_session(request):
	username = request.POST['username']
	password = request.POST['password']
	user = FacultySession.objects.get(username=username, password=password)
	if user:
		request.session['f_id'] = user.id
		profile = FacultyProfile.objects.filter(user_auth=user)
		if not profile:
			data = {
				'session': user,
				'departments': Department.objects.all(),
				'alert': 'Set your profile first.'
			}
			return render(request, 'theses_sys/set_profile.html', data)
		else:
			return render(request, 'theses_sys/home.html', {'thesis': Thesis.objects.all().order_by('add_date')[:10]})
	else:
		return render(request, 'theses_sys/login.html', {'alert': 'Incorrect username/password.'})

def show_session_theses(request):
	theses = Thesis.objects.all().order_by('title')
	return render(request, 'theses_sys/index.html', {'theses': theses})

def show_faculty_theses(request, username):
	theses = Thesis.objects.filter(faculty__user_auth__username=username)
	faculty = FacultyProfile.objects.get(user_auth__username=username)
	return render(request, 'theses_sys/faculty_theses.html', {'theses': theses, 'faculty': faculty})

def show_department_theses(request, department_id):
	theses = Thesis.objects.filter(faculty__department__id=department_id)
	department = Department.objects.get(pk=department_id)
	return render(request, 'theses_sys/department_theses.html', {'theses': theses, 'department': department})

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
	return render(request, 'theses_sys/create_entry.html', {'categories': Category.objects.all()})

def show_set_profile(request):
	session = FacultySession.objects.get(pk=request.session['f_id'])
	profile = FacultyProfile.objects.get(user_auth=session)
	departments = Department.objects.all()
	return render(request, 'theses_sys/set_profile.html', {'session': session, 'profile': profile, 'departments': departments})

def update_profile(request):
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
		return render(request, 'theses_sys/home.html', {'theses': Thesis.objects.all()})
	else:
		data = {
			'session': FacultySession.objects.get(pk=request.session['f_id']),
			'departments': Department.objects.all(),
			'alert': 'Passwords mismatched.'
		}
		return render(request, 'theses_sys/set_profile.html', data)

def add_thesis(request):
	title = request.POST['title']
	abstract = request.POST['abstract']
	tags = request.POST['tags'].split(',')
	faculty = FacultyProfile.objects.get(pk=request.session['f_id'])
	category = Category.objects.get(pk=request.POST['category'])
	pub_date = request.POST['pub_date']
	acc_date = request.POST['acc_date']
	res_first_name = request.POST.getlist('res_first_name')
	res_middle_name = request.POST.getlist('res_middle_name')
	res_last_name = request.POST.getlist('res_last_name')

	new_thesis = Thesis(title=title, abstract=abstract, faculty=faculty, category=category, pub_date=pub_date, acc_date=acc_date)
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

	return render(request, 'theses_sys/thesis_info.html', {'thesis': new_thesis})