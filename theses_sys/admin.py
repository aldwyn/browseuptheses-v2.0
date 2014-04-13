from django.contrib import admin
from theses_sys.models import Researcher, Department, FacultyReg, FacultyProfile, Tag, Category, Thesis

class ThesisAdmin(admin.ModelAdmin):
	list_display = ('title', 'pub_date')

admin.site.register(Thesis, ThesisAdmin)