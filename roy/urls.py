from django.conf.urls import patterns, include, url
import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'roy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/','blog.views.index'),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
)
