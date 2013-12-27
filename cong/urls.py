from django.conf.urls import patterns, include, url
from cong.views import *
from util import backup
from django.contrib import admin
admin.autodiscover()

report_patterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>[-\w]+)/$',
        ReportsMonthView.as_view(),
        name="archive_month"),

    url(r'^g/(?P<group>\d+)/(?P<year>\d{4})/(?P<month>[-\w]+)/$', # 
        ReportsMonthView.as_view(),
        name="report_group_month"),
    url(r'^g/(?P<group>\d+)/$', # 
        ReportsMonthView.as_view(),
        name="report_group"),
    url(r'^$',
        ReportsMonthView.as_view(),
        name="report_month"),
    url(r'^add/(?P<publisher>\d+)/$', 
        ReportCreate.as_view(),
        name="report_add")
)

publisher_patterns = patterns('',
    url(r'^(?P<publisher_id>\d+)/$', 'cong.views.publisher_card', name='card'),
    url(r'^list/$', PublisherList.as_view(), name="publisher_list"),
    url(r'^add/$', PublisherCreate.as_view(), name="publisher_add"),
)

attendance_patterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>[-\w]+)/$',
           AttendanceView.as_view(), name="attendance_archive_month"), 
    url(r'^add/$', AttendanceCreateView.as_view(), name="attendance_add"),
    url(r'^$', AttendanceView.as_view(), name="attendance_month")
)
    
urlpatterns = patterns('',
    url(r'^$', 'cong.views.home', name='home'),
    url(r'^r/', include(report_patterns)),
    url(r'^p/', include(publisher_patterns)),
    url(r'^att/', include(attendance_patterns)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^backup/$', backup, name='backup'),
)



