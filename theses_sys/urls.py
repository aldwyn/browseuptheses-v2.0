from django.conf.urls import patterns, url
from theses_sys import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^show_login/$', views.show_login, name='show_login'),
	url(r'^add_thesis/$', views.add_thesis, name='add_thesis'),
	url(r'^create_entry/$', views.create_entry, name='create_entry'),
	url(r'^(?P<department_id>\d+)/department_theses/$', views.show_department_theses, name='show_department_theses'),
	url(r'^(?P<thesis_id>\d+)/thesis_info/$', views.show_thesis_info, name='show_thesis_info'),
)
