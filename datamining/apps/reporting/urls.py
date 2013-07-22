'''
Created on Oct 15, 2010

@author: edwards
'''
from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from datamining.apps.reporting.handlers import StaffHandler, CommitteeHandler
from datamining.apps.reporting.views import view_committee, edit_committee,\
    view_meeting, edit_meeting, list_committees_by_school

committee_handler = Resource(handler=CommitteeHandler)
staff_handler = Resource(handler=StaffHandler)

urlpatterns = patterns('',
    # removing committee's and organizations due to ticket 170
    #url(r'^committee/add/$', edit_committee, name="reporting_add_committee"),
    #url(r'^committee/(?P<committee_id>[1-9]\d*)/edit/$', edit_committee, name="reporting_edit_committee"),
    #url(r'^committee/(?P<committee_id>[1-9]\d*)/$', view_committee, name="reporting_view_committee"),

    #url(r'^(?P<model_name>committee|organization)/(?P<object_id>[1-9]\d*)/meeting/add/$', edit_meeting, name="reporting_add_meeting"),
    #url(r'^meeting/(?P<meeting_id>[1-9]\d*)/edit/$', edit_meeting, name="reporting_edit_meeting"),
    #url(r'^meeting/(?P<meeting_id>[1-9]\d*)/$', view_meeting, name="reporting_view_meeting"),
    
    #url(r'^committees/$', list_committees_by_school, name="reporting_list_committees"),
)

#API urls
urlpatterns += patterns('',
    # removing committee's and organizations due to ticket 170
    #url(r'^api/committees.(?P<emitter_format>\w+)$', committee_handler),
    #url(r'^api/committee/(?P<id>[1-9]\d*).(?P<emitter_format>\w+)$', committee_handler),
    url(r'^api/staff.(?P<emitter_format>\w+)$', staff_handler),
    url(r'^api/staff/(?P<id>[1-9]\d*).(?P<emitter_format>\w+)$', staff_handler),
)    