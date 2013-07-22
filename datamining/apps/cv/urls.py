from django.conf.urls.defaults import *

from django.conf import settings

urlpatterns = patterns('',
    # Example:
    # (r'^datamining/', include('datamining.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^$', 'datamining.apps.cv.views.home'),
    url(r'^edit/(\d+)$', 'datamining.apps.cv.views.edit'),
    url(r'^delete/(\d+)$', 'datamining.apps.cv.views.delete'),
    url(r'^view/(\d+)$', 'datamining.apps.cv.views.view'),
)

