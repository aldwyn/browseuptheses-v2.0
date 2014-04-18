from django.conf.urls import patterns, url
from theses_sys.views import *

# account
urlpatterns = patterns('',
	url(r'^set-profile/$', account.edit.SetAccountView.as_view(), name='set-profile'),
	url(r'^update-profile/$', account.edit.update, name='update-profile'),
)

# admin
urlpatterns += patterns('',
	url(r'^admin/$', admin.accounts.AccountsView.as_view(), name='admin'),
	url(r'^generate-accounts/$', admin.backends.generate, name='generate-accounts'),
	url(r'^print-account/(?P<acct_id>\d+)/$', admin.backends.printone, name='print-account'),
	url(r'^delete-account/(?P<acct_id>\d+)/$', admin.backends.delete, name='delete-account'),
	url(r'^print-accounts/$', admin.backends.printbulk, name='print-accounts'),
	url(r'^delete-accounts/$', admin.backends.delbulk, name='delete-accounts'),
)

# browse
urlpatterns += patterns('',
	url(r'^$', browse.index.IndexView.as_view(), name='index'),
	url(r'^home/$', browse.home.HomeView.as_view(), name='home'),
	url(r'^my-domain/$', browse.session.SessionThesesView.as_view(), name='session-theses'),
	url(r'^faculty-theses/(?P<username>\w+)/$', browse.faculty.FacultyThesesView.as_view(), name='faculty-theses'),
	url(r'^department-theses/(?P<department_id>\d+)/$', browse.department.DepartmentThesesView.as_view(), name='department-theses'),
	url(r'^redirect-to-search/$', browse.search.redirect, name='redirect-to-search'),
	url(r'^search/(?P<filter>[a-zA-Z0-9_\- ]+)/(?P<query>[a-zA-Z0-9_\- ]+)/$', browse.search.SearchView.as_view(), name='search'),
)

# session
urlpatterns += patterns('',
	url(r'^login/$', session.login.LoginView.as_view(), name='login'),
	url(r'^create-user-session/$', session.backends.create, name='create-user-session'),
	url(r'^logout/$', session.backends.logout, name='logout'),
)

# thesis
urlpatterns += patterns('',
	url(r'^thesis/(?P<slug>[a-zA-Z0-9_\-]+)/$', thesis.show.ThesisView.as_view(), name='thesis'),
	url(r'^add-entry/$', thesis.backends.add, name='add-entry'),
	url(r'^delete-entry/(?P<thesis_id>\d+)/$', thesis.backends.delete, name='delete-entry'),
	url(r'^update-entry/(?P<thesis_id>\d+)/$', thesis.backends.update, name='update-entry'),
	url(r'^edit-entry/(?P<thesis_id>\d+)/$', thesis.edit.EditEntryView.as_view(), name='edit-entry'),
	url(r'^create-entry/$', thesis.create.CreateEntryView.as_view(), name='create-entry'),
)