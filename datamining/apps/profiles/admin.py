from django.contrib import admin, auth

from profiles.models import *

from objectpermissions.admin import TabularGroupPermInline
from basic.blog.models import Post
from basic.blog.admin import PostAdmin
from datamining.apps.profiles.models import Section, Expertise, FacultyMember,\
    AreaOfStudy, OrganizationType, Organization, Work, Requirement,\
    UnitPermission, Department
from django.contrib.contenttypes.generic import GenericTabularInline
from ajax_select import make_ajax_form
from datamining.apps.reporting.admin import AffiliationInline, AuthorityInline
from django.contrib.auth.models import User
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('year','term',)
    
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ('abbreviation','fullname',)
    list_display = ('abbreviation','fullname',)
    
class SectionFacultyInline(admin.StackedInline):
    list_display = ['__unicode__',]
    raw_id_fields = ['section','facultymember']
    model = Section.instructors.through    
    extra = 1
    
class SectionInline(admin.StackedInline):
    model = Section
    extra = 1
    raw_id_fields = ( 'course', 'semester', 'instructors','projects')
    list_display = ('__unicode__',)
    classes = ('collapse closed',)

class UnitPermissionsInline(GenericTabularInline):
    form = make_ajax_form(UnitPermission,dict(user='user'))    
    model = UnitPermission
    
class CourseAdmin(admin.ModelAdmin):
    form = make_ajax_form(Course,dict(prerequisites='course'))
    search_fields = [ 'title', 'coursenumber', 'subject__abbreviation', 'subject__fullname' ]
    list_display = [ 'title', 'subject', 'coursenumber', 'minimum_credits', 'maximum_credits',]
    list_filter = ['subject','is_archived','type']
    raw_id_fields = ( 'subject', 'prerequisites','projects','taken',)
    fields = ('title', 'subject', 'coursenumber', 'minimum_credits','description',)
    #inlines = [ SectionInline, ]
    fields = ('title', 'subject', 'coursenumber', 'minimum_credits', 'prerequisites', 'description',)
    inlines = [ SectionInline, ]
    
class FacultyAdmin(admin.ModelAdmin):
    search_fields = [ 'last_name', 'first_name' ]
    list_display = [ 'last_name', 'first_name' ]
    list_display_links = [ 'first_name', 'last_name' ]
    raw_id_fields = ('user_account','projects','expertise','feeds',)
    #inlines = [ SectionFacultyInline, ]

class StudentAdmin(admin.ModelAdmin):
    search_fields = [ 'last_name', 'first_name' ]
    list_display = [ 'last_name', 'first_name' ]
    list_display_links = [ 'first_name', 'last_name' ]
    #inlines = [ SectionInline, ]

class StaffAdmin(admin.ModelAdmin):
    search_fields = [ 'last_name', 'first_name' ]
    list_display = [ 'last_name', 'first_name', 'updated_at' ]
    list_display_links = [ 'first_name', 'last_name' ]
    inlines = [AffiliationInline,TabularGroupPermInline]

class SectionAdmin(admin.ModelAdmin):
    form = make_ajax_form(Section,dict(instructors='person'))
    search_fields = [ 'course__title', 'course__coursenumber', 'course__subject__abbreviation', 'title', 'crn' ]
    raw_id_fields = ('semester','course','feeds',)

class PersonAdmin(admin.ModelAdmin):
    search_fields = [ 'last_name', 'first_name' ]
    list_display = [ 'last_name', 'first_name' ]
    list_display_links = [ 'first_name', 'last_name' ]
    inlines = [AffiliationInline,TabularGroupPermInline]
    
class ProjectAdmin(admin.ModelAdmin):
    raw_id_fields = ('creator', 'participating_faculty', 'for_course',)

class ProfilesPostAdmin(PostAdmin):
    raw_id_fields = ('author',)
    class Media:
        js = ['/admin/media/tinymce/jscripts/tiny_mce/tiny_mce.js', '/admin/media/tinymce_setup/tinymce_setup.js']
        
        
class AreaOfStudyAdmin(admin.ModelAdmin):
    inlines = [AffiliationInline,]

class DivisionAdmin(admin.ModelAdmin):
    inlines = [AuthorityInline,UnitPermissionsInline]

class SchoolAdmin(admin.ModelAdmin):
    inlines = [AuthorityInline,UnitPermissionsInline]

class DepartmentAdmin(admin.ModelAdmin):
    inlines = [AuthorityInline,UnitPermissionsInline]

class ProgramAdmin(admin.ModelAdmin):
    inlines = [AuthorityInline,UnitPermissionsInline]

class WorkAdmin(admin.ModelAdmin):
    inlines = [AffiliationInline,]
    
class UserAdmin(auth.admin.UserAdmin):
    inlines = [UnitPermissionsInline,]

#register classes for admin interface
admin.site.register(Division,DivisionAdmin)
admin.site.register(School,SchoolAdmin)
admin.site.register(Department,DepartmentAdmin)
admin.site.register(Program,ProgramAdmin)
admin.site.register(AreaOfStudy,AreaOfStudyAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(CourseImage)
admin.site.register(Semester,SemesterAdmin)
admin.site.register(Section,SectionAdmin)
admin.site.register(FacultyMember,FacultyAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Staff,StaffAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(ContactEmail)
admin.site.register(WorkURL)
admin.site.register(WorkType)
admin.site.register(Work,WorkAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(Expertise)
admin.site.register(OrganizationType)
admin.site.register(Organization)
admin.site.register(Requirement)

admin.site.unregister(Post)
admin.site.register(Post,ProfilesPostAdmin)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)

#need to unregister User for userProfile admin editing
#admin.site.unregister(User)
#admin.site.register(User, BuzzUserAdmin)
