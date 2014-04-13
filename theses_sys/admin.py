from django.contrib import admin
from theses_sys.models import Researcher, Department, FacultyProfile, Tag, Category, Thesis

class ThesisAdmin(admin.ModelAdmin):
	list_display = ('title', 'pub_date')

class ResearcherAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'middle_name')

class FacultyProfileAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'middle_name')

admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Researcher, ResearcherAdmin)
admin.site.register(FacultyProfile, FacultyProfileAdmin)
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Tag)