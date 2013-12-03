from django.db import models
from datetime import datetime
from django.db.models import Count, Sum
from django.core import serializers

class Report(models.Manager):
    PUB, REG, AUX, SPIO = range(4)
    month = None
    year = None

    def set_month(self, year=None, month=None):
        if month is not None: 
            sdate = '%s-%s-01' % (year, month)
            self.date = datetime.strptime(sdate, '%Y-%m-%d')
        else: 
            self._latest_month()
        self.month = self.date.month
        self.year = self.date.year
    
    def _latest_month(self):
        self.date = ServiceReport.objects.latest('month').month
        return self.date.strftime('%m')
        
    def auxiliary_pioneers(self):
        return [r.publisher for r 
            in self.filter(auxiliary_pioneer=True, 
                month__month=self.month, month__year=self.year)]
        
    def regular_pioneers(self):

        return [r.publisher for r 
            in self.filter(publisher__is_regular_pioneer=True,
                month__month=self.month, month__year=self.year)]
        
    def publishers(self):
        return [r.publisher for r 
            in self.filter(auxiliary_pioneer=False, 
                month__month=self.month,  month__year=self.year,
                publisher__is_regular_pioneer=False, 
                publisher__is_special_pioneer=False)]        
    
    def group_report(self, group):
        if group==self.PUB:
            r = self.filter(month__month=self.month, month__year=self.year,
                auxiliary_pioneer=False, 
                publisher__is_regular_pioneer=False, 
                publisher__is_special_pioneer=False)
        if group==self.REG:
            r = self.filter(month__month=self.month , month__year=self.year, 
                publisher__is_regular_pioneer=True)
        if group==self.AUX:
            r = self.filter(month__month=self.month, month__year=self.year, 
                auxiliary_pioneer=True)
        result = r.aggregate(
            count=Count('publisher'), 
            hours=Sum('hours'),
            magazines=Sum('magazines'),
            visits=Sum('visits'),
            studies=Sum('studies'),
            books=Sum('books'),
            booklets_brochures=Sum('booklets_brochures'))
        return result
    
    def did_not_report(self):
        filled = self.filter(month__month=self.month, month__year=self.year)
        return Publisher.objects.exclude(servicereport__in=filled).order_by('group')
    
    def active_publishers(self):
        return len(self.filter(month__month=self.month, month__year=self.year))
    
class Congregation(models.Model): 
    name = models.CharField(max_length=50)
    number = models.IntegerField()
    
class Attendance(models.Model):
    MEETINGS = ( ('MW', 'Mid Week'), ('WE', 'Weekend') )
    meeting = models.CharField(max_length=2, choices=MEETINGS)
    date = models.DateField()
    number = models.IntegerField()
    
class Group(models.Model):
    name = models.CharField(max_length=50)
    overseer = models.ForeignKey('Publisher', 
        related_name='overseer', limit_choices_to = {'is_elder': True})
    
    def __unicode__(self):
        return "%s - %s" % (self.name, self.overseer)

class Publisher(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True, null=True)
    telephone = models.CharField(max_length=200, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_immersed = models.DateField(blank=True, null=True)
    is_annointed = models.BooleanField(default=False)
    is_elder = models.BooleanField(default=False)
    is_ministerial_servant = models.BooleanField(default=False)
    is_regular_pioneer = models.BooleanField(default=False)
    is_special_pioneer = models.BooleanField(default=False)
    group = models.ForeignKey('Group', blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __unicode__(self):
        return self.get_name()
        
    def get_name(self):
        return "%s %s" % (self.first_name, self.last_name)
        
    def to_json(self):
        return serializers.serialize("json", self)
        
class Pioneer(models.Model):
    TYPES = ( ('RE', 'Regular'), ('SP', 'Special') )
    publisher = models.ForeignKey ('Publisher')
    pioneer_type = models.CharField(max_length=2, choices=TYPES)
    date_started = models.DateField()
    date_stopped = models.DateField()
    
class ServiceReport(models.Model):
    publisher = models.ForeignKey('Publisher')
    month = models.DateField()
    hours = models.IntegerField()
    magazines = models.IntegerField(blank=True, null=True)
    visits = models.IntegerField(blank=True, null=True)
    studies = models.IntegerField(blank=True, null=True)
    books = models.IntegerField(blank=True, null=True)
    booklets_brochures = models.IntegerField(blank=True, null=True)
    auxiliary_pioneer = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    objects = Report()
    
    class Meta: 
        ordering = ['-month']
        
    def __unicode__(self):
        return "%s - %s" % (self.publisher, self.month.strftime('%b %Y'))
    
