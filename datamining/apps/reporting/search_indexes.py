'''
Created on Apr 12, 2011

@author: Mike_Edwards
'''
from haystack.indexes import RealTimeSearchIndex
from haystack.sites import site
from datamining.apps.reporting.models import Committee, Meeting
from haystack.fields import CharField
class CommitteeIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    description = CharField(model_attr="mandate",null=True)    
                                                
class MeetingIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    description = CharField(model_attr="agenda",null=True)    
                                                
site.register(Committee, CommitteeIndex)
site.register(Meeting, MeetingIndex)
