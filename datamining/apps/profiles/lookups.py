from models import Person, Course
from django.db.models import Q
from datamining.apps.profiles.models import School, Department, Division,\
    Program, Work, Organization

class CourseLookup(object):
    """
    This lookup pulls in ``Course`` objects to complete ajax-powered form fields.
    
    """
    
    def get_query(self,q,request):
        return Course.objects.filter(Q(title__istartswith=q) | Q(coursenumber__istartswith=q) | Q(subject__abbreviation__istartswith=q))

    def format_result(self,course):
        return u"%s (%s %s)" % (course.title, course.subject, course.coursenumber)

    def format_item(self,course):
        return unicode(course)

    def get_objects(self,ids):
        return Course.objects.filter(pk__in=ids).order_by('title')

class PersonLookup(object):
    """
    This lookup pulls in ``Person`` objects to complete ajax-powered form fields.
    
    """
    
    def get_query(self,q,request):
        terms = q.split()
        if len(terms) > 1:
            return Person.objects.filter(Q(first_name__istartswith=terms[0]) & Q(last_name__icontains=terms[-1]))
        else:
            return Person.objects.filter(Q(first_name__istartswith=terms[0]) | Q(last_name__istartswith=terms[0]))

    def format_result(self,person):
        return u"%s %s" % (person.first_name, person.last_name)

    def format_item(self,person):
        return unicode(person)

    def get_objects(self,ids):
        return Person.objects.filter(pk__in=ids).order_by('last_name')
    
class WorkLookup(object):
    """
    This lookup pulls in ``Work`` objects to complete ajax-powered form fields.
    
    """
    
    def get_query(self,q,request):
        results = Work.objects.filter(Q(title__icontains=q)|Q(affiliations__person__first_name__istartswith=q)|Q(affiliations__person__last_name__istartswith=q)).distinct()
        return results
    
    def format_result(self,object):
        return u"%s" % (object.title)

    def format_item(self,object):
        return u"%s" % (object.title)

    def get_objects(self,ids):
        results = Work.objects.filter(pk__in=ids).order_by('title')
        return results

class DivisionLookup(object):
    """
    This lookup pulls in ``Division`` objects to complete ajax-powered form fields.
    
    """
    
    def get_query(self,q,request):
        results = Division.objects.filter(Q(name__icontains=q))
        return results
    
    def format_result(self,object):
        return u"%s" % (object.name)

    def format_item(self,object):
        return u"%s" % (object.name)

    def get_objects(self,ids):
        results = Division.objects.filter(pk__in=ids).order_by('name')
        return results

class SchoolLookup(object):
    """
    This lookup pulls in ``School`` objects to complete ajax-powered form fields.
    
    """
    
    def get_query(self,q,request):
        results = School.objects.filter(Q(fullname__icontains=q)|Q(abbreviation__icontains=q))
        return results
    
    def format_result(self,object):
        return u"%s (%s)" % (object.fullname,object.abbreviation)

    def format_item(self,object):
        return u"%s (%s)" % (object.fullname,object.abbreviation)

    def get_objects(self,ids):
        results = School.objects.filter(pk__in=ids).order_by('fullname')
        return results

class DepartmentLookup(object):
    """
    This lookup pulls in ``Department`` objects to complete ajax-powered form fields.
    
    """
    
    def get_query(self,q,request):
        results = Department.objects.filter(Q(fullname__icontains=q)|Q(abbreviation__icontains=q))
        return results
    
    def format_result(self,object):
        return u"%s (%s)" % (object.fullname,object.abbreviation)

    def format_item(self,object):
        return u"%s (%s)" % (object.fullname,object.abbreviation)

    def get_objects(self,ids):
        results = Department.objects.filter(pk__in=ids).order_by('fullname')
        return results

class ProgramLookup(object):
    """
    This lookup pulls in ``Program`` objects to complete ajax-powered form fields.
    
    """
    
    def get_query(self,q,request):
        results = Program.objects.filter(Q(fullname__icontains=q)|Q(abbreviation__icontains=q))
        return results
    
    def format_result(self,object):
        if object.abbreviation is not None:
            return u"%s (%s)" % (object.fullname,object.abbreviation)
        else:
            return u"%s" % (object.fullname)

    def format_item(self,object):
        if object.abbreviation is not None:
            return u"%s (%s)" % (object.fullname,object.abbreviation)
        else:
            return u"%s" % (object.fullname)

    def get_objects(self,ids):
        results = Program.objects.filter(pk__in=ids).order_by('fullname')
        return results


class GroupLookup(object):
    """
    This lookup pulls in ``Organization`` objects to complete ajax-powered form fields.

    """

    def get_query(self,q,request):
        return Organization.objects.filter(Q(title__icontains=q))
        
    def format_result(self,object):
        return u"%s" % (object.title)

    def format_item(self,object):
        return unicode(object)

    def get_objects(self,ids):
        return Organization.objects.filter(pk__in=ids).order_by('title')
    