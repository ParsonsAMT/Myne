'''
Created on Apr 7, 2011

@author: Mike_Edwards
'''
from datamining.apps.reporting.models import Committee, Authority
from django.db.models import Q

class CommitteeLookup(object):
    """
    This lookup pulls in ``Committee`` objects to complete ajax-powered form fields.
    
    """
    
    def get_query(self,q,request):
        return Committee.objects.filter(Q(title__icontains=q))

    def format_result(self,committee):
        return u"%s" % (committee.title)

    def format_item(self,committee):
        return unicode(committee)

    def get_objects(self,ids):
        return Committee.objects.filter(pk__in=ids).order_by('title')
    
