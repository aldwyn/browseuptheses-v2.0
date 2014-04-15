from django.contrib import admin
from theses_sys.models import Researcher, Department, FacultyProfile, FacultySession, Tag, Category, Thesis, Tags_Added

class TagsAddedInline(admin.TabularInline):
	model = Tags_Added
	extra = 1

class ThesisAdmin(admin.ModelAdmin):
	inlines = [TagsAddedInline]
	list_filter = ['pub_date']
	list_display = ('title', 'pub_date')
	search_fields = ['title', 'researcher', 'faculty', 'tags', 'categories']

class ResearcherAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'middle_name')
	search_fields = ['last_name', 'first_name', 'middle_name']

class FacultySessionAdmin(admin.ModelAdmin):
	list_display = ('username', 'password', 'date_last_login')
	search_fields = ['username']

class FacultyProfileAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'middle_name')
	search_fields = ['last_name', 'first_name', 'middle_name']

class DepartmentAdmin(admin.ModelAdmin):
	search_fields = ['name']

class TagAdmin(admin.ModelAdmin):
	search_fields = ['name']

class CategoryAdmin(admin.ModelAdmin):
	search_fields = ['name']

admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Researcher, ResearcherAdmin)
admin.site.register(FacultyProfile, FacultyProfileAdmin)
admin.site.register(FacultySession, FacultySessionAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)