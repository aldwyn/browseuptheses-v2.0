from django.shortcuts import render, get_object_or_404
from theses_sys.models import Thesis, FacultyProfile, Researcher, Department, Tag, Category

def index(request):
	theses = Thesis.objects.all().order_by('title')
	return render(request, 'theses_sys/index.html', {'theses': theses})

def thesis_info(request, thesis_id):
	thesis = get_object_or_404(Thesis, pk=thesis_id)
	return render(request, 'theses_sys/thesis_info.html', {'thesis': thesis})

def create_entry(request):
	return render(request, 'theses_sys/create_entry.html')

def add_thesis(request):
	