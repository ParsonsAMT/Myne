from django.db.models import  *        
from django.contrib.auth.models import User

import tagging
from tagging.models import *
from tagging.fields import TagField
import objectpermissions
from feedjack.models import Feed
                 
from datamining.libs.utils import *
import os,sys                
from django.db import models

from south.modelsinspector import add_ignored_fields
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save, pre_delete
from django.db.models.query import EmptyQuerySet

import uuid
from django_extensions.db.fields import UUIDField
from djangocalais.models import CalaisDocument

add_ignored_fields(["^objectpermissions\.models\.UserPermissionRelation"])
add_ignored_fields(["^objectpermissions\.models\.GroupPermissionRelation"])


class BaseModel (Model):
    """
    BaseModel is the root of almost all other objects within the DataMYNE
    system. It establishes the creation and modification date fields, as well 
    as indicating which user last changed the given model.  It also stubs out
    the permissions for a ``auth.User`` and other objects based upon their 
    associations within the university's hierarchy of "units" 
    (e.g. ``profiles.Division``, ``profiles.School``, etc.)

    """
    class Meta: abstract = True
    created_at          = DateTimeField(auto_now_add=True,editable=False)
    updated_at          = DateTimeField(auto_now=True,editable=False)
    created_by          = ForeignKey(User,blank=True,editable=False)
    unit_permissions    = generic.GenericRelation("UnitPermission")
    scripted = False

    def __unicode__ (self):
        if hasattr(self,"name") and self.name:
            return self.name
        elif hasattr(self, "title") and self.title:
            return self.title
        else:
            return "%s #%d" % (type(self), self.id)

    # see http://code.djangoproject.com/wiki/CookBookThreadlocalsAndUser
    def save (self, *args, **kwargs):
        """
        Every DataMyne object has a ``created_by`` field that contains the ``User``
        object of the user who was logged in when the system created the
        object.  The method uses the datamining.middleware module to access
        another thread and check on the current user.
        
        """
        
        from datamining.middleware import threadlocals

        """ Sets created_by from current user. """
        if not hasattr(self,"created_by") or not self.created_by:
            self.created_by = threadlocals.get_current_user()
        super(BaseModel,self).save(*args,**kwargs)
        
    def get_unit(self):
        """
        get_unit returns the organizational unit that hold responsibility
        for this object.  For example, a committee executing get_unit could
        return the division that has authority over it.
        
        """
        
        return None
    
    def _get_unit_permissions(self,user,cascade=False):
        unit = self.get_unit()
        if unit is not None:
            unit_permissions = unit.unit_permissions.filter(user=user)
            if unit_permissions.count() == 0:
                return unit._get_unit_permissions(user,cascade=True)
            else:
                return (unit,unit_permissions)
        else:
            if cascade:
                return (self,EmptyQuerySet())
            else:
                #i.e. there are no unit permissions, so go ahead
                return (None,EmptyQuerySet())
    
    def has_unit_permission(self,user):
        """
        Given a user, this method will check to see if that user is
        attached to the appropriate organizational unit to have access
        to edit this object.  This allows people in higher levels of
        the university's hierarchy the ability to edit a greater number
        of objects, while restricting those lower down to objects that
        only affect their unit.
        
        """
        
        if user.is_anonymous():
            return False
        unit,unit_permissions = self._get_unit_permissions(user)
        if unit is not None:
            return unit_permissions.count() > 0
        else:
            #i.e. there are no unit permissions, so stop
            return False
   
###############################################################
# Projects
###############################################################   
class Project(BaseModel):
    """
    Project is a now defunct way of expressing what we now use Organizations
    and Works to accomplish.  This should be retired.
    
    """
    
    title = CharField(max_length=255, default='Untitled')
    description = CharField(max_length=255,blank=True,null=True)
    url = URLField(verify_exists=True,help_text="Provide a link to your project", blank=True,null=True)

    CREATOR_CHOICES = (
        ('I', 'Individual'),
        ('C', 'Collaborative')
    )                         

    SCOPE_CHOICES = (
        ('C', 'Curriculuar'),
        ('E', 'Extracurricular')
    )
    
    REF_CHOICES = (
        ('I', 'Internal'),
        ('E', 'External')
    )
                                                                  
    # Who made it?
    creator_type = CharField(max_length=2, choices=CREATOR_CHOICES, default='I')
    creator = ForeignKey('Person', blank=True, null=True)
    collaborators = TextField(blank=True,null=True)
    
    scope_type = CharField(max_length=2, choices=SCOPE_CHOICES)
    ref_type = CharField(max_length=2, choices=REF_CHOICES, default='I')

    thumbnail  = ImageField(upload_to='user/projects/%s' % id, blank=True,null=True)
    specifications = TextField(blank=True, null=True)  # e.g. size, partnership/association, or duration
    year = PositiveIntegerField(blank=True, null=True)
    location = CharField(max_length=255,blank=True, null=True) # city or country
    format = TagField(max_length=2000) # does this work ?
    tags = TagField(max_length=2000)
    
    # primarily for curricular scope
    participating_faculty = OneToOneField('FacultyMember', blank=True, null=True)
    for_course  = ForeignKey('Course', blank=True, null=True)

        
###############################################################
# People
###############################################################
class Division(BaseModel):
    """
    A ``Division`` is the highest "unit" within the university.  Below it
    are ``Department`` , ``School``, etc.

    """
    
    DIV_TYPES = (
        ('ac', 'Academic'),
        ('ad', 'Administrative'),
        ('ot', 'Other'),
    )
    
    name = CharField(max_length=255)
    type = CharField(max_length=2, choices=DIV_TYPES, default="ot")

    def __unicode__ (self):
        return self.name

class School(BaseModel):
    """
    A ``School`` is one of the the highest "units" within the university.  
    Below it are programs.  It sits at the same level as a ``Department``
    
    Historically, only Parsons the New School for Design has Schools.

    """
    abbreviation = CharField(max_length=255)
    fullname = CharField(max_length=255,blank=True)
    division = ForeignKey(Division,blank=True,null=True)

    def __unicode__ (self):
        return "%s (%s)" % (self.fullname,self.abbreviation)
    
    def get_unit(self):
        # A school's unit is its division
        
        return self.division
    
class Department(BaseModel):
    """
    A ``Department`` is one of the the highest "units" within the university.  
    Below it are programs.  It sits at the same level as a ``Department``
    
    Historically, all divisions except Parsons the New School for Design 
    have Departments.

    """
    abbreviation = CharField(max_length=255)
    fullname = CharField(max_length=255,blank=True)
    division = ForeignKey(Division,blank=True,null=True)

    def __unicode__ (self):
        return "%s (%s)" % (self.fullname,self.abbreviation)

    def get_unit(self):
        # A department's unit is its division
        return self.division

class Program(BaseModel):
    """
    A ``Program`` is typically the lowest organizational unit in the university.
    It sits below either a ``School`` or a ``Department``.
    
    """
    
    abbreviation    = CharField(max_length=255)
    fullname        = CharField(max_length=255, blank=True)
    school          = ForeignKey(School, blank=True, null=True)
    department      = ForeignKey(Department, blank=True, null=True)
    director        = ForeignKey('Person', blank=True, null=True, related_name="program_director")
    advisors        = ForeignKey('Person', blank=True, null=True, related_name="program_advisors")
    facultylist     = ManyToManyField('Person', blank=True, null=True, related_name="program_faculty")
    office          = CharField(max_length=255, null=True, blank=True)
    website_url     = URLField(verify_exists=True, blank=True, null=True)
    curriculum_url  = URLField(verify_exists=True, blank=True, null=True)
    extra_url       = URLField(verify_exists=True, blank=True, null=True)
    courses_url     = URLField(verify_exists=True, blank=True, null=True)
    description     = TextField(blank=True, null=True)
    groups          = ManyToManyField('Organization', blank=True, null=True, related_name="program_groups")
    works           = ManyToManyField('Work', blank=True, null=True, related_name="program_works")

    def get_unit(self):
        # A program's unit is its school or department
        return self.get_parent()
    
    @models.permalink
    def get_absolute_url(self):                      
        return ('view-program', [str(self.id)])
        
    def get_parent(self):
        if self.school is not None:
            return self.school
        elif self.department is not None:
            return self.department
        else:
            return None
        
    def __unicode__ (self):
        return "%s (%s)" % (self.fullname,self.abbreviation)
             

class Subject(BaseModel):
    """
    A ``Subject`` typically represents a group of ``Course`` objects below a
    ``Program``.  Recent changes in the way courses are constructed, though,
    may require this simple relationship to be expanded somewhat.  A ``Subject``
    also contains the four-letter abbreviation that precedes a couse number
    in the course directories. 
    
    """
    
    abbreviation = CharField(max_length=255)
    fullname = CharField(max_length=255,blank=True)
    program = ForeignKey(Program, blank=True, null=True, related_name="subject_program")
    division = ForeignKey(Division,blank=True,null=True, related_name="subject_division")

    class Meta:
        ordering = ['abbreviation',]

    def __unicode__ (self):
        return self.abbreviation

    def get_unit(self):
        #TODO: this needs to be associated with more than just a program unit.  Could be dept, school, division
        return self.program

class AreaOfStudy(BaseModel):
    """
    An ``AreaOfStudy`` is a more amorphous grouping of courses that are not
    necessarily organized under the traditional hierarchy.
    
    """
    
    abbreviation    = CharField(max_length=255)
    fullname        = CharField(max_length=255,blank=True)
    program         = ManyToManyField(Program, blank=True, null=True, related_name="aos_program")
    coordinator     = ForeignKey('Person', blank=True, null=True, related_name="aos_coordinator")
    advisors        = ForeignKey('Person', blank=True, null=True, related_name="aos_advisors")
    office          = CharField(max_length=255, null=True, blank=True)
    url             = URLField(verify_exists=True, blank=True, null=True)
    aos_url         = URLField(verify_exists=True, blank=True, null=True)
    courses_url     = URLField(verify_exists=True, blank=True, null=True)
    description     = TextField(blank=True, null=True)
    groups          = ManyToManyField('Organization', blank=True, null=True, related_name="aos_groups")
    works           = ManyToManyField('Work', blank=True, null=True, related_name="aos_works")
    
    class Meta:
        verbose_name_plural = "areas of study"
#    @models.permalink
#    def get_absolute_url(self):                      
#        return ('view-program', [str(self.id)])
        
    def __unicode__ (self):
        return self.abbreviation

class Expertise(BaseModel):
    """
    An ``Expertise`` (sometimes called an area of expertise) is a canonical
    keyword that users can select to describe them in their profiles.
    
    """
    
    name = CharField(max_length=255)
    
class ActivePersonManager(models.Manager):
    """
    The ``ActivePersonManager`` supports the ``Person`` class by restricting
    queries to only those people who have active user accounts.
    
    """
    
    def get_query_set(self):
        return super(ActivePersonManager, self).get_query_set().filter(user_account__is_active=1)
    
class Person(BaseModel):
    """
    A ``Person`` represents any number of roles within the university, but
    provides a unifying class for dealing with all of them.  The ``Person``
    has fields for first and last name, N Number, etc. as well as several
    crucial class and object methods that pertain to all members of the
    university.
    
    A ``Student``, ``Staff``, and ``FacultyMember`` object are all of 
    the ``Person`` type.
    
    """

    def cv_filename (self, filename):
        # We try to prepend CV documents with user id's to prevent collision
        
        if not self.id:
            raise Error("oops, trying to save file for profile that doesn't exist yet")
        return 'user/cv/%s-%s' % (self.id,filename)

    def photo_filename (self, filename):
        # We try to prepend profile photos with user id's to prevent collision

        if not self.id:
            raise Error("oops, trying to save file for profile that doesn't exist yet")
        return 'user/photos/%s-%s' % (self.id,filename)
    
    objects = models.Manager()
    actives = ActivePersonManager()

    CV_CHOICES = (
        ('u', 'Uploaded'),
        ('g', 'Generated'),
    )

    first_name    = CharField(max_length=255)
    last_name     = CharField(max_length=255)
    n_number      = CharField(max_length=9)
    user_account  = OneToOneField(User, related_name='person_profile', blank=True, null=True)
    tags          = TagField(max_length=2000)
    cv            = FileField("CV",upload_to=cv_filename,blank=True,null=True) 
    photo         = ImageField("Photo",upload_to=photo_filename,blank=True,null=True)
    use_which_cv  = CharField(max_length=1, choices=CV_CHOICES,blank=True)
    projects      = ManyToManyField(Project,blank=True,null=True)
    expertise     = ManyToManyField(Expertise,blank=True,null=True)
    feeds         = ManyToManyField(Feed,blank=True,null=True)
     
    class Meta: 
        ordering = ('last_name','first_name')
        verbose_name_plural = "People"

    def get_academic_title_display(self, *args, **kwargs):    
        return 'Community Member' 
        
    def full_name(self):
        # Creates a full name, if possible, from the person's information
        
        if self.last_name:
            return u"%s %s" % (self.first_name, self.last_name)
        return self.first_name
           
    def default_username (self):
        # this is a now-deprecated username generation method
        
        name = ('%s%s' % (self.last_name, self.first_name[0]))

        # TODO: need to make this more robust w/ a proper regular
        # expression ... remove all non-alpha:
        name = name.lower().replace(' ','').replace("'",'')[0:20]

        unique_name = name
        name_valid = False
        index = 2
        while not name_valid:
            try:
                existing_person = User.objects.get(username=unique_name)
                
                # then that unique_name exists, increase index and try again
                unique_name = '%s%d' % (name, index)
                index = index + 1
            except User.DoesNotExist: #@UndefinedVariable
                name_valid = True

        return unique_name

    def activate(self,email):
        """
        An email-based activation method.  This is deprecated since the 
        introduction of the LDAP authentication
        
        """

        username = email[0:email.find("@")].lower()

        new_activation = False

        # if this faculty already has user_account set, then use that
        if self.user_account is not None:

            if not self.user_account.is_active:
                new_activation = True

            self.user_account.is_active = True

        else:
            try:
                # else, if a user already exists for this username,
                # use that
                user = User.objects.get(username=username)
                if not user.is_active:
                    new_activation = True
                user.is_active = True
            except User.DoesNotExist:
                # or finally, make a new user
                user = User(username=username,email=email,is_staff=0,is_active=1)
                user.set_password(self.n_number)
                user.is_active = True

            self.user_account = user
            self.save()

        self.user_account.save()

        if new_activation:
            # @todo where should we put this text block? -rory
            subject = "You've been added to the Parsons DataMyne"
            message = """Greetings Parsons Faculty!

You've been added to the Parsons DataMyne!

DataMyne is a comprehensive, dynamic, web-based platform designed to connect the larger curricular and research domains of Parsons' courses and faculty. In its visual mapping of database information related to specific course content, syllabi, faculty interests, expertise and bios, this platform is helping to foster a resource for students, administration, and faculty across all areas of study. This information is also relayed to the official Parsons website.

In your faculty profile you submit a photo, professional bio & URL, areas of expertise, tagged research interests, and upload your CV and syllabus.  Your participation is enthusiastically encouraged!

Log in here with your NetID and N number:
http://mining.parsons.edu/

Cheers,

The DataMyne Team"""

            # now send notification email
            d = DataminingEmail( to=[email],
                                 from_email='datamine@parsons.edu',
                                 subject=subject,
                                 body=message, )
            d.send(fail_silently=False)

    def deactivate(self):
        """
        Deactivates a person's user account
        
        """
        
        self.user_account.is_active = False
        self.user_account.save()


    @staticmethod
    def does_person_exist_for_user(user):
        try:
            person = Person.objects.get(user_account=user)
            person_exists = True
        except Person.DoesNotExist:
            person_exists = False
        return person_exists

    def get_cv_url(self):
        from django.core.urlresolvers import reverse

        try:
            generated_cv = self.generated_cv
        except Exception:
            generated_cv = None

        if self.cv and generated_cv:
            if self.use_which_cv == 'u': # use the user's uploaded cv
                url = self.cv.url
            else: # use the generated cv
                url = reverse('cv.views.view',args=[self.id])
        elif self.cv:
            url = self.cv.url
        elif generated_cv:
            url = reverse('cv.views.view',args=[self.id])
        else:
            url = None

        return url                        
        
    def _cv_text(self):
        if self.cv:                    
            file_path = self.cv.path  
            try:
                if os.path.isfile(file_path):
                    txt = get_doc_contents(os.path.basename(self.cv.name), file_path)
                    return txt
            except pycurl.error:
                # skipping because of formpost error, come back next time
                return ""
            
    def cv_text(): #@NoSelf
        doc = """Docstring""" #@UnusedVariable
       
        def fget(self):
            return self._cv_text()
                      
        return locals()
       
    cv_text = property(**cv_text())
    
    @models.permalink
    def get_absolute_url(self):
        try:
            return ('profiles.views.view_person_profile', [str(self.id)])
        except:
            return None
        
    def __unicode__ (self):                     
        return self.full_name()
                 
person_perms = ['read cv','read syllabi','open cv','open syllabi']
objectpermissions.register(Person, person_perms)
                    
class WorkURL(BaseModel):
    """
    A ``WorkURL`` provides a URL associated with a persons work
    (e.g. portfolio links, etc.).
    
    This should be deprecated in favor of the more flexible
    ``Link`` class.
    
    """
    
    title = CharField(max_length=255)
    url = URLField(verify_exists=True,help_text="Provide links to your portfolio(s)")
    description = CharField(max_length=255)
    person = ForeignKey(Person,blank=True,null=True)

class Link(BaseModel):
    """
    A ``Link`` allows for adding a URL, plus description and other metadata,
    to any object in the system.
    
    It should succeed ``WorkURL`` for ``Person`` links and be used for other
    DataMyne objects should links become useful with them.
    
    """
    
    title = CharField(max_length=255)
    url = URLField(verify_exists=True,help_text="Provide interesting links")
    description = CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

class WorkType(BaseModel):
    
    name        = CharField(max_length=255)

class Work(BaseModel):
    """
    A ``Work`` represents any work of art or any other product/document/etc.
    created within the system.  We do NOT associate these with a ``Person``
    directly.  Instead, these relationships are managed with the 
    ``Affiliation`` class from the ``reporting`` application.  The allows for
    many-to-many relationships, as well as providing subtle variations in the
    role, date of participation, etc.
    
    """
    

    def image_filename (self, filename):
        return 'user/work/%s' % (filename)

    url             = URLField(verify_exists=True,help_text="Provide links with images to presentations")
    image           = ImageField(upload_to=image_filename, blank=True, null=True)
    title           = CharField(max_length=255, blank=True, null=True)
    location        = CharField(max_length=255, blank=True, null=True)
    date            = DateTimeField(blank=True,null=True)
    year            = PositiveIntegerField(max_length=4,blank=True,null=True)
    type            = ManyToManyField(WorkType, related_name="works", blank=True, null=True)
    description     = TextField(blank=True,null=True,help_text="Limit 100 words")
    tags            = TagField(max_length=2000)
    
    @models.permalink
    def get_absolute_url(self):                      
        return ('profiles_view_work', [str(self.id)])

def index_work(sender, *args, **kwargs): 
    # updates a ``Work`` in the search engine after every change to the object
    from haystack import site
    site.get_indexes()[Work].update_object(kwargs['instance']) 
post_save.connect(index_work, sender=Work) 

def delete_work_affiliations(sender, *args, **kwargs): 
    # removes affiliations to a ``Work`` upon deletion
    from datamining.apps.reporting.models import Affiliation
    work = kwargs['instance']
    affiliations = Affiliation.current.filter(content_type__name="work",object_id = work.id)
    affiliations.delete()
pre_delete.connect(delete_work_affiliations, sender=Work) 

class ActiveFacultyManager(models.Manager):
    def get_query_set(self):
        return super(ActiveFacultyManager, self).get_query_set().filter(user_account__is_active=1)

class FacultyMember(Person):
    """
    A ``FacultyMember`` is a ``Person`` (believe it or not) that teaches one or more
    ``Section`` objects of a ``Course`` object.  Their association with a ``Section``
    is their key distinction with other ``Person`` objects.
    
    """
    
    class Meta: 
        verbose_name_plural = "Faculty"

    objects = models.Manager()  # The default manager
    actives = ActiveFacultyManager()  # only active faculty members

    STATUS_CHOICES = (
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('AD', 'Administrative'),
        )
    pidm            = IntegerField(blank=True,null=True)
    academic_title  = CharField(max_length=255,blank=True)
    admin_title     = CharField("Administrative Title",max_length=255,blank=True)
    status          = CharField(max_length=2,choices=STATUS_CHOICES)
    #expertise      = ManyToManyField(Expertise,blank=True,null=True)
    bio             = TextField(blank=True,null=True,help_text="Limit 250 words")
    office          = CharField(max_length=255,blank=True)
    phone           = CharField(max_length=20,blank=True)
    homeschool      = ForeignKey(School,verbose_name="School Affiliation",blank=True,null=True)
    homedepartment  = ForeignKey(Department,verbose_name="Department Affiliation",blank=True,null=True)
    homedivision    = ForeignKey(Division,verbose_name="Divisional Affiliation",blank=True,null=True)
    homeprogram     = ForeignKey(Program,verbose_name="Program Affiliation",blank=True,null=True)

    def save (self, *args, **kwargs):
        super(FacultyMember,self).save(*args,**kwargs)

    def get_academic_title_display(self, *args, **kwargs):
        if self.status == 'FT' and self.academic_title:
            return self.academic_title
        else:
            return "%s Faculty" % self.get_status_display()

    def get_short_title_display(self, *args, **kwargs):
        if self.status == 'FT':
            return "FTF"
        else:
            return "PTF"
        
    def get_unit(self):
        # A ``FacultyMember`` has their home school as their unit
        return self.homeschool

    @models.permalink
    def get_absolute_url(self):                      
        return ('profiles.views.view_profile', [str(self.id)])

        
def index_faculty_member(sender, *args, **kwargs): 
    # updates a ``FacultyMember`` in the search engine after every change to the object
    from haystack import site
    site.get_indexes()[FacultyMember].update_object(kwargs['instance']) 
#        if kwargs['instance'].bio is not None:
#            CalaisDocument.objects.analyze(kwargs['instance'],fields=[('bio','text/html'),('cv_text','text/txt')])
post_save.connect(index_faculty_member, sender=FacultyMember) 

class ActiveStudentManager(models.Manager):
    def get_query_set(self):
        return super(ActiveStudentManager, self).get_query_set().filter(user_account__is_active=1)

class Student(Person):
    """
    A ``Student`` is a ``Person`` that has a graduation year and home program.
    
    Students need to be addressed with the utmost sensitivity and security, since
    we must follow FERPA guidelines and cannot divulge any more data than is
    absolutely necessary (i.e. directory information).  See:
    
    http://www2.ed.gov/policy/gen/guid/fpco/ferpa/mndirectoryinfo.html
    
    """
    
    objects = models.Manager()  # The default manager
    actives = ActiveStudentManager()  # only active student members
    
    STATUS_CHOICES = (
        ('C', 'Current'),
        ('P', 'Past'),
        )
    status          = CharField(max_length=2,choices=STATUS_CHOICES,default='C')
    program         = CharField(max_length=255,blank=True,null=True)
    homeprogram     = ForeignKey(Program,verbose_name="Program",blank=False,null=True)
    year            = PositiveIntegerField(max_length=4,blank=False,null=True)
    bio             = TextField(blank=True,null=True,help_text="Limit 250 words")
    homeschool      = ForeignKey(School,verbose_name="School Affiliation",blank=True,null=True)
    
    def get_academic_title_display(self, *args, **kwargs):
        if self.status == 'C':
            return 'Current Student'
        elif self.status == 'P':
            return 'Past Student'
        else:
            return 'Student'
    
    def get_school_name_display(self, *args, **kwargs):
        # this is a deprecated method that needs to be factored out of code
        return ''
            
    @models.permalink
    def get_absolute_url(self):                      
        return ('profiles.views.view_student_profile', [str(self.id)])

def index_student(sender, *args, **kwargs): 
    # updates a ``Student`` in the search engine after every change to the object
    from haystack import site
    site.get_indexes()[Student].update_object(kwargs['instance']) 
#        if kwargs['instance'].bio is not None:
#            CalaisDocument.objects.analyze(kwargs['instance'],fields=[('bio','text/html'),('cv_text','text/txt')])
post_save.connect(index_student, sender=Student)

class Staff(Person):
    """
    A ``Staff`` member is a ``Person`` that works for the university in a role
    other than faculty.  They are assigned to a ``Division`` and have a 
    job description.
    
    """
    
    STATUS_CHOICES = (
        ('C', 'Current'),
        ('P', 'Past'),
        )
    pidm            = IntegerField(blank=True,null=True)
    status          = CharField(max_length=2,choices=STATUS_CHOICES)
    admin_title     = CharField("Administrative Title",max_length=255,blank=True)
    bio             = TextField(blank=True,null=True,help_text="Limit 250 words")
    job_description = TextField("Job Description",blank=True,null=True,help_text="Limit 250 words")
    division        = ForeignKey(Division,verbose_name="Divisional Affiliation",blank=True,null=True)
    office_location = CharField("Office Location",max_length=255,null=True,blank=True)
    phone           = CharField("Phone",max_length=255,null=True,blank=True)
    school          = ForeignKey(School,verbose_name="School Affiliation",blank=True,null=True)
    department      = ForeignKey(Department,verbose_name="Department Affiliation",blank=True,null=True)
    program         = ForeignKey(Program,verbose_name="Program Affiliation",blank=True,null=True)

    @models.permalink
    def get_absolute_url(self):                      
        return ('profiles_view_staff_profile', [str(self.id)])

            
def index_staff(sender, *args, **kwargs): 
    # updates a ``Staff`` in the search engine after every change to the object
    from haystack import site
    site.get_indexes()[Staff].update_object(kwargs['instance']) 
#        if kwargs['instance'].bio is not None:
#            CalaisDocument.objects.analyze(kwargs['instance'],fields=[('bio','text/html'),('cv_text','text/txt')])
post_save.connect(index_staff, sender=Staff)

###############################################################
# Courses
###############################################################

class Semester(BaseModel):
    """
    A ``Semester`` object represents the season and year in which a ``Section``
    of a ``Course`` is held.  Note that, in Banner exports, spring and summer
    semesters are list as part of the previous year.  For example:
    
    * 201010 is the fall semester of 2010
    * 201030 is the spring semester of 2011
    
    For simplicity's sake, however, we convert the banner code to the correct
    calendar year.  Therefore, fall 2010 has the term "fa" and the year "2010"
    while spring 2011 has the term "sp" and the year "2011".  All the conversions
    for this are done in the import script and should never need to be
    considered outside of that.
    
    """
    
    TERM_CHOICES = (
        ('fa', 'Fall'),
        ('sp', 'Spring'),
        ('su', 'Summer'),
        ('wi', 'Winter'),
        )
    term        = CharField(max_length=2,choices=TERM_CHOICES)
    year        = PositiveIntegerField()
    start_date  = DateField()
    end_date    = DateField()

    def __unicode__ (self):
        return "%s %d" % ( self.get_term_display(), self.year )

class CurrentCourseManager(models.Manager):
    # a helper for ``Course`` objects to indicate if a course has not been archived
    use_for_related_fields = True
    
    def get_query_set(self):
        return super(CurrentCourseManager, self).get_query_set().filter(is_archived=False)

class ArchivedCourseManager(models.Manager):
    # a helper for ``Course`` objects to indicate if a course has been archived
    use_for_related_fields = True
    
    def get_query_set(self):
        return super(ArchivedCourseManager, self).get_query_set().filter(is_archived=True)

class Course(BaseModel):
    """
    A ``Course`` is an object that contains course information across time. A
    ``Section`` object is connected to a course and shows only the information
    that is specific to a particular semester and set of faculty.  
    
    The distinction between ``Course`` and ``Section`` is subtle but crucial.
    A course effectively lives outside of time.  Faculty are never associated
    with a course.  Nor are semesters.  A section, by contrast, has associated
    with it a particular ``Semester`` as well as zero or many ``FacultyMember``
    objects (it is possible to have zero faculty for a ``Section`` in cases 
    where the faculty assignments are TBD.)
    
    It is Mike Edwards's **strong** recommendation that the ``taken`` field
    by replaced with code that defines an ``Affiliation``.  See the documentation
    of the ``reporting`` app for a complete explanation of the design decision
    to favor ``Affiliation`` objects over simple ManyToManyField fields.
    
    Also, the ``projects`` field should be refactored and removed, since the 
    ``Project`` model is deprecated.  It should be replaced with code that
    relates to ``Work`` objects instead, either as a ManyToMany or something
    similar to what the ``Affiliation`` object seeks to achieve between
    ``Person`` objects and every other DataMYNE class.
    
    """
    
    objects = Manager()
    current = CurrentCourseManager()
    archived = ArchivedCourseManager()

    TYPE_CHOICES = (
        ('studio', 'Studio'),
        ('lab', 'Lab'),
        ('seminar', 'Seminar'),
        ('lecture', 'Lecture'),
        ('recitation', 'Recitation'),
        ('workshop', 'Workshop'),
        ('practicum', 'Practicum'),
        ('critical', 'Critical Studio'),
        ('online', 'Online'), 
        ('admin', 'Administrative'),
        ('discussion', 'Discussion'),
        ('independent', 'Independent Study'), 
        ('internextern', 'Internship/Externship'),  
        ('maintenance', 'Equivalency & Maintain Status'),  
        ('exchange', 'Mobility/Exchange'),  
        ('private', 'Private Lessons'),
        ('group', 'Group Lessons'),
        ('mannesprep', 'Mannes Prep'),
        # @todo importer should handle case specially and select format, too
    )

    FORMAT_CHOICES = (
        ('online', 'Online'),
        ('onsite', 'Onsite'),
        ('blended', 'Blended')
    )
    
    METHOD_CHOICES = (
        ('practice','Practice'),
        ('theory','Theory')
    )
    
    STATUS_CHOICES = (
        ('r', 'Required'),
        ('e', 'Elective')
    )
    
    CREDIT_RANGE_CHOICES = (
        ('no', 'No range'),
        ('to', 'To'),
        ('or', 'Or'),
    )
    
    LEVELS_CHOICES = (
        ('doctoral', 'Doctoral'),
        ('graduate', 'Graduate'),
        ('undergraduate', 'Undergraduate'),
        ('associate', 'Associate'),
        ('non-degree', 'Non-degree'),
        ('non-credit', 'Non-credit'),
        ('certificate', 'Certificate'),
    )
    
    title               = CharField(max_length=255)
    coursenumber        = CharField(max_length=10)
    subject             = ForeignKey(Subject)
    tags                = TagField(max_length=2000)

    minimum_credits     = FloatField(default=0.0)
    credit_range_type   = CharField(max_length=2,choices=CREDIT_RANGE_CHOICES,default="no")
    maximum_credits     = FloatField(blank=True,null=True)
    
    attributes          = CharField(max_length=255,null=True,blank=True)
    levels              = CharField(max_length=255,choices=LEVELS_CHOICES,null=True,blank=True)
    type                = CharField(max_length=255,choices=TYPE_CHOICES,null=True,blank=True) 
    format              = CharField(max_length=255,choices=FORMAT_CHOICES,null=True,blank=True)
    method              = CharField(max_length=255,choices=METHOD_CHOICES,null=True,blank=True)
    description         = TextField(null=True,blank=True)
    learning_outcomes   = TextField(null=True,blank=True) 
    timeline            = TextField(null=True,blank=True)                         
    status              = CharField(max_length=2,choices=STATUS_CHOICES,null=True,blank=True)
    prerequisites       = ManyToManyField( 'Course', blank=True, null=True,
                                           symmetrical=False, related_name="dependents" )
    projects            = ManyToManyField(Project,blank=True,null=True)
    taken               = ManyToManyField(Student,blank=True,null=True)
    
    is_archived         = BooleanField(default=False)
    archived_at         = DateTimeField(null=True,blank=True)
    
    def demo_section(self):
        sections = Section.objects.filter(course=self,use_as_demo=True)
        for i in sections:
            return i

    def display_subject_number(self):
        return Subject.objects.get(course=self).abbreviation + ' ' + self.coursenumber
    
    # @todo later, add what school/division this course is open to?
    
    def __unicode__ (self):
        try:
            return "%s (%s %s)" % (self.title, self.subject, self.coursenumber)
        except:
            return "%s (%s)" % (self.title, self.coursenumber)
           
    @models.permalink
    def get_absolute_url(self):                      
        return ('view-course', [str(self.id)])
    
    def get_unit(self):
        """
        A ``Course`` is assumed to be under the authority of whatever
        organizational unit manages the course's ``Subject`` object.
        
        """
        
        return self.subject.get_unit()

def index_course(sender, *args, **kwargs): 
    from haystack import site
    site.get_indexes()[Course].update_object(kwargs['instance']) 
#        if kwargs['instance'].description is not None:
#            CalaisDocument.objects.analyze(kwargs['instance'],fields=[('description','text/html')])
post_save.connect(index_course, sender=Course) 

class Requirement(BaseModel):
    """
    A ``Requirement`` connects a ``Program`` to zero or more ``Course`` objects
    in order to define a program's requirements.
    
    Although this relationship exists in the model code, there are currently
    no tools to manage this outside of the admin tool.  Considerable thought and
    planning needs to go into how to manage this, as well as other models such
    as ``AreaOfStudy``, etc.
    
    """
    
    title = CharField(max_length=255)
    description = TextField(blank=True, null=True)
    program = ForeignKey(Program, related_name="requirements")
    courses = ManyToManyField(Course, related_name="fulfils_requirements",blank=True,null=True)
        
class CourseImage(BaseModel):
    """
    A ``CourseImage`` connects a ``Course`` to an image file and associated metadata.
    
    It is Mike Edwards's **strong** recommendation that this be refactored and
    migrated into a generic ``Image`` class that can relate the same data to a
    GenericForeignKey.  This would allow images to decorate any other object within
    the DataMYNE system, allowing for a common set of code to handle image assets,
    rather than duplicating the effort.  In addition, it may also be worth considering
    how a generic ``Image`` object could inherit from a generic ``Media`` object, 
    leaving open the possibility of achieving similar efficiency for video, audio, 
    and other unforeseen media.
    
    Of course, some of this addresses issues at the heart of what DataMYNE is and
    what it ought to be.  The degree to which this system stores (or references)
    other data depends largely on how much data needs to be internally understood
    by the system (for the purposes of searching, cross-referencing, etc.) and how
    much ought to be offloaded to the rest of the Web (e.g. Flickr, YouTube, etc.)
    At the time of writing, this issue is still very much in flux.  As such,
    designing for flexibility (instead of performance or simplicity) is paramount.

    """
    
    def image_filename (self, filename):
        if not self.course.id:
            raise Exception("oops, trying to save image for course that doesn't exist yet")
        return 'user/images/c-%s-%s' % (self.course.id,filename)
    
    url = URLField(verify_exists=False,help_text="Provide links with images to courses")
    image = ImageField(upload_to=image_filename)
    course = ForeignKey(Course)
    title = CharField(max_length=255, blank=True, null=True)
    author = CharField(max_length=255, blank=True, null=True)
    type = CharField(max_length=255, blank=True, null=True)
    year = PositiveIntegerField(max_length=4,blank=True,null=True)
                                                   
class RemoveSectionManager(models.Manager):
    use_for_related_fields = True
    
    def get_query_set(self):
        return super(RemoveSectionManager, self).get_query_set().exclude(course__title__exact='Independent Study').exclude(course__title__exact='Professional Internship')

    def recent(self):
        from datetime import timedelta
        year = timedelta(days=365)
        end_date = datetime.today()
        start_date = end_date - year   
        return self.get_query_set().filter(semester__start_date__range=(start_date,end_date))

class Section(BaseModel):
    """
    A ``Section`` object is connected to a course and shows only the information
    that is specific to a particular semester and set of faculty. A ``Course`` is 
    an object that contains course information across time.  
    
    Refer to the ``Course`` documentation for a more complete explanation of this
    distinction.
    
    """
    objects = RemoveSectionManager()
    
    class Meta:
        ordering = ['-semester',]
    
    def get_syllabus_filename (self, filename):
        if not self.id:
            raise Error("oops, trying to save syllabus for section that doesn't exist yet")
        return 'user/syllabus/%s-%s' % (self.id,filename)

    course      = ForeignKey(Course)
    use_as_demo = BooleanField(default=False)
    semester    = ForeignKey(Semester)
    syllabus    = FileField(upload_to=get_syllabus_filename,blank=True,null=True)
    syllabus_orig_filename = CharField(max_length=255,blank=True)
    instructors = ManyToManyField(FacultyMember)
    title       = CharField(max_length=255,blank=True) # may override course title for this particular section
    crn         = IntegerField(max_length=4, default=0)
    projects    = ManyToManyField(Project,blank=True,null=True)
    credits     = FloatField(null=True,blank=True)
    feeds       = ManyToManyField(Feed,blank=True,null=True)
        
    def syllabus_text(self):
        # Uses the Solr search engine to dig out raw text from PDF and MS Word files.
        if self.syllabus:                    
            file_path = self.syllabus.path       
            try:
                if os.path.isfile(file_path):
                    txt = get_doc_contents(os.path.basename(self.syllabus.name), file_path)
                    return txt
            except UnicodeEncodeError:
		print "Skipping file {0} due to formatting issues.".format(self.syllabus)
                return ""
            except pycurl.error:
                # skipping because of formpost error, come back next time
                pass

    @models.permalink
    def get_absolute_url(self):
        return ('view-section', [str(self.id)])
              
    def get_display_title (self):
        """
        Not all sections need to have their own title, but there are enough cases
        where the section of a course has a meaningfully different title that
        this ought to be shown instead (e.g. Parsons AMT Collab studios)
        """
        
        if self.title:
            return self.title
        else:
            return self.course.title

    def __unicode__ (self):
        #return "%d" % (self.crn)
        return "%s, %s" % ( self.course, self.semester )
    
    def get_unit(self):
        # The unit associated with the ``Course`` is assumed to pertain here, too.
        return self.course.get_unit()
        
###############################################################
# Contact
###############################################################

FeedbackChoices = (
    ('Account Management', 'Account Management'),
    ('Report Errors', 'Report Errors'),
    ('General Inquiry', 'General Inquiry'),
)

class ContactEmail(BaseModel):
    """
    ``ContactEmail`` is legacy code that needs to be refactored out``
    
    """
    
    subject = CharField(max_length=255, choices=FeedbackChoices, blank=False)
    recipient = EmailField(max_length = 255, blank=False)
    
    def __unicode__ (self):
        return "%s: %s" % ( self.subject, self.recipient )
    
class Sponsorship(BaseModel):
    """ 
    A ``Sponsorship`` ties an organization to a bureaucratic unit, etc. 
    
    At the time of writing, this relationship exists only in the model code.
    The necessity of an organization's sponsorship will need to be determined
    as the ``Organization`` use cases and code achieve more maturity.
    
    See the ``Authority`` class within the ``reporting`` documentation for
    an analog to this between ``Committee`` objects and organizational units.
    
    """
    
    organization    = models.ForeignKey("Organization",related_name="sponsorships")
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    content_object  = generic.GenericForeignKey()
    
    class Meta:
        unique_together = ('organization', 'content_type', 'object_id')
        verbose_name_plural = "sponsorships"

    def __unicode__(self):
        return u"%s is sponsored by %s" % (self.organization,self.content_object)


class OrganizationType(BaseModel):
    """
    An ``OrganizationType`` defines a canonical category for ``Organization``
    objects (e.g. lab, center, institute, etc.)
    
    """
    
    name           = CharField(max_length=255)


class Organization(BaseModel):
    """
    An ``Organization`` is an object that represents any number of kinds of groups
    that may appear within the university.  It comprises everything from officially
    designated labs to ad hoc student groups.
    
    The ``projects`` field should be refactored out and, most likely, replaced with
    some kind of relationship to the ``Work`` model (either via a new ManyToMany field
    or something akin to how the ``Person`` models relates to other objects via the
    ``Affiliation``
    
    """
        
    def photo_filename (self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'org/'+filename

    title           = CharField(max_length=255)
    abbreviation    = CharField(max_length=255,blank=True,null=True)
    logo            = ImageField(upload_to=photo_filename,blank=True,null=True)
    description     = TextField()
    url             = URLField(verify_exists=True,blank=True,null=True)
    type            = ForeignKey(OrganizationType,related_name="organizations")
    projects        = ManyToManyField(Project,blank=True,null=True,related_name="org_projects")
    courses         = ManyToManyField(Course,blank=True,null=True,related_name="org_courses")
    tags            = TagField(max_length=2000)


    @models.permalink
    def get_absolute_url(self):
        return ('profiles_view_organization', [str(self.id)])

    def __unicode__(self):
        return u"%s" % (self.title)
    
    def has_unit_permission(self, user):
        """
        Organization models don't have a parent unit, therefore there are no unit 
        restrictions on this.  This situation may change if the ``Sponsorship``
        object becomes more widely used.
        
        """
        return True

def index_organization(sender, *args, **kwargs): 
    # updates an ``Organization`` in the search engine after every change to the object
    from haystack import site
    site.get_indexes()[Organization].update_object(kwargs['instance']) 
post_save.connect(index_organization, sender=Organization) 

    
class UnitPermission(Model):
    """
    A ``UnitPermission`` object attaches itself to a user and another DataMYNE
    object, most suitably an organizational unit (e.g. ``Division``, ``Program``).
    
    Unit permissions allow for an expanded authorization framework that goes
    beyond the stock permissions built into Django which are based solely on
    ``ContentType``.  For example, a user may:
    
    * have permission to change only ``Course`` objects
    * have permission to change only objects that falls under the Parsons ``Division``
    
    The effect of this is to create a matrix that constrains administrators to
    only edit certain kind of objects and only object that fall under their
    purview.  
    
    At the time of writing, this can be managed from within the admin tool by
    DataMYNE administrators.  The administrator need to go to a unit's admin
    page (e.g. Parsons) and, under the Unit Permissions section, add only those
    users who are able to act on behalf of the unit (e.g. an operations manager
    for Parsons, a program director of Communication Design, etc.)
    
    While this addresses the problem of how to restrict editorial permissions
    to both object (via Django's system) and unit, more work needs to be done
    on creating an effective set of admin interfaces that could allow the 
    assignment of unit permissions by people within the university, rather
    than the rather rough way DataMYNE administrators need to work now
    within the admin tool.  This will become especially important as the
    system expands to cover the entire university.
    
    """
    
    user = models.ForeignKey(User,related_name="unit_permissions")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        verbose_name_plural = "unit permissions"

    def __unicode__(self):
        return u"%s has permission under %s" % (self.user,self.content_object)

class Invitation(Model):
    """
    An ``Invitation`` object allows a ``host`` user to invite a ``guest`` user
    to be part of another object within the DataMYNE system.  The guest can either 
    be a registered user or someone with an email address outside of the university.
    
    Once a guest receives his or her invitation email, they are directed to follow
    a url (composed of a unique ``slug``) that will do one of the following:
    
    * if the user is a member of DataMYNE and is signed in, he or she will be taken
      directly to the object in question
    
    * if the user is a member of DataMYNE and is not signed it, he or she will be
      taken first to a login screen
    
    * if the user is not yet a member of DataMYNE, he or she will still be directed
      to the login screen.  
    
      * If he or she is able to join (e.g. has a listing within LDAP), a profile will
        automatically be created.
    
      * If he or shee is not able to join, at this point, tough luck.
    
    This last case is an interesting one, since DataMYNE still represents a closed
    community.  The best way to deal with this is most likely best handled within
    the ``profiles.backends`` module.  This will be most important for alumni who
    no longer can authenticate through LDAP, as well as incoming students who are
    not yet established within LDAP.  In any case, the ``Invitation`` model should
    remain more or less agnostic to this.
    
    """
    
    slug            = UUIDField()
    host            = models.ForeignKey(Person, related_name="invitations_sent")
    guest           = models.ForeignKey(Person, related_name="invitations_received", blank=True, null=True)
    guest_email     = models.EmailField(blank=True, null=True)
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    content_object  = generic.GenericForeignKey()
    created_at      = DateTimeField(auto_now_add=True,editable=False)
    updated_at      = DateTimeField(auto_now=True,editable=False)
    received_at     = DateTimeField(blank=True, null=True)
    accepted_at     = DateTimeField(blank=True, null=True)
    message         = TextField(blank=True, null=True)

    def __unicode__(self):
        if self.guest is not None:
            return u"%s invited %s to %s" % (self.host,self.guest, self.content_object)
        elif self.guest_email:
            return u"%s invited %s to %s" % (self.host,self.guest_email, self.content_object)
        else:
            return u"%s invited someone to %s" % (self.host, self.content_object)

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_view_invitation', [self.slug])
              

