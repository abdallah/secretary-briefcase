from django.conf.urls import patterns, include, url
from cong.views import *
from util import backup
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^r/', include('cong.urls')),
    url(r'^$', 'cong.views.home', name='home'),
    url(r'^card/(?P<publisher_id>\d+)/$', 'cong.views.publisher_card', name='card'),
    
    url(r'^p/lookup/$', 
        PublisherList.as_view(),
        name="publisherlist"),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^backup/$', backup, name='backup'),
)
