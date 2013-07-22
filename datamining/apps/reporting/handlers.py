'''
Created on Aug 18, 2010

@author: edwards
'''
from django.db.models import Q
from piston.handler import BaseHandler
from piston.emitters import Emitter,DjangoEmitter
from datamining.apps.reporting.models import Committee
from datamining.apps.profiles.models import Staff

class CommitteeHandler(BaseHandler):
    """
    This handler returns committees.
    
    """
    
    allowed_methods = ('GET',)
    model = Committee
    fields = ['id',
              'title',
              ('affiliations',
                    ('id',
                     ('role',
                        ('title',
                         ('content_type',
                          ('model',)))),
                     ('person',
                        ('id',
                         'first_name',
                         'last_name')))),
              ('authorities',
                    ('id',
                     ('content_object',
                        ('id',
                         'fullname',)),
                     ('content_type',
                          ('model',))))
              ]
    
    def queryset(self,request):
        return self.model.objects.distinct().order_by('title')

class StaffHandler(BaseHandler):
    """
    This handler returns staff members.
    
    """
    
    allowed_methods = ('GET',)
    fields = ['id',
              'first_name',
              'last_name',
              'tags',
              'photo',
              ('affiliations',
                    ('id',
                     ('role',
                        ('title',
                         ('content_type',
                          ('model',)))),
                     ('content_object',
                        ('id',
                         ('authorities',('id',('content_object',('abbreviation','id',)))),
                         'title',
                         'first_name',
                         'last_name')),
                     ('content_type',
                          ('model',))),
                    )
              ]
    model = Staff
    
    def queryset(self,request):
        return self.model.objects.all().order_by('last_name','first_name')

Emitter.unregister('django')
Emitter.unregister('pickle')

