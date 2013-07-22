from datamining.apps.profiles.models import Work, Course, FacultyMember, Student,\
    Staff, Organization

from haystack.indexes import RealTimeSearchIndex, CharField
from haystack import site            

class CourseIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr="title")
                                                                       
class FacultyMemberIndex(RealTimeSearchIndex): 
    text = CharField(document=True, use_template=True)    
    first_name = CharField(model_attr="first_name")
    last_name = CharField(model_attr="last_name")
    tags = CharField(model_attr="tags")
    school_name = CharField(model_attr="homeschool__fullname", null=True)
    school_division = CharField(model_attr="homeschool__division__name", null=True)
    
class StudentIndex(RealTimeSearchIndex): 
    text = CharField(document=True, use_template=True)    
    first_name = CharField(model_attr="first_name")
    last_name = CharField(model_attr="last_name")
    tags = CharField(model_attr="tags")  
    
class StaffIndex(RealTimeSearchIndex): 
    text = CharField(document=True, use_template=True)    
    first_name = CharField(model_attr="first_name")
    last_name = CharField(model_attr="last_name")
    tags = CharField(model_attr="tags")  
    
class WorkIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr="title",null=True)
    type = CharField(model_attr="type",null=True)
    location = CharField(model_attr="location",null=True)
    description = CharField(model_attr="description",null=True)
    tags = CharField(model_attr="tags",null=True)
    
class OrganizationIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    title = CharField(model_attr="title",null=True)
    type = CharField(model_attr="type",null=True)
    description = CharField(model_attr="description",null=True)
    tags = CharField(model_attr="tags",null=True)
    
                                                
site.register(FacultyMember, FacultyMemberIndex)
site.register(Work, WorkIndex)
site.register(Student, StudentIndex)
site.register(Staff, StaffIndex)
site.register(Course, CourseIndex)
site.register(Organization, OrganizationIndex)