'''
Created on Oct 15, 2010

@author: edwards
'''
from django.contrib import admin
from models import Committee, Role, Affiliation
from datamining.apps.reporting.models import Authority, Meeting
from django.contrib.contenttypes.generic import GenericTabularInline
from django.contrib.admin.options import ModelAdmin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

class AuthorityInline(GenericTabularInline):
    form = make_ajax_form(Authority,dict(committee='committee'))    
    model = Authority

class AffiliationInline(GenericTabularInline):
    form = make_ajax_form(Affiliation,dict(person='person'))    
    model = Affiliation
    extra = 1
  
class MeetingInline(GenericTabularInline):
    model = Meeting
    extra = 1
  
class CommitteeAdmin(ModelAdmin):
    inlines = [AffiliationInline,MeetingInline,]

admin.site.register(Committee,CommitteeAdmin)
admin.site.register(Role)
admin.site.register(Affiliation)
admin.site.register(Authority)
