from theses_sys.models import Thesis, FacultySession, FacultyProfile, Researcher, Department, Tag, Category, Tags_Added
from django.contrib.auth.models import BaseUserManager, User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.http import HttpResponse
from math import floor

def index(request):
	return render(request, 'theses_sys/index.html')

def show_home(request):
	data = {}
	data['theses'] = Thesis.objects.all().order_by('title')
	if request.session.get('f_id') and not request.user.is_superuser:
		data['f_id'] = request.session['f_id']
		data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
		if request.session.get('alert'):
			data['alert'] = request.session.pop('alert')
		terms = []
		for tag in Tag.objects.all():
			terms.append({'filter': 'tag', 'query': tag.name, 'count': Thesis.objects.filter(tags=tag).count()})
		for category in Category.objects.all():
			terms.append({'filter': 'category', 'query': category.name, 'count': Thesis.objects.filter(category=category).count()})
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

def show_login(request):
	data = {}
	if request.session.get('alert'):
		data['alert'] = request.session.pop('alert')
	if not request.session.get('f_id') and not request.user.is_superuser:
		return render(request, 'theses_sys/login.html', data)
	elif request.session.get('f_id') and not request.user.is_superuser:
		return redirect('theses_sys:home')
	else:
		raise PermissionDenied

def show_admin(request):
	data = {'accounts': []}
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

def show_session_theses(request):
	if request.session.get('f_id') and not request.user.is_superuser:
		data = {}
		if request.session.get('alert'):
			data['alert'] = request.session.pop('alert')
		data['f_id'] = request.session['f_id']
		faculty = FacultyProfile.objects.get(user_auth__id=data['f_id'])
		data['faculty'] = faculty
		data['dept_id'] =faculty.department.id
		data['theses'] = Thesis.objects.filter(faculty__user_auth__id=request.session['f_id'])
		return render(request, 'theses_sys/faculty.html', data)
	else:
		raise PermissionDenied

def show_faculty_theses(request, username):
	if request.session.get('f_id') and not request.user.is_superuser:
		data = {}
		if request.session.get('alert'):
			data['alert'] = request.session.pop('alert')
		data['theses'] = Thesis.objects.filter(faculty__user_auth__username=username)
		data['faculty'] = FacultyProfile.objects.get(user_auth__username=username)
		data['f_id'] = request.session['f_id']
		data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
		return render(request, 'theses_sys/faculty.html', data)
	else: 
		raise PermissionDenied

def show_department_theses(request, department_id):
	data = {}
	data['theses'] = Thesis.objects.filter(faculty__department__id=department_id)
	data['department'] = Department.objects.get(pk=department_id)
	if request.session.get('alert'):
		data['alert'] = request.session.pop('alert')
	if request.session.get('f_id') and not request.user.is_superuser:
		data['f_id'] = request.session['f_id']
		data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
		return render(request, 'theses_sys/department.html', data)
	else:
		raise PermissionDenied

def show_search(request, filter, query):
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
		theses_list = []
		theses = Thesis.objects.filter(title__icontains=query).filter(tags__name__icontains=query).filter(category__name__icontains=query).filter().filter(faculty__department__name__icontains=query).filter(researchers__first_name__icontains=query).filter(researchers__middle_name__icontains=query).filter(researchers__last_name__icontains=query).filter(faculty__first_name__icontains=query).filter(faculty__middle_name__icontains=query).filter(faculty__last_name__icontains=query)
	data['theses'] = theses
	return render(request, 'theses_sys/search.html', data)

def show_thesis_info(request, slug):
	data = {}
	if request.session.get('alert'):
		data['alert'] = request.session.pop('alert')
	if request.session.get('f_id'):
		data['f_id'] = request.session['f_id']
		data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
	data['thesis'] = Thesis.objects.get(slug=slug)
	return render(request, 'theses_sys/thesis_info.html', data)

def show_set_profile(request):
	if request.session.get('f_id') and not request.user.is_superuser:
		data = {}
		data['session'] = FacultySession.objects.get(pk=request.session['f_id'])
		data['profile'] = FacultyProfile.objects.get(user_auth__id=request.session['f_id'])
		data['departments'] = Department.objects.all()
		data['dept_id'] = data['profile'].department.id
		if request.session.get('alert'):
			data['alert'] = request.session.pop('alert')
		data['f_id'] = request.session['f_id']
		data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
		return render(request, 'theses_sys/set_profile.html', data)
	else:
		raise PermissionDenied

def show_print_account(request, acct_id):
	if request.session.get('f_id') and not request.user.is_superuser:
		data = {}
		data['accounts'] = FacultySession.objects.filter(pk=acct_id)
		return render(request, 'theses_sys/print.html', data)
	else:
		raise PermissionDenied

def show_print_accounts(request):
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

def show_create_entry(request):
	if request.session.get('f_id') and not request.user.is_superuser:
		data = {}
		data['process'] = 0
		data['categories'] = Category.objects.all()
		if request.session.get('f_id') and not request.user.is_superuser:
			data['f_id'] = request.session['f_id']
			data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
		if request.session.get('alert'):
			data['alert'] = request.session.pop('alert')
		return render(request, 'theses_sys/entry.html', data)
	else:
		raise PermissionDenied

def show_edit_entry(request, thesis_id):
	if request.session.get('f_id') and not request.user.is_superuser:
		data = {}
		data['process'] = 1
		data['thesis'] = Thesis.objects.get(pk=thesis_id)
		data['categories'] = Category.objects.all()
		chunks = []
		for chunk in data['thesis'].tags.all():
			chunks.append(chunk.name)
		categories_joined = ', '.join(chunks)
		data['categories_joined'] = categories_joined
		if request.session.get('f_id') and not request.user.is_superuser:
			data['f_id'] = request.session['f_id']
			data['dept_id'] = FacultyProfile.objects.get(user_auth__id=data['f_id']).department.id
		if request.session.get('alert'):
			data['alert'] = request.session.pop('alert')
		return render(request, 'theses_sys/entry.html', data)
	else:
		raise PermissionDenied

def logout(request):
	if request.session.get('f_id') and not request.user.is_superuser:
		request.session.pop('f_id')
		request.session['alert'] = 'You have been logged out.'
		return redirect('theses_sys:login')
	else:
		raise PermissionDenied

def generate_accounts(request):
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

def delete_account(request, acct_id):
	if not request.session.get('f_id') and request.user.is_superuser:
		to_delete = FacultySession.objects.get(pk=acct_id)
		to_delete.delete()
		request.session['alert'] = 'You deleted ' + to_delete.username + '.'
		return redirect('theses_sys:admin')
	else:
		raise PermissionDenied

def delete_accounts(request):
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

def create_user_session(request):
	if not request.session.get('f_id') and not request.user.is_superuser:
		username = request.POST['username']
		password = request.POST['password']
		user = FacultySession.objects.filter(username=username, password=password)
		if user:
			request.session['f_id'] = user[0].id
			profile = FacultyProfile.objects.filter(user_auth=user[0])
			if not profile:
				return redirect('theses_sys:set_profile')
			else:
				return redirect('theses_sys:home')
		else:
			request.session['alert'] = 'Incorrect username/password.'
			return redirect('theses_sys:login')
	else:
		raise PermissionDenied

def delete_entry(request, thesis_id):
	if request.session.get('f_id') and not request.user.is_superuser:
		to_delete = get_object_or_404(Thesis, pk=thesis_id)
		to_delete.delete()
		request.session['alert'] = str(to_delete.title) + ' successfully deleted.'
		return redirect('theses_sys:session_theses')
	else:
		raise PermissionDenied

def update_profile(request):
	if request.session.get('f_id') and not request.user.is_superuser:
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
	else:
		raise PermissionDenied

def add_entry(request):
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

			return redirect('theses_sys:thesis_info', slug=new_thesis.slug)
		else:
			request.session['alert'] = 'There is an existing thesis with the same title/abstract you provided.'
			return redirect('theses_sys:create_entry')
	else:
		raise PermissionDenied

def update_entry(request, thesis_id):
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
				return redirect('theses_sys:thesis_info', slug=new_thesis.slug)
			else:
				request.session['alert'] = 'There is an existing thesis with the same title/abstract you provided.'
				return redirect('theses_sys:edit_entry', thesis_id=thesis_id)
	else:
		raise PermissionDenied

def redirect_to_search(request):
	filter = request.POST['filter']
	query = request.POST['query']
	return redirect('theses_sys:search', filter=filter, query=query)