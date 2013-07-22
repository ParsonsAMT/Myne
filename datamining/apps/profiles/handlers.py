'''
Created on Aug 18, 2010

@author: edwards
'''
from django.db.models import Q
from datamining.apps.profiles.models import Course, Expertise, Person, Student, Project,\
    Work, FacultyMember, Organization, WorkURL, AreaOfStudy, Program, Division, Section
from tagging.models import Tag, TaggedItem
from piston.emitters import Emitter,DjangoEmitter
from haystack.models import SearchResult
from haystack.query import SearchQuerySet
from datamining.apps.profiles.forms import SearchForm
from piston.utils import validate
from piston.handler import BaseHandler

class ResultHandler(BaseHandler):
    """
    This handler is unique in that is uses a ``SearchQuerySet`` from ``haystack``
    rather than the typical Django ``QuerySet``.  This requires a bit of customization
    with the read output, but allows us to treat ``haystack`` search results the
    same way as any other set coming out of the ``piston`` API application.
    """
    
    allowed_methods = ('GET',)
    model = SearchResult
    
    def convert_search_queryset(self,queryset,mlt=False):
        return [{'pk':sr.pk,
                 'app_label':sr.app_label,
                 'model_name':sr.model_name,
                 'title':sr.title,
                 'text':sr.highlighted['text'],
                 'object':sr.object,
                 'score':sr.score} for sr in queryset]      
    
    @validate(SearchForm,'GET')
    def read(self,request,model=None,*args, **kwargs):
        form = SearchForm(getattr(request, 'GET'))
        if form.is_valid():
            content = form.cleaned_data["content"]
            if form.cleaned_data["start"] is not None:
                start = int(form.cleaned_data["start"])
            else:
                start = 0
            if model:
                queryset = SearchQuerySet().narrow("django_ct:%s" % (model)).auto_query(content).highlight()[start:start+10]
            else:
                queryset = SearchQuerySet().auto_query(content).highlight()[start:start+10]
            return self.convert_search_queryset(queryset)
        else:
            return []
 
class FacultyResultHandler(ResultHandler):
    """
    This ``ResultHandler`` allows for searches to be faceted to just return the faculty
    members within a search result set.
    """
    
    def read(self,request,model=None,*args, **kwargs):
        return super(FacultyResultHandler,self).read(request,model="profiles.facultymember")

class StudentResultHandler(ResultHandler):
    """
    This ``ResultHandler`` allows for searches to be faceted to just return the students
    within a search result set.
    """
    
    
    def read(self,request,model=None,*args, **kwargs):
        return super(StudentResultHandler,self).read(request,model="profiles.student")

class WorkResultHandler(ResultHandler):
    """
    This ``ResultHandler`` allows for searches to be faceted to just return the works
    within a search result set.
    """
    
    
    def read(self,request,model=None,*args, **kwargs):
        return super(WorkResultHandler,self).read(request,model="profiles.work")

class CourseHandler(BaseHandler):
    """
    This handler returns courses.
    
    """
    
    allowed_methods = ('GET',)
    fields = ['id',
              'title',
              'type',
              'format',
              'method',
              ('subject',
               ('id','abbreviation',)
               ),
              'coursenumber',
              'description',
              'learning_outcomes',
              'timeline',
              'status',
              'tags',
              'prerequisites']
    model = Course
    
    def queryset(self,request):
        return self.model.objects.distinct().order_by('title')

class SectionHandler(BaseHandler):
    
    allowed_methods = ('GET',)
    fields = ['id',
              'course',
              'semester',
              'crn']
    model = Section
    
    def queryset(self,request):
        return self.model.objects.distinct().order_by('id')

class DivisionHandler(BaseHandler):
    
    allowed_methods = ('GET',)
    fields = ['id',
              'name']
    model = Division
    
    def queryset(self,request):
        return self.model.objects.distinct().order_by('name')

class ProgramHandler(BaseHandler):
    
    allowed_methods = ('GET',)
    fields = ['id',
              'abbreviation',
              'fullname',
              ('school',
                ('id',)
              ),
              ('department',
                ('id',)
              )]
    model = Program
    
    def queryset(self,request):
        return self.model.objects.distinct().order_by('fullname')
        
class AreaOfStudyHandler(BaseHandler):
    
    allowed_methods = ('GET',)
    fields = ['id',
              'abbreviation',
              'fullname']
    model = AreaOfStudy
    
    def queryset(self,request):
        return self.model.objects.distinct().order_by('fullname')
        
class StudentHandler(BaseHandler):
    """
    This handler returns students.
    
    """
    
    allowed_methods = ('GET',)
    fields = ['id',
              'first_name',
              'last_name',
              'status',
              ('homeprogram', ('abbreviation', 'fullname')),
              'year',
              ('homeschool',('id','fullname')),
              'photo',
              'bio',
              'expertise',
              #('affiliations',
                    #('id',
                        #('role',
                            #('title',
                                #('content_type', ('model',))
                            #)
                        #),
                        #('content_object',()),
                        #('content_type', ('model',))
                    #),
                #)
                ]
    model = Student
    
    def queryset(self,request):
        return self.model.objects.order_by('last_name','first_name')

class RecentStudentHandler(StudentHandler):
    """
    This handler returns the 50 most recently updated students.
    
    """
        
    def queryset(self,request):
        return self.model.objects.distinct().order_by('-updated_at')[:50]

class FacultyHandler(BaseHandler):
    """
    This handler returns faculty members.
    
    """
    
    allowed_methods = ('GET',)
    fields = ['id',
              'first_name',
              'last_name',
              'status',
              'homeschool',
              'photo',
              'bio',
              ('affiliations',
                    ('id',
                     ('role',
                        ('title',
                         ('content_type',
                          ('model',)))),
                     ('content_object',()),
                     ('content_type',
                          ('model',))),
                    ),
              'expertise']
    model = FacultyMember
    
    def queryset(self,request):
        return self.model.objects.distinct().order_by('last_name','first_name')
        
class RecentFacultyHandler(FacultyHandler):
    """
    This handler returns the 50 most recently updated faculty members.
    
    """
        
    def queryset(self,request):
        return self.model.objects.distinct().order_by('-updated_at')[:50]

class ProjectHandler(BaseHandler):
    #Deprecated
    
    allowed_methods = ('GET',)
    fields = ['id',
              'title',
              'creator',
              'collaborators',
              'thumbnail',
              'description',
              'year']
    model = Project
    
    def queryset(self,request):
        return self.model.objects.distinct().order_by('title')

class ExpertiseHandler(BaseHandler):
    """
    This handler returns areas of expertise.
    
    """
    
    allowed_methods = ('GET',)
    fields = ['id','name',]
    model = Expertise
    
    def queryset(self,request):
        return self.model.objects.all().order_by('name')

class PersonHandler(BaseHandler):
    """
    This handler is a generic handler for all people.  It's most useful in
    queries like with affiliations where people of multiple roles could be 
    returned (e.g. FacultyMember, Student, Staff)
    
    """
    
    allowed_methods = ('GET',)
    fields = ['id',
              'first_name',
              'last_name',
              'tags',
              ('affiliations',
                    ('id',
                     ('role',
                        ('title',
                         ('content_type',
                          ('model',)))),
                     ('content_object',()),
                     ('content_type',
                          ('model',))),
                    ),
              'photo']
    model = Person
    
    def queryset(self,request):
        return self.model.objects.all().order_by('last_name','first_name')

class WorkHandler(BaseHandler):
    """ 
    This handler returns works.
    
    """
    
    allowed_methods = ('GET',)
    fields = ['id',
              'url',
              'image',
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
              'title',
              'date',
              'year',
              'location',
              'description']
    model = Work


class RecentWorkHandler(WorkHandler):
    """
    This handler returns the 50 most recently updated works.
    
    """

    def queryset(self,request):
        return self.model.objects.all().order_by('-updated_at')[:50]
            
class WorkURLHandler(BaseHandler):
    allowed_methods = ('GET',)
    fields = [('person', ('id', 'first_name', 'last_name')),
              'title',
              'url',
              'description']
    model = WorkURL

class TaggedWorkHandler(BaseHandler):
    """
    This handler returns tagged items, but restricts the results to ``Work`` objects.
    
    """
    
    allowed_methods = ('GET',)
    fields = [('object',
                ('id',
                'url',
                'image',
                'title',
                'location',
                'date',
                'year',
                'type',
                'description',
                'tags')
                )]
    model = TaggedItem
    
    def queryset(self,request):
        return self.model.objects.filter(Q(content_type__name = "work"))

class OrganizationHandler(BaseHandler):
    """
    This handler returns organizations.
    
    """
    
    allowed_methods = ('GET',)
    fields = ['id',
              'title',
              'abbreviation',
              'logo',
              'description',
              'url',
              ('type',('id','name')),
              'projects',
              'courses',
              'tags',
              ]
    model = Organization
    
    def queryset(self,request):
        return self.model.objects.order_by('title')

    
class TagHandler(BaseHandler):
    """
    This handler returns tags.
    
    """
    
    allowed_methods = ('GET',)
    model = Tag
    
class TaggedPersonHandler(BaseHandler):
    """
    This handler returns tagged items, but restricts the results to ``Student`` and ``FacultyMember`` objects.
    
    """
    
    allowed_methods = ('GET',)
    fields = [('object',
                ('id',
              'first_name',
              'last_name',
              'tags',
              'photo',)
               )
              ]
    model = TaggedItem
    
    def queryset(self,request):
        return self.model.objects.filter(Q(content_type__name = "faculty member")|Q(content_type__name = "student"))

Emitter.unregister('django')
Emitter.unregister('pickle')

from datamining.apps.reporting.handlers import CommitteeHandler