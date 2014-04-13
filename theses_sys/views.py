from django.shortcuts import render
from theses_sys.models import Thesis, FacultyProfile, Researcher, Department, Tag, Category

def index(request):
	theses = Thesis.objects.all().order_by('title')
	return render(request, 'theses_sys/index.html', {'theses': theses})

def add_thesis(request):
	return render(request, 'theses_sys/add_thesis.html')