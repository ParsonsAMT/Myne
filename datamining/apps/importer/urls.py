from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',           
    url(r'^sections$', add_sections_import, name="add-sections-import"),
    url(r'^deactivations$', add_deactivations_import, name="add-deactivations-import"),
    url(r'^courses$', add_course_import, name="add-course-import"),
    url(r'^coursemaster$', add_course_master_import, name="add-course-master-import"),
)
