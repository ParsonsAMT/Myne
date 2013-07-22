from django.conf.urls.defaults import *
from django.conf import settings
'''
Created on Aug 28, 2009

@author: edwards
'''
import views

urlpatterns = patterns('pdfreader.views',
    (r'^read/(?P<id>\d)', 'reader'),
    (r'^success/(?P<id>\d)', 'success'),
)