from django.conf.urls import patterns, url
from theses_sys import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^create_entry/$', views.create_entry, name='create_entry'),
	url(r'^(?P<thesis_id>\d+)/thesis_info/$', views.thesis_info, name='thesis_info'),
)
