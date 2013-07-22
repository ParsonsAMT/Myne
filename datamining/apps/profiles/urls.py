'''
Created on Aug 18, 2010

@author: edwards
'''
from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from datamining.apps.profiles.handlers import CourseHandler, ExpertiseHandler,\
    PersonHandler, TaggedPersonHandler, TagHandler, StudentHandler, ProjectHandler,\
    WorkHandler, FacultyHandler, ResultHandler, RecentWorkHandler,\
    StudentResultHandler, WorkResultHandler, WorkURLHandler,\
    RecentFacultyHandler, FacultyResultHandler, RecentStudentHandler, TaggedWorkHandler,\
    AreaOfStudyHandler, ProgramHandler, DivisionHandler, SectionHandler
from datamining.apps.profiles.views import download_syllabus, view_staff_profile,\
    view_organization, edit_organization, view_student_profile, view_project_profile,\
    view_work, edit_work, view_invitation, accept_invitation, decline_invitation,\
    edit_student_profile, view_person_profile, edit_person_profile,\
    edit_staff_profile, delete_work, edit_program

course_handler = Resource(handler=CourseHandler)
expertise_handler = Resource(handler=ExpertiseHandler)
faculty_handler = Resource(handler=FacultyHandler)
recent_faculty_handler = Resource(handler=RecentFacultyHandler)
person_handler = Resource(handler=PersonHandler)
project_handler = Resource(handler=ProjectHandler)
student_handler = Resource(handler=StudentHandler)
recent_student_handler = Resource(handler=RecentStudentHandler)
tag_handler = Resource(handler=TagHandler)
tagged_person_handler = Resource(handler=TaggedPersonHandler)
work_handler = Resource(handler=WorkHandler)
recent_work_handler = Resource(handler=RecentWorkHandler)
result_handler = Resource(handler=ResultHandler)
faculty_result_handler = Resource(handler=FacultyResultHandler)
student_result_handler = Resource(handler=StudentResultHandler)
work_result_handler = Resource(handler=WorkResultHandler)
tagged_work_handler = Resource(handler=TaggedWorkHandler)
work_url_handler = Resource(handler=WorkURLHandler)
area_of_study_handler = Resource(handler=AreaOfStudyHandler)
program_handler = Resource(handler=ProgramHandler)
division_handler = Resource(handler=DivisionHandler)
section_handler = Resource(handler=SectionHandler)

urlpatterns = patterns('',
    url(r'^api/subjects/(?P<subject__abbreviation__iexact>[A-Za-z]{4})/semesters/(?P<section__semester__year__exact>\d{4})/(?P<section__semester__term>[a-z]{2})/courses\.(?P<emitter_format>\w+)$', course_handler),
    url(r'^api/subjects/(?P<subject__abbreviation__iexact>[A-Za-z]{4})/courses/(?P<coursenumber>\d{4})\.(?P<emitter_format>\w+)$', course_handler),
    url(r'^api/subjects/(?P<subject__abbreviation__iexact>[A-Za-z]{4})/courses\.(?P<emitter_format>\w+)$', course_handler),
    url(r'^api/expertise/(?P<expertise__id>[1-9]\d*)/people\.(?P<emitter_format>\w+)$', person_handler),
    url(r'^api/expertise/(?P<expertise__name>[\w ]+)/people\.(?P<emitter_format>\w+)$', person_handler),
    url(r'^api/expertise\.(?P<emitter_format>\w+)$', expertise_handler),

    url(r'^api/courses/id/(?P<id>\d+)\.(?P<emitter_format>\w+)$', course_handler),
    url(r'^api/courses/type/(?P<type__iexact>\w+)\.(?P<emitter_format>\w+)$', course_handler),        
    url(r'^api/courses\.(?P<emitter_format>\w+)$', course_handler),
    
    url(r'^api/aos/id/(?P<id>\d+)\.(?P<emitter_format>\w+)$', area_of_study_handler),    
    url(r'^api/aos\.(?P<emitter_format>\w+)$', area_of_study_handler),
    
    
    url(r'^api/programs\.(?P<emitter_format>\w+)$', program_handler),

    url(r'^api/divisions/id/(?P<id>\d+)\.(?P<emitter_format>\w+)$', division_handler),
    url(r'^api/divisions\.(?P<emitter_format>\w+)$', division_handler),

    url(r'^api/sections\.(?P<emitter_format>\w+)$', section_handler),
    
    url(r'^api/people/(?P<id>[1-9]\d*).(?P<emitter_format>\w+)$', person_handler),
    url(r'^api/people/(?P<id>[1-9]\d*)/expertise\.(?P<emitter_format>\w+)$', expertise_handler),
    url(r'^api/people/(?P<person__last_name__iexact>\w+)/(?P<person__first_name__iexact>\w+)/expertise\.(?P<emitter_format>\w+)$', expertise_handler),
    
    url(r'^api/tags/(?P<tag__name__iexact>[\w ]+)/people\.(?P<emitter_format>\w+)$', tagged_person_handler),
    url(r'^api/tags/(?P<tag__name__iexact>[\w ]+)/work\.(?P<emitter_format>\w+)$', tagged_work_handler),
 
    url(r'^api/students\.(?P<emitter_format>\w+)$', student_handler),
    url(r'^api/students/recent\.(?P<emitter_format>\w+)$', recent_student_handler),
    url(r'^api/student/(?P<id>[1-9]\d*)\.(?P<emitter_format>\w+)$', student_handler),
    url(r'^api/student/(?P<homeprogram__abbreviation__iexact>[\w ]+)/students.(?P<emitter_format>\w+)$', student_handler),
    
    url(r'^api/faculty/recent\.(?P<emitter_format>\w+)$', recent_faculty_handler),
    url(r'^api/faculty/(?P<id>[1-9]\d*)\.(?P<emitter_format>\w+)$', faculty_handler),
    url(r'^api/project/(?P<id>[1-9]\d*)\.(?P<emitter_format>\w+)$', project_handler),
    url(r'^api/tags\.(?P<emitter_format>\w+)$', tag_handler),
    
    url(r'^api/work/(?P<id>[1-9]\d*)\.(?P<emitter_format>\w+)$', work_handler),
    url(r'^api/works/recent.(?P<emitter_format>\w+)$', recent_work_handler),
    url(r'^api/workurl.(?P<emitter_format>\w+)$', work_url_handler),
    url(r'^api/workurl/(?P<person__id>\w+)\.(?P<emitter_format>\w+)$', work_url_handler),
    
    url(r'^api/search/$', result_handler),
    url(r'^api/search/faculty/$', faculty_result_handler),
    url(r'^api/search/students/$', student_result_handler),
    url(r'^api/search/works/$', work_result_handler),
        
    url(r'^person/(?P<person_id>[1-9]\d*)/$', view_person_profile, name="profiles_view_person_profile"),
    url(r'^person/(?P<person_id>[1-9]\d*)/edit/$', edit_person_profile, name="profiles_edit_person_profile"),

    url(r'^sections/(?P<section_id>[1-9]\d*)/syllabus/', download_syllabus, name="profiles_download_syllabus"),

    url(r'^staff/(?P<person_id>[1-9]\d*)/$', view_staff_profile, name="profiles_view_staff_profile"),
    url(r'^staff/(?P<person_id>[1-9]\d*)/edit/$', edit_staff_profile, name="profiles_edit_staff_profile"),

    url(r'^org/add/', edit_organization, name="profiles_add_organization"),
    url(r'^org/(?P<organization_id>[1-9]\d*)/edit', edit_organization, name="profiles_edit_organization"),
    url(r'^org/(?P<organization_id>[1-9]\d*)/', view_organization, name="profiles_view_organization"),
    
    url(r'^program/(?P<program_id>[1-9]\d*)/edit', edit_program, name="profiles_edit-program"),

    url(r'^work/add/', edit_work, name="profiles_add_work"),
    url(r'^work/(?P<work_id>[1-9]\d*)/edit/', edit_work, name="profiles_edit_work"),
    url(r'^work/(?P<work_id>[1-9]\d*)/delete/(?P<person_id>[1-9]\d*)/', delete_work, name="profiles_delete_work"),
    url(r'^work/(?P<work_id>[1-9]\d*)/delete/', delete_work, name="profiles_delete_work"),
    url(r'^work/(?P<work_id>[1-9]\d*)/', view_work, name="profiles_view_work"),
    
    url(r'^inv/(?P<slug>[0-9a-f\-]+)/$', view_invitation, name="profiles_view_invitation"),
    url(r'^inv/(?P<slug>[0-9a-f\-]+)/accept/$', accept_invitation, name="profiles_accept_invitation"),
    url(r'^inv/(?P<slug>[0-9a-f\-]+)/decline/$', decline_invitation, name="profiles_decline_invitation"),
)    