from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'browseuptheses.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^theses_sys/', include('theses_sys.urls', namespace='theses_sys')),
    url(r'^admin/', include(admin.site.urls)),
)
