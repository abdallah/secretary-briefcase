from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.core import serializers
from django.views import generic
from django.forms import ModelForm
from django.forms.formsets import formset_factory
from django.forms.formsets import BaseFormSet
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib import messages
import json
import logging
from datetime import datetime
from calendar import Calendar
from cong.models import *
from django.conf import settings


def home(request, year=None, month=None):
    everyone = Publisher.objects.all()
    groups = Group.objects.all()
    report = ServiceReport.objects
    if report.all():
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
            'groups': groups,
            'everyone': everyone,
            'pub_report': pub_report, 
            'aux_report': aux_report, 
            'reg_report': reg_report, 
            'dnr': dnr
            })
    else:
        return render(request, 'home.html', {
            'groups': groups,
            'everyone': everyone
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
        return serializers.serialize('json', context['publisher_list'])
    
    def get_queryset(self):
        if self.kwargs.has_key('q'):
            return Publisher.objects.filter(
                Q(first_name__icontains=self.kwargs['q']) |
                Q(last_name__icontains=self.kwargs['q'])
            )
        else: 
            return Publisher.objects.all()

class GroupsView(ListView):
    model = Publisher 

    def get_queryset(self):
        return Publisher.objects.filter(congregation=settings.CONGREGATION).order_by('group', 'last_name')

def update_group(request, publisher_id, group_id):
    pub = get_object_or_404(Publisher, pk=publisher_id)
    group = get_object_or_404(Group, pk=group_id)
    pub.group = group
    try: 
        pub.save()
        return HttpResponse('Saved')
    except:
        return HttpResponseBadRequest()

class PublisherCreate(CreateView):
    model = Publisher
    success_url = '/'

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Publisher added')
        return super(PublisherCreate, self).post(request, *args, **kwargs)


class ReportsMonthView(MonthArchiveView):
    queryset = ServiceReport.objects.all()
    date_field = "month"
    make_object_list = True
    allow_future = False

    def get(self, request, *args, **kwargs):
        latest = ServiceReport.objects.latest('month').month
        self.year = self.kwargs['year'] if self.kwargs.has_key('year') else latest.strftime('%Y')
        self.month = self.kwargs['month'] if self.kwargs.has_key('month') else latest.strftime('%b')
        if self.kwargs.has_key('group'):
            self.group = self.kwargs['group']
        return super(ReportsMonthView, self).get(request, *args, **kwargs)
        
    def get_queryset(self):
        if self.kwargs.has_key('group') :
            self.group = get_object_or_404(Group, name=self.kwargs['group'])
            return ServiceReport.objects.filter(publisher__group=self.group)
        else: 
            return ServiceReport.objects.all()

    def get_context_data(self, **kwargs):
        groups = Group.objects.all()
        kwargs['groups'] = groups
        return kwargs

class ReportForm(ModelForm):
    class Meta: 
        model = ServiceReport
        
class ReportCreate(CreateView):
    model = ServiceReport
    success_url = "/"
    
    def get_initial(self):
        return {'publisher': self.kwargs['publisher'],
                'month': last_month()}
    
    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        d = datetime.strptime(request.POST['month'], '%Y/%m')
        post_values['month'] = datetime.strftime(d, '%Y-%m-%d')
        request.POST = post_values
        messages.success(request, 'Report added')
        return super(ReportCreate, self).post(request, *args, **kwargs)
    
class AttendanceView(MonthArchiveView):
    model = Attendance
    date_field = "meeting_date"
    allow_future = False
    make_object_list = True

    def get(self, request, *args, **kwargs):
        latest = Attendance.objects.latest('meeting_date').meeting_date
        self.year = self.kwargs['year'] if self.kwargs.has_key('year') else latest.strftime('%Y')
        self.month = self.kwargs['month'] if self.kwargs.has_key('month') else latest.strftime('%b')
        return super(AttendanceView, self).get(request, *args, **kwargs)



class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance

class AttendanceCreateView(CreateView):
    model = Attendance
    form_class = AttendanceForm
    success_url  = "/att/"

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Attendance report added')
        return super(AttendanceCreateView, self).post(request, *args, **kwargs)

def initialize_month_attendance(**kwargs):    
    print 'initializing month_attendance'
    latest = ServiceReport.objects.latest('month').month
    year = kwargs['year'] if kwargs.has_key('year') else latest.strftime('%Y')
    month = kwargs['month'] if kwargs.has_key('month') else latest.strftime('%m')
    initial = []
    mwlist = []
    welist = []
    cal = Calendar()
    for day in cal.itermonthdates(int(year),int(month)):
        print 'day: %s' % day.isoformat()
        meeting = None
        if day.weekday()==settings.MEETING_MIDWEEK:
            meeting = "MW"
            mwlist.append({'meeting': meeting, 'meeting_date': day})
        if day.weekday()==settings.MEETING_WEEKEND:
            meeting = "WE"
            welist.append({'meeting': meeting, 'meeting_date': day})
        initial = mwlist + welist
    return initial
        

def manage_attendance(request, year=None, month=None):
    print 'managing attendance'
    AttendanceFormset = formset_factory(AttendanceForm)
    if request.method == 'POST':
        formset = AttendanceFormset(request.POST)
        if formset.is_valid():
            pass
    else:
        latest = ServiceReport.objects.latest('month').month
        year = year if year else latest.strftime('%Y')
        month = month if month else latest.strftime('%m')
        initial = initialize_month_attendance(year=year, month=month)
        formset = AttendanceFormset(initial=initial)
        return render_to_response('cong/attendance_sheet.html', {'formset': formset, 'month':month})
