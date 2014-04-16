from theses_sys.models import Thesis, FacultySession, FacultyProfile, Researcher, Department, Tag, Category, Tags_Added
from django.contrib.auth.models import BaseUserManager
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.http import HttpResponse

def index(request):
	return render(request, 'theses_sys/index.html')

def show_home(request):
	data = {'theses': Thesis.objects.all().order_by('title'), 'f_id': ''}
	if request.session['f_id']:
		data['f_id'] = request.session['f_id']
	return render(request, 'theses_sys/home.html', data)

def show_login(request):
	return render(request, 'theses_sys/login.html')

def show_admin(request):
	data = {'accounts': []}
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

def show_session_theses(request):
	theses = Thesis.objects.filter(faculty__user_auth__id=request.session['f_id'])
	return render(request, 'theses_sys/faculty_theses.html', {'theses': theses})

def show_faculty_theses(request, username):
	theses = Thesis.objects.filter(faculty__user_auth__username=username)
	faculty = FacultyProfile.objects.get(user_auth__username=username)
	return render(request, 'theses_sys/faculty_theses.html', {'theses': theses, 'faculty': faculty})

def show_department_theses(request, department_id):
	theses = Thesis.objects.filter(faculty__department__id=department_id)
	department = Department.objects.get(pk=department_id)
	return render(request, 'theses_sys/department_theses.html', {'theses': theses, 'department': department})

def search(request, filter, query):
	if filter == 'tag':
		theses = Thesis.objects.filter(tags__name__contains=query)
	elif filter == 'category':
		theses = Thesis.objects.filter(category__name__contains=query)
	elif filter == 'department':
		theses = Thesis.objects.filter(faculty__department__name__contains=query)
	elif filter == 'researcher':
		theses = Thesis.objects.filter(researchers__first_name__contains=query).filter(researchers__middle_name__contains=query).filter(researchers__last_name__contains=query)
	elif filter == 'faculty':
		theses = Thesis.objects.filter(faculty__first_name__contains=query).filter(faculty__middle_name__contains=query).filter(faculty__last_name__contains=query)
	else:
		theses = Thesis.objects.filter(tags__name__contains=query).filter(category__name__contains=query).filter().filter(faculty__department__name__contains=query).filter(researchers__first_name__contains=query).filter(researchers__middle_name__contains=query).filter(researchers__last_name__contains=query).filter(faculty__first_name__contains=query).filter(faculty__middle_name__contains=query).filter(faculty__last_name__contains=query)
	return render(request, 'theses_sys/search.html', {'filter': filter, 'query': query, 'theses': theses})

def show_thesis_info(request, slug):
	thesis = get_object_or_404(Thesis, slug=slug)
	return render(request, 'theses_sys/thesis_info.html', {'thesis': thesis})

def generate_accounts(request):
	quantity = int(request.GET['quantity'])
	entry_count = FacultySession.objects.all().count()
	for i in list(range(entry_count, quantity + entry_count)):
		password = BaseUserManager().make_random_password(length=7, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789')
		new_account = FacultySession(username='UPCFACULTY'+str(i), password=password)
		new_account.save()
	request.session['alert'] = 'Admin successfully added ' + str(quantity) + ' accounts.'
	return redirect('theses_sys:admin')

def print_account(request, acct_id):
	return render(request, 'theses_sys/print.html', {'accounts': FacultySession.objects.filter(pk=acct_id)})

def print_accounts(request):
	accounts = request.POST.getlist('acct_id')
	list_to_print = []
	for acct_id in accounts:
		list_to_print.append(FacultySession.objects.get(pk=acct_id))
	return render(request, 'theses_sys/print.html', {'accounts': list_to_print})

def delete_account(request, acct_id):
	to_delete = FacultySession.objects.get(pk=acct_id)
	to_delete.delete()
	request.session['alert'] = 'You deleted ' + to_delete.username + '.'
	return redirect('theses_sys:admin')

def delete_accounts(request):
	accounts = request.POST.getlist('acct_id')
	size = len(accounts)
	for acct_id in accounts:
		to_delete = FacultySession.objects.get(pk=acct_id)
		to_delete.delete()
	request.session['alert'] = 'You deleted ' + str(size) + ' accounts.'
	return redirect('theses_sys:admin')

def create_user_session(request):
	username = request.POST['username']
	password = request.POST['password']
	user = FacultySession.objects.get(username=username, password=password)
	if user:
		request.session['f_id'] = user.id
		profile = FacultyProfile.objects.filter(user_auth=user)
		if not profile:
			return redirect('theses_sys:set_profile')
		else:
			return redirect('theses_sys:home')
	else:
		return render(request, 'theses_sys/login.html', {'alert': 'Incorrect username/password.'})

def create_entry(request):
	data = {'alert': ''}
	if request.session['f_id']:
		data['categories'] = Category.objects.all()
		if request.session.get('alert'):
			data['alert'] = request.session.pop('alert')
		return render(request, 'theses_sys/create_entry.html', data)
	else:
		return redirect('theses_sys:login')

def delete_entry(request):
	return redirect('theses_sys:')

def show_set_profile(request):
	session = FacultySession.objects.get(pk=request.session['f_id'])
	profile = FacultyProfile.objects.filter(user_auth__id=request.session['f_id'])
	departments = Department.objects.all()
	if profile:
		data = {'session': session, 'profile': profile, 'departments': departments}
	else:
		data = {'session': session, 'departments': departments}
	return render(request, 'theses_sys/set_profile.html', data)

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
		return redirect('theses_sys:home')
	else:
		return redirect('theses_sys:set_profile')

def add_thesis(request):
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

		return redirect('theses_sys:thesis_info', slug=new_thesis.slug)
	else:
		request.session['alert'] = 'There is an existing thesis with the same title/abstract you provided.'
		return redirect('theses_sys:create_entry')