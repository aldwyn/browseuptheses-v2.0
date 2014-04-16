from django.conf.urls import patterns, url
from theses_sys import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^home/$', views.show_home, name='home'),
	url(r'^login/$', views.show_login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^admin/$', views.show_admin, name='admin'),
	url(r'^thesis_added/$', views.add_thesis, name='add_thesis'),
	url(r'^create_entry/$', views.create_entry, name='create_entry'),
	url(r'^set_profile/$', views.show_set_profile, name='set_profile'),
	url(r'^update_profile/$', views.update_profile, name='update_profile'),
	url(r'^generate_accounts/$', views.generate_accounts, name='generate_accounts'),
	url(r'^print_account/(?P<acct_id>\d+)/$', views.print_account, name='print_account'),
	url(r'^print_accounts/$', views.print_accounts, name='print_accounts'),
	url(r'^delete_account/(?P<acct_id>\d+)/$', views.delete_account, name='delete_account'),
	url(r'^delete_accounts/$', views.delete_accounts, name='delete_accounts'),
	url(r'^search/(?P<filter>\w+)/(?P<query>\w+)/$', views.search, name='search'),
	url(r'^my_domain/$', views.show_session_theses, name='session_theses'),
	url(r'^getting_started/$', views.create_user_session, name='create_user_session'),
	url(r'^department_theses/(?P<department_id>\d+)/$', views.show_department_theses, name='department_theses'),
	url(r'^faculty_theses/(?P<username>\w+)/$', views.show_faculty_theses, name='faculty_theses'),
	url(r'^thesis/(?P<slug>[a-zA-Z0-9_\-]+)/$', views.show_thesis_info, name='thesis_info'),
)
