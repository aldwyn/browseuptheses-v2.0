from django.conf.urls import patterns, url
from theses_sys import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^home/$', views.show_home, name='home'),
	url(r'^login/$', views.show_login, name='login'),
	url(r'^admin/$', views.show_admin, name='admin'),
	url(r'^thesis_added/$', views.add_thesis, name='add_thesis'),
	url(r'^create_entry/$', views.create_entry, name='create_entry'),
	url(r'^show_set_profile/$', views.show_set_profile, name='show_set_profile'),
	url(r'^update_profile/$', views.update_profile, name='update_profile'),
	url(r'^search/(?P<filter>\w+)/(?P<query>\w+)/$', views.search, name='search'),
	url(r'^getting_started/$', views.create_user_session, name='create_user_session'),
	url(r'^department_theses/(?P<department_id>\d+)/$', views.show_department_theses, name='department_theses'),
	url(r'^faculty_theses/(?P<username>\w+)/$', views.show_faculty_theses, name='faculty_theses'),
	url(r'^thesis/(?P<thesis_id>\d+)/$', views.show_thesis_info, name='thesis_info'),
)
