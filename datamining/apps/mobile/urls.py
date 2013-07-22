'''
Created on Aug 18, 2010

@author: edwards
'''
from django.conf.urls.defaults import patterns, url
from datamining.apps.mobile.views import home
from haystack.views import SearchView
from haystack.forms import HighlightedModelSearchForm
from django.template.context import RequestContext

urlpatterns = patterns('',
    url(r'^$', home, name="mobile_home"),
    url(r'^search/$', SearchView(template="mobile/search.html",load_all=True, form_class=HighlightedModelSearchForm, searchqueryset=None, context_class=RequestContext), name='mobile_haystack_search'),
)    