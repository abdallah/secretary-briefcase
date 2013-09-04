from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from cong.models import Publisher, ServiceReport, Group, Report

def home(request, year=None, month=None):
    report = ServiceReport.objects
    report.set_month(year,month)
    regular_pioneers = report.regular_pioneers()
    auxiliary_pioneers = report.auxiliary_pioneers()
    publishers = report.publishers()
    active_publishers = report.active_publishers()
    
    pub_report = report.group_report(Report.PUB)
    aux_report = report.group_report(Report.AUX)
    reg_report = report.group_report(Report.REG)
    
    dnr = report.did_not_report()
    
    return render(request, 'home.html', {
            'report_month': report.date,
            'active_publishers': active_publishers,
            'regular_pioneers': regular_pioneers,
            'auxiliary_pioneers': auxiliary_pioneers,
            'publishers': publishers,
            'pub_report': pub_report, 
            'aux_report': aux_report, 
            'reg_report': reg_report, 
            'dnr': dnr
        })
        
def publisher_card(request, publisher_id):
    publisher = get_object_or_404(Publisher, pk=publisher_id)
    return render(request, 'publisher_card.html', {
            'publisher': publisher
        })
        
from django.views.generic.dates import MonthArchiveView

class ReportsMonthView(MonthArchiveView):
    queryset = ServiceReport.objects.all()
    date_field = "month"
    make_object_list = True
    allow_future = False