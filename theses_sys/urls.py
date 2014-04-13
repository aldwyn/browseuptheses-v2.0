from django.conf.urls import patterns, url
from theses_sys import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^add_thesis/', views.add_thesis, name='add_thesis'),
)
