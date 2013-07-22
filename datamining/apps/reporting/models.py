from django.db import models
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from datamining.apps.profiles.models import BaseModel, Person, Work, AreaOfStudy,\
    Program, Department, School, Division, Organization
from datetime import datetime, timedelta
from django.contrib import comments
from django.db.models.signals import post_save, pre_delete
from django.utils import formats


class Role(BaseModel):
    """
    A ``Role`` is a refinement of ``Affiliation`` between a ``Person``
    and another object.  A roles has:
    
    title
      A role's title is simply that.  Good examples include "creator," as in
      "Jane Doe is the creator of Artwork X" and "chairperson," as in
      "John Does is the chairperson of Committee ABC"
       
    content_type
      A role must also have a content type.  This allows for there to be a 
      distinct "member" role, for example, in affiliations to both a
      ``Committee`` and an ``Organization``.
    
    """
    
    title       = models.CharField(max_length=255)
    content_type= models.ForeignKey(ContentType,related_name="roles")

    def __unicode__(self):
        return u"%s for a %s" % (self.title,self.content_type)
    
class AffiliationCurrentManager(models.Manager):
    """
    This manager show affiliations that exist between two dates OR without
    any dates OR where there is a previous start but not an end OR where
    there is no start date but a future end date.
    
    This affiliation manager, like all the others, allows for affiliations
    to be begun or retired en masse.
     
    """
    
    use_for_related_fields = True

    def get_query_set(self):
        # find all affilations started before now and ending after now OR where start and end are blank
        return super(AffiliationCurrentManager, self).get_query_set().filter(
                                                                             Q(start_date__lte = datetime.now()) &
                                                                             Q(end_date__gte = datetime.now()) |
                                                                             Q(start_date = None) &
                                                                             Q(end_date = None) |
                                                                             Q(start_date__lte = datetime.now()) &
                                                                             Q(end_date = None) |
                                                                             Q(start_date = None) &
                                                                             Q(end_date__gte = datetime.now())
                                                                             )
        
    def begin_all(self,role,content_type,object_id):
        qs = self.filter(role=role,content_type=content_type,object_id=object_id)
        for object in qs:
            object.begin()
        
    def retire_all(self,role,content_type,object_id):
        qs = self.filter(role=role,content_type=content_type,object_id=object_id)
        for object in qs:
            object.retire()
        

class AffiliationPastManager(AffiliationCurrentManager):
    """
    This manager only lists affiliations whose end date is in the past.
    
    """
    
    use_for_related_fields = True

    def get_query_set(self):
        # find all affilations ending before now 
        return super(AffiliationCurrentManager, self).get_query_set().filter(end_date__lt = datetime.now())
    
class AffiliationFutureManager(AffiliationCurrentManager):
    """
    This manager only lists affiliations whose start date is in the future.
    
    """
    
    use_for_related_fields = True

    def get_query_set(self):
        # find all affilations starting after now 
        return super(AffiliationCurrentManager, self).get_query_set().filter(start_date__gt = datetime.now())
    
    
    
class Affiliation(BaseModel):
    """
    The ``Affiliation`` objects are both useful and pervasive in the current DataMYNE
    system.  In almost all cases, they have superseded the use of the ``ManyToManyField``
    for the *``Person`` to other objects* relationships.  They have the following
    advantages:
    
    * They are generic.  This means we do not need to redefine the relationship field on 
      every new object we make.  Instead, we can assume that **any** new model will be 
      able to form a many-to-many relationship to a person via an ``Affiliation``.
      
    * They have a ``Role``.  We can therefore create several different kinds of
      relationships between a ``Person`` and an object.  For example, a ``Committee``
      can have both a chairperson and a member.
      
    * They have a start and end date.  This allows us to maintain old relationships,
      and embargo new relationships, without have to delete links.  This is useful
      historically and for data-mining purposes.  For example, we can create a history
      of all of a ``Committee``'s chairs as far back as we like.  
      
      * The use of the ``begin`` and ``retire`` methods is encouraged in maintaining
        current and past affiliations.  An ``embargo`` method would probably also be
        useful for maintaining future affiliations (e.g. an incoming committee chair.)
    
    """
    
    person          = models.ForeignKey(Person,related_name="affiliations")
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    content_object  = generic.GenericForeignKey()
    role            = models.ForeignKey(Role,related_name="affiliations",blank=True,null=True)
    start_date      = models.DateTimeField(blank=True,null=True)
    end_date        = models.DateTimeField(blank=True,null=True)

    objects = models.Manager()  # The default manager
    current = AffiliationCurrentManager()  # Only current affiliations
    past = AffiliationPastManager()  # Only past affiliations
    future = AffiliationFutureManager()  # Only future affiliations

    class Meta:
        unique_together = ('person', 'content_type', 'object_id', 'role')

    def __unicode__(self):
        if self.role is not None:
            return u"%s is a %s of %s" % (self.person,self.role.title,self.content_object)
        else:
            return u"%s is related to %s" % (self.person,self.content_object)
        
    def begin(self):
        if self.start_date is None:
            self.start_date = datetime.now()
        if self.end_date is not None:
            self.end_date = None
        self.save()
            
    def retire(self):
        self.end_date = datetime.now()
        self.save()
            
field = generic.GenericRelation(Affiliation)
field.contribute_to_class(Work,"affiliations")
Work.affiliations = generic.ReverseGenericRelatedObjectsDescriptor(field)

field = generic.GenericRelation(Affiliation)
field.contribute_to_class(Program,"affiliations")
Program.affiliations = generic.ReverseGenericRelatedObjectsDescriptor(field)

def delete_program_affiliations(sender, *args, **kwargs): 
    program = kwargs['instance']
    affiliations = Affiliation.current.filter(content_type__name="program",object_id = program.id)
    affiliations.delete()
pre_delete.connect(delete_program_affiliations, sender=Program) 


field = generic.GenericRelation(Affiliation)
field.contribute_to_class(AreaOfStudy,"affiliations")
AreaOfStudy.affiliations = generic.ReverseGenericRelatedObjectsDescriptor(field)

def delete_area_of_study_affiliations(sender, *args, **kwargs): 
    area_of_study = kwargs['instance']
    affiliations = Affiliation.current.filter(content_type__name="area_of_study",object_id = area_of_study.id)
    affiliations.delete()
pre_delete.connect(delete_area_of_study_affiliations, sender=AreaOfStudy) 


field = generic.GenericRelation(Affiliation)
field.contribute_to_class(Organization,"affiliations")
Organization.affiliations = generic.ReverseGenericRelatedObjectsDescriptor(field)

def delete_organization_affiliations(sender, *args, **kwargs): 
    organization = kwargs['instance']
    affiliations = Affiliation.current.filter(content_type__name="organization",object_id = organization.id)
    affiliations.delete()
pre_delete.connect(delete_organization_affiliations, sender=Organization) 

    
class Meeting(BaseModel):
    """
    A ``Meeting`` generically connects itself to any other object.  This allows other
    models like ``Committee`` and ``Organization`` to use the same meeting code.
    
    """
    
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    content_object  = generic.GenericForeignKey()
    start_time      = models.DateTimeField()
    end_time        = models.DateTimeField()
    location        = models.TextField(blank=True,null=True)
    agenda          = models.TextField(blank=True,null=True)
    minutes         = models.TextField(blank=True,null=True)
    
    class Meta:
        unique_together = ('content_type', 'object_id')

    def __unicode__(self):
        return "%s Meeting, %s" % (self.content_object, formats.date_format(self.start_time,"DATETIME_FORMAT"))

    @models.permalink
    def get_absolute_url(self):
        return ('reporting_view_meeting', [str(self.id)])

    def accept_invitation(self,invitation):
        content_type = ContentType.objects.get_by_natural_key("reporting", "meeting")
        role,created = Role.objects.get_or_create(title="invitee",content_type=content_type)
        
        current_membership,created = Affiliation.objects.get_or_create(role=role,content_type=content_type,person = invitation.guest, object_id = self.id)
        
        current_membership.begin()
        
        if invitation.accepted_at is None:
            invitation.accepted_at = datetime.now()
            invitation.save()
            
        return created

def index_meeting(sender, *args, **kwargs): 
    from haystack import site
    site.get_indexes()[Meeting].update_object(kwargs['instance']) 
post_save.connect(index_meeting, sender=Meeting) 
    
    
class MeetingManager(models.Manager):
    # based on the work of David Krauth in django-swingtime, this helps schedule meetings
    
    use_for_related_fields = True
    

    def range_occurences(self, start=None, end=None, content_type=None, object_id=None):
        qs = self.filter(
            models.Q(
                start_time__gte=start,
                start_time__lt=end,
            ) |
            models.Q(
                end_time__gte=start,
                end_time__lt=end,
            ) |
            models.Q(
                start_time__lt=start,
                end_time__gte=end
            )
        )
        
        if content_type is not None and object_id is not None:
            return qs.filter(content_type=content_type,object_id=object_id) 
        else:
            return qs

    def daily_occurrences(self, dt=None, content_type=None, object_id=None):
        '''
        Returns a queryset of for instances that have any overlap with a 
        particular day.
        
        * ``dt`` may be either a datetime.datetime, datetime.date object, or
          ``None``. If ``None``, default to the current day.
        
        * ``event`` can be an ``Event`` instance for further filtering.
        '''
        dt = dt or datetime.now()
        start = datetime(dt.year, dt.month, dt.day)
        end = start + timedelta(days=1)
        
        return self.range_occurences(start, end, content_type, object_id)
    
    
    def weekly_occurrences(self, dt=None, content_type=None, object_id=None):
        '''
        Returns a queryset of for instances that have any overlap with a 
        particular day.
        
        * ``dt`` may be either a datetime.datetime, datetime.date object, or
          ``None``. If ``None``, default to the current day.
        
        * ``event`` can be an ``Event`` instance for further filtering.
        '''
        dt = dt or datetime.now()
        start_week = datetime(dt.year, dt.month, dt.day).isocalendar()[1]
        year_start_date = datetime(dt.year,1,1)
        start = year_start_date + timedelta(weeks=start_week-1)
        end = year_start_date + timedelta(weeks=start_week)
        
        return self.range_occurences(start, end, content_type, object_id)
    
    
    def monthly_occurrences(self, dt=None, content_type=None, object_id=None):
        '''
        Returns a queryset of for instances that have any overlap with a 
        particular day.
        
        * ``dt`` may be either a datetime.datetime, datetime.date object, or
          ``None``. If ``None``, default to the current day.
        
        * ``event`` can be an ``Event`` instance for further filtering.
        '''
        dt = dt or datetime.now()
        start = datetime(dt.year,dt.month,1)
        if dt.month <= 12:
            end = datetime(dt.year,dt.month+1,1)
        else:
            end = datetime(dt.year+1,1,1)
        
        return self.range_occurences(start, end, content_type, object_id)

field = generic.GenericRelation(Meeting)
field.contribute_to_class(Organization,"meetings")
Organization.meetings = generic.ReverseGenericRelatedObjectsDescriptor(field)

def delete_organization_meetings(sender, *args, **kwargs): 
    organization = kwargs['instance']
    meetings = Meeting.objects.filter(content_type__name="organization",object_id = organization.id)
    meetings.delete()
pre_delete.connect(delete_organization_meetings, sender=Organization) 


    
class Committee(BaseModel):
    """
    A ``Committee`` is an official designated group of people who have a mandate and who
    presumably meet regularly.  A committee may have a parent committee to which it reports.
    It is more structured than an ``Organization`` and is attached to organization units
    such as ``Division`` or ``Program`` via the ``Authority`` objects.
    
    """
    
    title           = models.CharField(max_length=255)
    parent          = models.ForeignKey("Committee",related_name="subcommittees",blank=True,null=True)
    mandate         = models.TextField(blank=True,null=True)
    affiliations    = generic.GenericRelation(Affiliation)
    meetings        = generic.GenericRelation(Meeting)

    @models.permalink
    def get_absolute_url(self):
        return ('reporting_view_committee', [str(self.id)])
 
    def accept_invitation(self,invitation):
        content_type = ContentType.objects.get_by_natural_key("reporting", "committee")
        role,created = Role.objects.get_or_create(title="member",content_type=content_type)
        
        current_membership,created = Affiliation.objects.get_or_create(role=role,content_type=content_type,person = invitation.guest, object_id = self.id)
        
        current_membership.begin()
        
        if invitation.accepted_at is None:
            invitation.accepted_at = datetime.now()
            invitation.save()

        return created

    def get_unit(self):
        if self.authorities.count() > 0:
            return self.authorities.all()[0].content_object
        else:
            return None
    
def index_committee(sender, *args, **kwargs): 
    from haystack import site
    site.get_indexes()[Committee].update_object(kwargs['instance']) 
post_save.connect(index_committee, sender=Committee) 

def delete_committee_affiliations(sender, *args, **kwargs): 
    committee = kwargs['instance']
    affiliations = Affiliation.current.filter(content_type__name="committee",object_id = committee.id)
    affiliations.delete()
pre_delete.connect(delete_committee_affiliations, sender=Committee) 

def delete_committee_meetings(sender, *args, **kwargs): 
    committee = kwargs['instance']
    meetings = Meeting.objects.filter(content_type__name="committee",object_id = committee.id)
    meetings.delete()
pre_delete.connect(delete_committee_meetings, sender=Committee) 

    
class Authority(BaseModel):
    """
    An ``Authority`` defines the control of a committee by an organizational
    unit within the university (e.g. a ``Division``).
    
    """
    
    committee = models.ForeignKey(Committee,related_name="authorities")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    class Meta:
        unique_together = ('committee', 'content_type', 'object_id')
        verbose_name_plural = "authorities"

    def __unicode__(self):
        return u"%s is under the authority of %s" % (self.committee,self.content_object)

field = generic.GenericRelation(Authority)
field.contribute_to_class(Department,"authorities")
Department.authorities = generic.ReverseGenericRelatedObjectsDescriptor(field)

def delete_department_authorities(sender, *args, **kwargs): 
    department = kwargs['instance']
    authorities = Authority.objects.filter(content_type__name="department",object_id = department.id)
    authorities.delete()
pre_delete.connect(delete_department_authorities, sender=Department) 


field = generic.GenericRelation(Authority)
field.contribute_to_class(School,"authorities")
School.authorities = generic.ReverseGenericRelatedObjectsDescriptor(field)

def delete_school_authorities(sender, *args, **kwargs): 
    school = kwargs['instance']
    authorities = Authority.objects.filter(content_type__name="school",object_id = school.id)
    authorities.delete()
pre_delete.connect(delete_school_authorities, sender=School) 


field = generic.GenericRelation(Authority)
field.contribute_to_class(Division,"authorities")
Division.authorities = generic.ReverseGenericRelatedObjectsDescriptor(field)

def delete_division_authorities(sender, *args, **kwargs): 
    division = kwargs['instance']
    authorities = Authority.objects.filter(content_type__name="division",object_id = division.id)
    authorities.delete()
pre_delete.connect(delete_division_authorities, sender=Division) 


field = generic.GenericRelation(Authority)
field.contribute_to_class(Program,"authorities")
Program.authorities = generic.ReverseGenericRelatedObjectsDescriptor(field)

def delete_program_authorities(sender, *args, **kwargs): 
    program = kwargs['instance']
    authorities = Authority.objects.filter(content_type__name="program",object_id = program.id)
    authorities.delete()
pre_delete.connect(delete_program_authorities, sender=Program) 

