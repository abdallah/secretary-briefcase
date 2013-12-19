from django.conf.urls import patterns, url

from cong.views import *

urlpatterns = patterns('',
    
    # Example: /2012/aug/
    url(r'^(?P<year>\d{4})/(?P<month>[-\w]+)/$',
        ReportsMonthView.as_view(),
        name="archive_month"),
    # Example: /2012/08/
    url(r'^(?P<year>\d{4})/(?P<month>\d+)/$',
        ReportsMonthView.as_view(month_format='%m'),
        name="archive_month_numeric"),

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
