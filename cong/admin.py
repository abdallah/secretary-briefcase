from django.contrib import admin
from cong.models import Publisher, ServiceReport, Group
from django import forms
from django.db import models

class SRInline(admin.TabularInline):
    model = ServiceReport
    fk_name = 'publisher'
    extra = 0
    formfield_overrides = {
        models.TextField: { 
            'widget': forms.Textarea(attrs={'cols': 80, 'rows': 1})
        }
    }
    
class PubAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'telephone', 'group')
    list_filter = ('group', )
    inlines = [ SRInline, ]
    

class SRAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('publisher', 
        'month', 'hours', 'magazines', 'visits', 
        'studies', 'books', 'booklets_brochures',
        'auxiliary_pioneer')
    date_hierarchy = 'month'
    fields = (('month', 'auxiliary_pioneer'),
        ('hours', 'magazines', 'visits', 'studies', 'books', 'booklets_brochures'))

admin.site.register(Group)
admin.site.register(Publisher, PubAdmin)
admin.site.register(ServiceReport, SRAdmin)
