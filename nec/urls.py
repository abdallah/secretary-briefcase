from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^r/', include('cong.urls')),
    url(r'^$', 'cong.views.home', name='home'),
    url(r'^report/(?P<year>(\d{4}))\/(?P<month>(\d{2}))/$', 'cong.views.home', name='report'),
    url(r'^card/(?P<publisher_id>\d+)/$', 'cong.views.publisher_card', name='card'),
    # url(r'^nec/', include('nec.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
