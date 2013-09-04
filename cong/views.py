from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.db.models import Q
import json
import logging
from cong.models import Publisher, ServiceReport, Group, Report


def home(request, year=None, month=None):
    report = ServiceReport.objects
    report.set_month(year,month)
    regular_pioneers = report.regular_pioneers()
    auxiliary_pioneers = report.auxiliary_pioneers()
    publishers = report.publishers()
    active_publishers = report.active_publishers()
    everyone = Publisher.objects.all()
    
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
            'everyone': everyone,
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
        
from django.views.generic.dates import MonthArchiveView, ArchiveIndexView
from django.views.generic import ListView

class PublisherList(ListView):
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(
            self.convert_context_to_json(context),
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        from django.core import serializers
        return serializers.serialize('json', context['publisher_list'])
    
    def get_queryset(self):
        return Publisher.objects.filter(
            Q(first_name__icontains=self.kwargs['name']) |
            Q(last_name__icontains=self.kwargs['name'])
        )

class ReportsMonthView(MonthArchiveView):
    queryset = ServiceReport.objects.all()
    date_field = "month"
    make_object_list = True
    allow_future = False

    def get(self, request, *args, **kwargs):
        print self.kwargs
        latest = ServiceReport.objects.latest('month').month
        self.year = self.kwargs['year'] if self.kwargs.has_key('year') else latest.strftime('%Y')
        self.month = self.kwargs['month'] if self.kwargs.has_key('month') else latest.strftime('%b')
        if self.kwargs.has_key('group'):
            self.group = self.kwargs['group']
        return super(ReportsMonthView, self).get(request)
        
    def get_queryset(self):
        if self.kwargs.has_key('group') :
            self.group = get_object_or_404(Group, name=self.kwargs['group'])
            return ServiceReport.objects.filter(publisher__group=self.group)
        else: 
            return ServiceReport.objects.all()

class ReportsIndexView(ArchiveIndexView):
    latest = ServiceReport.objects.latest('month').month
    queryset = ServiceReport.objects.filter(month__month=latest.month)
    date_field = "month"
    make_object_list = True
    allow_future = False
    template_name = "cong/servicereport_archive_month.html"
    