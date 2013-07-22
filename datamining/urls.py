from django.conf.urls.defaults import *
from haystack.views import SearchView
from haystack.forms import *

from django.conf import settings

from django.views.generic.simple import direct_to_template

from django.template import RequestContext

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()        

from datamining.apps.profiles import views

handler404 = "datamining.views.resource_error"
handler500 = 'datamining.views.server_error'
handler503 = "datamining.views.maintenance_error"

urlpatterns = patterns('',
    # Example:
    # (r'^datamining/', include('datamining.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^feeds/', include('feedjack.urls')),

    (r'^profiles/', include('datamining.apps.profiles.urls')),
    
    # Static Files
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^robots.txt$', 'django.views.static.serve', {'path' : "/txt/robots.txt", 'document_root': settings.MEDIA_ROOT, 'show_indexes': False }),
                  
    # App URLs
    (r'^cv/', include('datamining.apps.cv.urls')),

    (r'^importer/', include('datamining.apps.importer.urls')),

    (r'^reporting/', include('datamining.apps.reporting.urls')),

    (r'^comments/', include('django.contrib.comments.urls')),

    (r'^$', 'profiles.views.home'),

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':settings.SUBDIR_PREFIX}),

    (r'^facultylist/$', 'profiles.views.browse'),
    (r'^studentlist/$', 'profiles.views.browse_student'),
    (r'^grouplist/$', 'profiles.views.browse_organization'),
    url(r'^facultylist/alpha/$', 'profiles.views.list_profiles', name='list-alpha-profiles'),
    url(r'^studentlist/alpha/$', 'profiles.views.list_student_profiles', name='list-alpha-student-profiles'),
    url(r'^grouplist/alpha/$', 'profiles.views.list_organization_profiles', name='list-alpha-organization-profiles'),
    url(r'^facultylist/(.*)$', 'profiles.views.list_profiles', name='list-tagged-profiles'),
    
    url(r'^view/(\d+)$', 'profiles.views.view_profile', name='view-profile'),
    url(r'^person/(\d+)/edit/$', 'profiles.views.edit_profile', name='profiles_edit_profile'),
    url(r'^student/(\d+)/edit/$', 'profiles.views.edit_student_profile', name='profiles_edit_student_profile'),
    url(r'^student/(\d+)/contact/$', 'profiles.views.contact_student', name='profiles_contact_student'),
    url(r'^course/(\d+)/edit/$', 'profiles.views.edit_course_profile', name='profiles_course_change'),
    url(r'^section/(\d+)/edit/$', 'profiles.views.edit_section_profile', name='profiles_section_change'),
    #url(r'^org/add/$', 'profiles.views.add_organization', name='profiles_add_organization'),
    
    url(r'^person/(\d+)$', 'profiles.views.view_profile', name='view-person'),
    url(r'^course/(\d+)$', 'profiles.views.view_course', name='view-course'),
    url(r'^section/(\d+)$', 'profiles.views.view_section', name='view-section'),
    url(r'^program/(\d+)$', 'profiles.views.view_program', name='view-program'),
    url(r'^program/(\d+)/edit$', 'profiles.views.edit_program', name='profiles_edit_program'),

    url(r'^aos/(\d+)$', 'profiles.views.view_areasofstudy', name='view-aos'),
    url(r'^student/(\d+)$', 'profiles.views.view_student_profile', name='view-student-profile'),
    url(r'^project/(\d+)$', 'profiles.views.view_project_profile', name='view-project-profile'),
    url(r'^post/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'basic.blog.views.post_detail', name='blog_detail'),

    (r'^syllabus/add/(\d+)$', 'profiles.views.add_syllabus'),

    (r'^about$', direct_to_template, {'template':'about.html'}, 'about' ),
        
    (r'^help$', direct_to_template, {'template':'help.html'}, 'help' ),
        
    (r'^demo$', direct_to_template, {'template':'demo.html'}, 'demo' ),
        
    (r'^contact$', 'profiles.views.contact'),
    (r'^grantperm$', 'profiles.views.grant_permission'),

#    (r'^activate$', 'profiles.views.activate-list'),
    (r'^activate/(\d+)$', 'profiles.views.activate'),

    (r'^site-admin$', 'profiles.views.admin'),
    url(r'^site-admin/stats-report$', 'profiles.views.stats_report', name='stats-report'),

    # CEA Export
    (r'^api/faculty$','profiles.views.api'),

    (r'^api/wordpress/(\d+)$','profiles.views.wordpress'),

    (r'^filter$','profiles.views.filter'),
                                  
    url(r'^search/', SearchView(template='search/search.html', load_all=True, form_class=HighlightedModelSearchForm, searchqueryset=None, context_class=RequestContext), name='haystack_search'), 
    url(r'^visualize/', SearchView(template='search/node_visualizer.html', load_all=True, form_class=HighlightedSearchForm, searchqueryset=None, context_class=RequestContext), name='list-search'),
    
    (r'^test-api/', include('api.urls')),
    (r'^ajax_select/', include('ajax_select.urls')),
    (r'^m/', include('datamining.apps.mobile.urls')),

    (r'^password_required/$', 'password_required.views.login'),
                                             
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^404/$', 'datamining.views.resource_error'),
        (r'^500/$', 'datamining.views.server_error'),
        (r'^503/$', 'datamining.views.maintenance_error'),        
)
