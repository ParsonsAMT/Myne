import BeautifulSoup

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse, resolve
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import *
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.html import *
import tagging
from tagging.models import Tag, TaggedItem
from tagging.utils import *
from tagging.views import tagged_object_list

from datamining.apps.profiles.models import Section, Person, FacultyMember,\
    Work, Expertise, Student, Project, WorkURL, Course, Program,\
    ContactEmail, Organization, Staff, Invitation, WorkType, AreaOfStudy
from datamining.apps.profiles.forms import *
from django.contrib.auth.models import Group, User
from datamining.libs.utils import NamePaginator, DataminingEmail
from django.core.paginator import InvalidPage
from django.core.servers.basehttp import FileWrapper
import mimetypes
import os
import random
from django.contrib.contenttypes.models import ContentType
from datamining.apps.reporting.models import Affiliation, Role
from django.forms.formsets import formset_factory
from haystack.query import SearchQuerySet
from django.core import validators
import datetime
from django.core.validators import EmailValidator, email_re
from djangocalais.models import CalaisDocument
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from urlparse import urlparse

from password_required.decorators import password_required
from BeautifulSoup import BeautifulSoup
from django.conf import settings



try:
    tagging.register(Person,tag_descriptor_attr='ptags')
except tagging.AlreadyRegistered:
    #there appear to be case when models.py is run twice, which results in the error
    pass

def home(request):
    """
    This is the home page of DataMYNE.  It calls the ``_random_images``
    function to generate a set of images that contain a mix of user
    profile images and work images.
    
    """

    cloud = Tag.objects.cloud_for_model(FacultyMember,steps=5,min_count=6)

    images = _random_images(18)
    
    from datamining.libs.truncate import truncate
    short_names = [ (truncate(str(i[0]), 18)) for i in images ]

    return render_to_response('home.html', {
            'cloud': cloud,
            'images': images,
            'short_names': short_names,
            },
            RequestContext(request, {}),
            )

# returns an array of N tuples (id, image) where id is a profile id,
# and image is an ImageField; drawn randomly from WorkImages and
# Faculty photos.
def _random_images(n):
    """
    `_random_images`` generates a set of images that contain a mix of user
    profile images and work images.  It excludes any profile or work that
    does not have an image associated with it.
    
    """

    num_work = random.randint(0,n)
    num_photo = n - num_work

    # TODO: work images could pull from inactive faculty. must fix. -rory
    works = Work.objects.exclude(image__isnull=True).exclude(image='')
    i = min(num_work,works.count())

    work_images = []     
    for work in random.sample(works,i):
        work_images.append((work,work.image))
#    work_images = [ (img.affiliations.all(), img.image) for img in random.sample(all_work_images,i) ]

    photo_people = Person.objects.exclude(photo__isnull=True).exclude(photo='')
    i = min(num_photo,photo_people.count())
    photo_images = [ (f, f.photo) for f in random.sample(photo_people,i) ]

    images = work_images + photo_images
    random.shuffle(images)
    
    return images

def _random_images_by_type(n, type):

    people = Person.objects.exclude(photo__isnull=True).exclude(photo='')
    photo_people = []
    for p in people:
        if _check_person_type(p.id, type):
            photo_people.append(p)
    
    i = min(n,len(photo_people))
    
    images = [ (f, f.photo) for f in random.sample(photo_people,i) ]

    random.shuffle(images)
    
    return images
    
def _check_person_type(id, type):
    
    if (type == "Faculty"):
        try:
            person = FacultyMember.objects.get(pk=id)
        except ObjectDoesNotExist:
            return False
        
    elif (type == "Student"):
        try:
            person = Student.objects.get(pk=id)
        except ObjectDoesNotExist:
            return False
    
    return True

def _random_images_organization(n):

    orgs = Organization.objects.exclude(logo__isnull=True).exclude(logo='')
    
    i = min(n,orgs.count())
    
    images = [ (f, f.logo) for f in random.sample(orgs,i) ]

    random.shuffle(images)
    
    return images

def list_profiles(request, tag=''):
    """
    This is a deprecated view.  It served primarily as destination for tag links, but has
    since been temporarily removed in favor of a direct link to the search results for a tag.
    
    """
    if tag:

        faculty_by_expertise = FacultyMember.actives.filter(expertise__name=tag)

        tag_instance = get_tag(tag)
        queryset = FacultyMember.actives.all().order_by('last_name')
        if tag_instance is not None:
            faculty_by_interest = TaggedItem.objects.get_by_model(queryset, tag_instance).exclude(pk__in=[f.id for f in faculty_by_expertise])
        else:
            faculty_by_interest = None

        return render_to_response('list_profiles.html', {
            'tag': tag_instance,
            'faculty_by_expertise': faculty_by_expertise,
            'faculty_by_interest': faculty_by_interest,
            },
            RequestContext(request, {}),
            )

    else:

        if request.GET.get('search') and not request.GET.get('clear'):
            search = request.GET.get('search')
            faculty_members = FacultyMember.actives.filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search) )
            page = {}
            page['object_list'] = faculty_members

        else:

            search = ''

            faculty_members = FacultyMember.actives.filter(user_account__isnull=False).order_by('last_name')

            paginator = NamePaginator(faculty_members, on="last_name", per_page=25)

            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1

            try:
                page = paginator.page(page)
            except (InvalidPage):
                page = paginator.page(paginator.num_pages)
                
            page_title = 'Faculty'

        return render_to_response('list_profiles_paginated.html', {
                'page': page,
                'search': search,
                'page_title': page_title,
                },
                RequestContext(request, {}),
                )
                
def list_student_profiles(request, tag=''):
    if tag:

        student_by_expertise = Student.actives.filter(expertise__name=tag)

        tag_instance = get_tag(tag)
        queryset = Student.actives.all().order_by('last_name')
        if tag_instance is not None:
            student_by_interest = TaggedItem.objects.get_by_model(queryset, tag_instance).exclude(pk__in=[f.id for f in student_by_expertise])
        else:
            student_by_interest = None

        return render_to_response('list_profiles.html', {
            'tag': tag_instance,
            'student_by_expertise': student_by_expertise,
            'student_by_interest': student_by_interest,
            },
            RequestContext(request, {}),
            )

    else:

        if request.GET.get('search') and not request.GET.get('clear'):
            search = request.GET.get('search')
            student_members = Student.actives.filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search) )
            page = {}
            page['object_list'] = student_members

        else:

            search = ''

            student_members = Student.actives.filter(user_account__isnull=False).order_by('last_name')

            paginator = NamePaginator(student_members, on="last_name", per_page=25)

            try:
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1

            try:
                page = paginator.page(page)
            except (InvalidPage):
                page = paginator.page(paginator.num_pages)
                
            page_title = 'Student'

        return render_to_response('list_profiles_paginated.html', {
                'page': page,
                'search': search,
                'page_title': page_title,
                },
                RequestContext(request, {}),
                )

def list_organization_profiles(request, tag=''):
    search = ''

    organizations = Organization.objects.all().order_by('title')

    paginator = NamePaginator(organizations, on="title", per_page=10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        page = paginator.page(page)
    except (InvalidPage):
        page = paginator.page(paginator.num_pages)
        
    page_title = 'Group'

    return render_to_response('list_profiles_paginated.html', {
            'page': page,
            'search': search,
            'page_title': page_title,
            },
            RequestContext(request, {}),
            )
                
def browse(request):
    """
    This is a deprecated view.  It served primarily as the *browse* page, which has
    since been temporarily removed from the main nav pending a redesign.
    
    """
    faculty_members = FacultyMember.actives.filter(user_account__isnull=False).order_by('last_name')
    
    paginator = NamePaginator(faculty_members, on="last_name", per_page=25)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        page = paginator.page(page)
    except (InvalidPage):
        page = paginator.page(paginator.num_pages)
        
    areas_of_expertise = Expertise.objects.all()
    
    cloud = Tag.objects.cloud_for_model(FacultyMember,steps=5,min_count=6)
    
    images = _random_images_by_type(18, "Faculty")
    
    from datamining.libs.truncate import truncate
    short_names = [ (truncate(str(i[0]), 18)) for i in images ]
    
    page_title = 'Faculty'
        
    return render_to_response('browse.html', {
                'page': page,
                'areas_of_expertise': areas_of_expertise,
                'cloud': cloud,
                'images': images,
                'short_names': short_names,
                'page_title': page_title,
                },
                RequestContext(request, {}),
                )

def browse_student(request):
    students = Student.actives.filter(user_account__isnull=False).order_by('last_name')
    
    paginator = NamePaginator(students, on="last_name", per_page=25)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        page = paginator.page(page)
    except (InvalidPage):
        page = paginator.page(paginator.num_pages)
    
    images = _random_images_by_type(18, "Student")
    
    from datamining.libs.truncate import truncate
    short_names = [ (truncate(str(i[0]), 18)) for i in images ]
    
    page_title = 'Student'
        
    return render_to_response('browse.html', {
                'page': page,
                'images': images,
                'short_names': short_names,
                'page_title': page_title,
                },
                RequestContext(request, {}),
                )

def browse_organization(request):
    organizations = Organization.objects.all().order_by('title')
    
    paginator = NamePaginator(organizations, on="title", per_page=10)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    
    try:
        page = paginator.page(page)
    except (InvalidPage):
        page = paginator.page(paginator.num_pages)
    
    images = _random_images_organization(18)
    
    from datamining.libs.truncate import truncate
    short_names = [ (truncate(str(i[0]), 18)) for i in images ]
    
    page_title = 'Group'
        
    return render_to_response('browse.html', {
                'page': page,
                'images': images,
                'short_names': short_names,
                'page_title': page_title,
                },
                RequestContext(request, {}),
                )

def view_person_profile(request, person_id):
    """
    This view serves to unify the ``FacultyMember``, ``Student``, and ``Staff``
    profile views under a single view.  Within the ``urls`` module, any person's
    role-specific profile can be reached from here.  This allows a common
    "gateway" to profiles without needing to decide, within the templates,
    which role a ``Person`` occupies.
    
    This should be the destination for all profile requests going forward.
    
    """
    
    person = get_object_or_404(Person, pk=int(person_id))
    
    try:
        return view_profile(request, person.facultymember.id)
    except (FacultyMember.DoesNotExist):
        try:
            return view_student_profile(request, person.student.id)
        except (Student.DoesNotExist):
            return view_staff_profile(request, person.staff.id)
        
def edit_person_profile(request, person_id):
    """
    This view serves to unify the ``FacultyMember``, ``Student``, and ``Staff``
    profile edit views under a single edit view.  Within the ``urls`` module, 
    any person's role-specific profile editing page can be reached from here.  
    This allows a common "gateway" to profiles editors without needing to decide, 
    within the templates, which role a ``Person`` occupies.
    
    This should be the destination for all profile edit requests going forward.
    
    """
    person = get_object_or_404(Person, pk=int(person_id))
    
    try:
        return edit_profile(request, person.facultymember.id)
    except (FacultyMember.DoesNotExist):
        try:
            return edit_student_profile(request, person.student.id)
        except (Student.DoesNotExist):
            return edit_staff_profile(request, person.staff.id)
        


def view_profile(request, person_id):
    """
    This is the profile view for ``FacultyMembers``.  Its function is pretty
    straightforward, but there are some tricky areas:
    
    * much of this code is similar to other ``Person`` objects.  This could be
      refactored into the ``view_person_profile`` view to reduce repetition.
    
    * edittable defines whether the Edit button appears.  This really needs
      to be refactored out of the view code and into the model code, either
      at the level of ``FacultyMember`` or, at least in part, at the level of
      ``Person`` itself.  The reason for this is that the combination of 
      Django permissions and unit permissions is becoming increasingly brittle.
      Unifying this with a well-written object method would improve security,
      reusability, and performance.
    
    * mlt refers to the ``more_like_this`` method available in ``haystack`` 
      (and, in turn, ``Solr``).  It produces what appears to be a fairly interesting
      list of related documents (i.e. other DataMYNE objects with sufficient
      document similarity).  However, this could be improved with a faceted search.
      For example, perhaps only other people and/or works are shown, but not courses
      or committees.  Further user testing is necessary to determine this.
    
    * OpenCalais code exists here which updates the OpenCalais objects in
      the background.  The OC code is still experimental within DataMYNE and
      should probably either be removed or made subject to a debug setting.
    
    """
    
    faculty = get_object_or_404(FacultyMember, pk=int(person_id))
    
    mlt = SearchQuerySet().more_like_this(faculty)[:5]

    user = getattr(request, 'user', None)
    edittable = ( user == faculty.user_account or faculty.has_unit_permission(user) and user.has_perm("profiles.change_facultymember") or user.is_staff)

    faculty.sections = faculty.section_set.all().order_by('-semester')

    work = Affiliation.current.filter(person=faculty,content_type=ContentType.objects.get(name="work"))

    invitations = []
    
    if user is not None and user == faculty.user_account:
        person = Person.objects.get(user_account = user)
        invitations = Invitation.objects.filter(guest=person, accepted_at__isnull = True )
        
    if len(invitations) > 0:
        request.user.message_set.create(message="You have open invitations! <a href=\"#invitations-block\">View them now</a>")

#    presentations = list(faculty.presentations.all())
    
    if edittable:
        can_read_cv = True
        can_read_syllabi = True
    elif request.user.is_authenticated():
        #if both are set, rely on the group permissions to decide who can view
        if faculty.person_ptr.group_perms_set.filter(permission = Person.perms.as_int(('read cv','read syllabi'))).count() > 0:#@UndefinedVariable
            can_read_syllabi = request.user.has_object_perm(faculty.person_ptr,"read syllabi")
            can_read_cv = request.user.has_object_perm(faculty.person_ptr,"read cv")
        else:                            
            if faculty.person_ptr.group_perms_set.filter(permission = Person.perms.as_int('read syllabi')).count() > 0:#@UndefinedVariable
                can_read_syllabi = request.user.has_object_perm(faculty.person_ptr,"read syllabi")
            else:
                #if no permission is set, this is the default.  True is open and opt-out!
                can_read_syllabi = True            
    
            if faculty.person_ptr.group_perms_set.filter(permission = Person.perms.as_int('read cv')).count() > 0:#@UndefinedVariable
                can_read_cv = request.user.has_object_perm(faculty.person_ptr,"read cv")
            else:
                #if no permission is set, this is the default.  True is open and opt-out!
                can_read_cv = True            
                
    else:
        can_read_cv = False
        can_read_syllabi = False
        
    docs = CalaisDocument.objects.filter(content_type__name = "faculty member", object_id = faculty.id)
    if docs.count() > 0:
        document = docs[0]
    else:
        if faculty.bio is not None:
            document = CalaisDocument.objects.analyze(faculty,fields=[('bio','text/html'),('cv_text','text/txt')])
        else:
            document = None
    
    #print dir(document.topics.all()[1])
    
    person = faculty
    
    return render_to_response('view_profile.html', {
            'faculty': faculty,
            'person': person,
            'edittable': edittable,
            'work': work,
            'can_read_cv': can_read_cv,
            'can_read_syllabi': can_read_syllabi,
            'mlt': mlt,
            'document': document,
            'invitations': invitations,
            },
            RequestContext(request, {}),
            )

def view_student_profile(request, person_id):
    """
    This is the profile view for ``Student`` objects.  Its function is pretty
    straightforward, but there are some tricky areas:
    
    * much of this code is similar to other ``Person`` objects.  This could be
      refactored into the ``view_person_profile`` view to reduce repetition.
    
    * edittable defines whether the Edit button appears.  This really needs
      to be refactored out of the view code and into the model code, either
      at the level of ``Student`` or, at least in part, at the level of
      ``Person`` itself.  The reason for this is that the combination of 
      Django permissions and unit permissions is becoming increasingly brittle.
      Unifying this with a well-written object method would improve security,
      reusability, and performance.
    
    * mlt refers to the ``more_like_this`` method available in ``haystack`` 
      (and, in turn, ``Solr``).  It produces what appears to be a fairly interesting
      list of related documents (i.e. other DataMYNE objects with sufficient
      document similarity).  However, this could be improved with a faceted search.
      For example, perhaps only other people and/or works are shown, but not courses
      or committees.  Further user testing is necessary to determine this.
    
    * OpenCalais code exists here which updates the OpenCalais objects in
      the background.  The OC code is still experimental within DataMYNE and
      should probably either be removed or made subject to a debug setting.
    
    """
    
    student = get_object_or_404(Student, pk=int(person_id))

    mlt = SearchQuerySet().more_like_this(student)[:5]

    user = getattr(request, 'user', None)
    edittable = ( user == student.user_account or student.has_unit_permission(user) and user.has_perm("profiles.change_student") or user.is_staff )
    
    cloud = Tag.objects.get_for_object(get_object_or_404(Person, pk=int(person_id)))
    
    work = Affiliation.current.filter(person=student,content_type=ContentType.objects.get(name="work"))
    
    invitations = []
    
    if user is not None and user == student.user_account:
        person = Person.objects.get(user_account = user)
        invitations = Invitation.objects.filter(guest=person, accepted_at__isnull = True )
        
    if len(invitations) > 0:
        request.user.message_set.create(message="You have open invitations! <a href=\"#invitations-block\">View them now</a>")

    if edittable:
        can_read_cv = True
        can_read_syllabi = True
    elif request.user.is_authenticated():
        #if both are set, rely on the group permissions to decide who can view
        if student.person_ptr.group_perms_set.filter(permission = Person.perms.as_int(('read cv','read syllabi'))).count() > 0:#@UndefinedVariable
            can_read_syllabi = request.user.has_object_perm(student.person_ptr,"read syllabi")
            can_read_cv = request.user.has_object_perm(student.person_ptr,"read cv")
        else:                            
            if student.person_ptr.group_perms_set.filter(permission = Person.perms.as_int('read syllabi')).count() > 0:#@UndefinedVariable
                can_read_syllabi = request.user.has_object_perm(student.person_ptr,"read syllabi")
            else:
                #if no permission is set, this is the default.  True is open and opt-out!
                can_read_syllabi = True            
    
            if student.person_ptr.group_perms_set.filter(permission = Person.perms.as_int('read cv')).count() > 0:#@UndefinedVariable
                can_read_cv = request.user.has_object_perm(student.person_ptr,"read cv")
            else:
                #if no permission is set, this is the default.  True is open and opt-out!
                can_read_cv = True            
                
    else:
        if student.person_ptr.group_perms_set.filter(permission = Person.perms.as_int('open cv')).count() > 0:#@UndefinedVariable
            can_read_cv = True
        else:
            can_read_cv = False
        
        if student.person_ptr.group_perms_set.filter(permission = Person.perms.as_int('open syllabi')).count() > 0:#@UndefinedVariable
            can_read_syllabi = True
        else:
            can_read_syllabi = False
    
    docs = CalaisDocument.objects.filter(content_type__name = "student", object_id = student.id)
    if docs.count() > 0:
        document = docs[0]
    else:
        if student.bio is not None:
            document = CalaisDocument.objects.analyze(student,fields=[('bio','text/html'),('cv_text','text/txt')])
        else:
            document = None
    
    person = student
    
    return render_to_response('view_student_profile.html', {
            'student': student,
            'person': person,
            'edittable': edittable,
            'cloud': cloud,
            'work': work,
            'can_read_cv': can_read_cv,
            'can_read_syllabi': can_read_syllabi,
            'mlt': mlt,
            'document': document,
            'invitations': invitations,
            },
            RequestContext(request, {}),
            )
            
def contact_student(request, person_id):
    """
    This view allows users to send students email without revealing the
    student's email address publicly.  
    
    There most likely should be a setting on the ``Student`` profile page
    which allows the student to disable this.  At time of writing, this
    does not exist in either model or view code and should be considered.
    
    """
    
    student = get_object_or_404(Student, pk=int(person_id))
    
    if request.method == 'POST':
        form = ContactStudentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subj = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            recipients = [student.user_account.username + '@' + settings.SCHOOL_URL, ]
            
            d = DataminingEmail( to=recipients,
                                 from_email='datamine@' + settings.SCHOOL_URL,
                                 subject=subj,
                                 body=message, 
                                 headers = {'Reply-To': "%s <%s>" % (name, email)} )
            d.send(fail_silently=False)
            thankyou = 'Your message has been sent.'
        else:
            thankyou = 'Invalid form.'
        
        #if user.is_authenticated():
        #    request.user.message_set.create(message=thankyou)
        return HttpResponseRedirect( reverse(view_student_profile, args=[student.id]) )
    else:
        form = ContactStudentForm()
    
    return render_to_response('contact_student.html', {
            'student': student,
            'form': form,
            },
            RequestContext(request, {}),
            )

def view_staff_profile(request, person_id):
    """
    This is the profile view for ``Staff`` objects.  Its function is pretty
    straightforward, but there are some tricky areas:
    
    * much of this code is similar to other ``Person`` objects.  This could be
      refactored into the ``view_person_profile`` view to reduce repetition.
    
    * edittable defines whether the Edit button appears.  This really needs
      to be refactored out of the view code and into the model code, either
      at the level of ``Staff`` or, at least in part, at the level of
      ``Person`` itself.  The reason for this is that the combination of 
      Django permissions and unit permissions is becoming increasingly brittle.
      Unifying this with a well-written object method would improve security,
      reusability, and performance.
    
    * mlt refers to the ``more_like_this`` method available in ``haystack`` 
      (and, in turn, ``Solr``).  It produces what appears to be a fairly interesting
      list of related documents (i.e. other DataMYNE objects with sufficient
      document similarity).  However, this could be improved with a faceted search.
      For example, perhaps only other people and/or works are shown, but not courses
      or committees.  Further user testing is necessary to determine this.
    
    * OpenCalais code exists here which updates the OpenCalais objects in
      the background.  The OC code is still experimental within DataMYNE and
      should probably either be removed or made subject to a debug setting.
    
    """
    
    staff = get_object_or_404(Staff, pk=int(person_id))

    mlt = SearchQuerySet().more_like_this(staff)[:5]

    user = getattr(request, 'user', None)
    edittable = ( user == staff.user_account or staff.has_unit_permission(user) and user.has_perm("profiles.change_staff") or user.is_staff)

    work = staff.affiliations.filter(person=staff,content_type=ContentType.objects.get(name="work"))

    committees = staff.affiliations.filter(person=staff,content_type=ContentType.objects.get(name="committee"))

    managers = Affiliation.objects.filter(object_id=staff.id,content_type=ContentType.objects.get(name="person"))

    reports = staff.affiliations.filter(person=staff,content_type=ContentType.objects.get(name="person"))

    invitations = []
    
    if user is not None and user == staff.user_account:
        person = Person.objects.get(user_account = user)
        invitations = Invitation.objects.filter(guest=person, accepted_at__isnull = True )
        
    if len(invitations) > 0:
        request.user.message_set.create(message="You have open invitations! <a href=\"#invitations-block\">View them now</a>")
    
    if edittable:
        can_read_cv = True
        can_read_syllabi = True
    elif request.user.is_authenticated():
        #if both are set, rely on the group permissions to decide who can view
        if staff.person_ptr.group_perms_set.filter(permission = Person.perms.as_int(('read cv','read syllabi'))).count() > 0: #@UndefinedVariable
            can_read_syllabi = request.user.has_object_perm(staff.person_ptr,"read syllabi")
            can_read_cv = request.user.has_object_perm(staff.person_ptr,"read cv")
        else:                            
            if staff.person_ptr.group_perms_set.filter(permission = Person.perms.as_int('read syllabi')).count() > 0: #@UndefinedVariable
                can_read_syllabi = request.user.has_object_perm(staff.person_ptr,"read syllabi")
            else:
                #if no permission is set, this is the default.  True is open and opt-out!
                can_read_syllabi = True            
    
            if staff.person_ptr.group_perms_set.filter(permission = Person.perms.as_int('read cv')).count() > 0: #@UndefinedVariable
                can_read_cv = request.user.has_object_perm(staff.person_ptr,"read cv")
            else:
                #if no permission is set, this is the default.  True is open and opt-out!
                can_read_cv = True            
                
    else:
        can_read_cv = False
        can_read_syllabi = False
    
    person = staff
    
    return render_to_response('profiles/staff.html', {
            'person': person,
            'staff': staff,
            'edittable': edittable,
            'work': work,
            'committees': committees,
            'managers': managers,
            'reports': reports,
            'can_read_cv': can_read_cv,
            'can_read_syllabi': can_read_syllabi,
            'mlt':mlt,
            'invitations': invitations,
            },
            RequestContext(request, {}),
            )

def view_project_profile(request, project_id):
    """
    This view, and its associated ``Project`` model, is deprecated and should
    be refactored out.
    
    """
    
    project = get_object_or_404(Project, pk=int(project_id))
    
    creator = get_object_or_404(Person, pk=int(project.creator_id))
    
    cloud = Tag.objects.get_for_object(project)
    
    return render_to_response('view_project_profile.html', {
            'project': project,
            'creator': creator,
            'cloud': cloud,
            },
            RequestContext(request, {}),
            )

@login_required
def edit_profile(request, faculty_id):
    """
    This is the profile edit view for ``FacultyMember`` objects.  Its function is pretty
    straightforward, but there are some tricky areas:
    
    * much of this code is similar to other ``Person`` objects.  This could be
      refactored into the ``edit_person_profile`` view to reduce repetition.
    
    * edittable defines whether a user can edit this object.  This really needs
      to be refactored out of the view code and into the model code, either
      at the level of ``FacultyMember`` or, at least in part, at the level of
      ``Person`` itself.  The reason for this is that the combination of 
      Django permissions and unit permissions is becoming increasingly brittle.
      Unifying this with a well-written object method would improve security,
      reusability, and performance.
      
    * There are really two edit views: one for regular users and one for admins.
      Be sensitive to the distinction, since admins have access to many fields
      that we do not want users to be able to update (e.g. field provided by
      Banner, etc.)

    """
    
    faculty = get_object_or_404(FacultyMember, pk=int(faculty_id))

    faculty.sections = faculty.section_set.order_by('-semester')

    user = getattr(request, 'user', None)

    edittable = ( user == faculty.user_account or faculty.has_unit_permission(user) and user.has_perm("profiles.change_facultymember") or user.is_staff )

    if not edittable:
        return HttpResponseForbidden("You do not have access to edit this profile.")

    from django.forms.models import inlineformset_factory
    from django.forms.models import modelformset_factory
    WorkURLFormSet = inlineformset_factory(Person,WorkURL,form=WorkURLForm,extra=1)
    SectionFormSet = modelformset_factory(Section,fields=('title',),extra=0)

    areas_of_expertise = Expertise.objects.all()
    selected_areas = ", ".join( [ str(e.id) for e in faculty.expertise.all() ] )

    try:
        admins = Group.objects.get(name="Administrators")
    except:
        admins = None
            
    if request.method == 'POST':

        if user.is_staff:
            faculty_form = AdminFacultyForm(request.POST,request.FILES,instance=faculty)
        else:
            faculty_form = FacultyForm(request.POST,request.FILES,instance=faculty)
            
        workurl_formset = WorkURLFormSet(request.POST,instance=faculty)
        #queryset=[a.content_object for a in faculty.affiliations.filter(content_type=ContentType.objects.get(name="work"))])
        section_formset = SectionFormSet(request.POST,prefix="section",queryset=faculty.section_set.all())

        if ( faculty_form.is_valid() and workurl_formset.is_valid() and section_formset.is_valid()):

#            selected_areas = ", ".join( [ str(e.id) for e in faculty_form.clean_expertise()] )
        
            faculty.ptags = faculty_form.cleaned_data['tags'].replace('\n',' ')
        
            if admins is not None:
                if faculty_form.cleaned_data['allow_cv_viewing_by'] == "O":
                    admins.grant_object_perm(faculty.person_ptr,"read cv")
                else:
                    admins.revoke_object_perm(faculty.person_ptr,"read cv")

                if faculty_form.cleaned_data['allow_syllabus_viewing_by'] == "O":
                    admins.grant_object_perm(faculty.person_ptr,"read syllabi")
                else:
                    admins.revoke_object_perm(faculty.person_ptr,"read syllabi")

            faculty_form.save()
            workurl_formset.save()
            section_formset.save()

            request.user.message_set.create(message="Profile changes were saved.")

            return HttpResponseRedirect( reverse(view_profile, args=[faculty.id]) )

    else:
        faculty.tags = tagging.utils.edit_string_for_tags(faculty.ptags)

        #check permissions settings
        admin_read_cv = False
        admin_read_syllabi = False

        if admins is not None:
            group_perms = faculty.person_ptr.group_perms_set.filter(group = admins)
            if group_perms.count() > 0:
                for perm in group_perms:
                    if "read cv" in Person.perms.as_string_list(int(perm.permission)): #@UndefinedVariable
                        admin_read_cv = True
                    if  "read syllabi" in Person.perms.as_string_list(int(perm.permission)): #@UndefinedVariable
                        admin_read_syllabi = True
        
        default_data = {}
        
        if admin_read_cv:
            default_data["allow_cv_viewing_by"] = "O"
        else:
            default_data["allow_cv_viewing_by"] = "A"

        if admin_read_syllabi:
            default_data["allow_syllabus_viewing_by"] = "O"
        else:
            default_data["allow_syllabus_viewing_by"] = "A"

        if user.is_staff:
            faculty_form = AdminFacultyForm(initial=default_data, instance=faculty)
        else:
            faculty_form = FacultyForm(initial=default_data, instance=faculty)
                

        workurl_formset = WorkURLFormSet(instance=faculty)
        section_formset = SectionFormSet(prefix="section",queryset=faculty.section_set.all())

    return render_to_response('edit_profile.html', {
            'faculty': faculty,
            'selected_areas': selected_areas,
            'areas_of_expertise': areas_of_expertise,
            'faculty_form': faculty_form,
            'workurl_formset': workurl_formset,
            'section_formset': section_formset,
            },
            RequestContext(request, {}),
            )

@login_required
def edit_student_profile(request, student_id):
    """
    This is the profile edit view for ``Student`` objects.  Its function is pretty
    straightforward, but there are some tricky areas:
    
    * much of this code is similar to other ``Person`` objects.  This could be
      refactored into the ``edit_person_profile`` view to reduce repetition.
    
    * edittable defines whether a user can edit this object.  This really needs
      to be refactored out of the view code and into the model code, either
      at the level of ``Student`` or, at least in part, at the level of
      ``Person`` itself.  The reason for this is that the combination of 
      Django permissions and unit permissions is becoming increasingly brittle.
      Unifying this with a well-written object method would improve security,
      reusability, and performance.
      
    * There are really two edit views: one for regular users and one for admins.
      Be sensitive to the distinction, since admins have access to many fields
      that we do not want users to be able to update (e.g. field provided by
      Banner, etc.)

    """
    
    student = get_object_or_404(Student, pk=int(student_id))
    
    user = getattr(request, 'user', None)
    
    edittable = ( user == student.user_account or student.has_unit_permission(user) and user.has_perm("profiles.change_student") or user.is_staff )

    if not edittable:
        return HttpResponseForbidden("You do not have access to edit this profile.")
        
    from django.forms.models import inlineformset_factory
    from django.forms.models import modelformset_factory
    WorkURLFormSet = inlineformset_factory(Person,WorkURL,form=WorkURLForm,extra=1)
    
    areas_of_expertise = Expertise.objects.all()
    selected_areas = ", ".join( [ str(e.id) for e in student.expertise.all() ] )

    try:
        admins = Group.objects.get(name="Administrators")
    except:
        admins = None
    
    if request.method == 'POST':


        if user.is_staff:
            student_form = AdminStudentForm(request.POST,request.FILES,instance=student)
        else:
            student_form = StudentForm(request.POST,request.FILES,instance=student)

        workurl_formset = WorkURLFormSet(request.POST,instance=student)

        if (student_form.is_valid() and workurl_formset.is_valid()):
            student.ptags = student_form.cleaned_data['tags'].replace('\n',' ')
            
            if admins is not None:
                if student_form.cleaned_data['allow_cv_viewing_by'] == "P":
                    admins.grant_object_perm(student.person_ptr,"open cv")
                elif student_form.cleaned_data['allow_cv_viewing_by'] == "O":
                    admins.grant_object_perm(student.person_ptr,"read cv")
                else:
                    admins.revoke_object_perm(student.person_ptr,"open cv")
                    admins.revoke_object_perm(student.person_ptr,"read cv")

                if student_form.cleaned_data['allow_syllabus_viewing_by'] == "P":
                    admins.grant_object_perm(student.person_ptr,"open syllabi")
                elif student_form.cleaned_data['allow_syllabus_viewing_by'] == "O":
                    admins.grant_object_perm(student.person_ptr,"read syllabi")
                else:
                    admins.revoke_object_perm(student.person_ptr,"open syllabi")
                    admins.revoke_object_perm(student.person_ptr,"read syllabi")

            student_form.save()
            workurl_formset.save()
            
            request.user.message_set.create(message="Profile changes were saved.")

            return HttpResponseRedirect( reverse(view_student_profile, args=[student.id]) )

    else:
        student.tags = tagging.utils.edit_string_for_tags(student.ptags)

        #check permissions settings
        admin_read_cv = False
        admin_read_syllabi = False

        if admins is not None:
            group_perms = student.person_ptr.group_perms_set.filter(group = admins)
            if group_perms.count() > 0:
                for perm in group_perms:
                    if "read cv" in Person.perms.as_string_list(int(perm.permission)): #@UndefinedVariable
                        admin_read_cv = True
                    if "read syllabi" in Person.perms.as_string_list(int(perm.permission)): #@UndefinedVariable
                        admin_read_syllabi = True
        
        default_data = {}
        
        if admin_read_cv:
            default_data["allow_cv_viewing_by"] = "O"
        else:
            default_data["allow_cv_viewing_by"] = "A"

        if admin_read_syllabi:
            default_data["allow_syllabus_viewing_by"] = "O"
        else:
            default_data["allow_syllabus_viewing_by"] = "A"

        if user.is_staff:
            student_form = AdminStudentForm(instance=student)
        else:
            student_form = StudentForm(instance=student)

        workurl_formset = WorkURLFormSet(instance=student)
        
    return render_to_response('edit_student_profile.html', {
            'student': student,
            'selected_areas': selected_areas,
            'areas_of_expertise': areas_of_expertise,
            'student_form': student_form,
            'workurl_formset': workurl_formset,
            },
            RequestContext(request, {}),
            )
    
@login_required
def edit_staff_profile(request, person_id):
    """
    This is the profile edit view for ``Staff`` objects.  Its function is pretty
    straightforward, but there are some tricky areas:
    
    * much of this code is similar to other ``Person`` objects.  This could be
      refactored into the ``edit_person_profile`` view to reduce repetition.
    
    * edittable defines whether a user can edit this object.  This really needs
      to be refactored out of the view code and into the model code, either
      at the level of ``Staff`` or, at least in part, at the level of
      ``Person`` itself.  The reason for this is that the combination of 
      Django permissions and unit permissions is becoming increasingly brittle.
      Unifying this with a well-written object method would improve security,
      reusability, and performance.
      
    * There are really two edit views: one for regular users and one for admins.
      Be sensitive to the distinction, since admins have access to many fields
      that we do not want users to be able to update (e.g. field provided by
      Banner, etc.)

    """

    staff = get_object_or_404(Staff, pk=int(person_id))
    
    user = getattr(request, 'user', None)
    
    edittable = ( user == staff.user_account or staff.has_unit_permission(user) and user.has_perm("profiles.change_staff") or user.is_staff )

    if not edittable:
        return HttpResponseForbidden("You do not have access to edit this profile.")
            
    areas_of_expertise = Expertise.objects.all()
    selected_areas = ", ".join( [ str(e.id) for e in staff.expertise.all() ] )

    try:
        admins = Group.objects.get(name="Administrators")
    except:
        admins = None
    
    if request.method == 'POST':

        if user.is_staff:
            staff_form = AdminStaffForm(request.POST,request.FILES,instance=staff)
        else:
            staff_form = StaffForm(request.POST,request.FILES,instance=staff)

        if (staff_form.is_valid()):
            staff.ptags = staff_form.cleaned_data['tags'].replace('\n',' ')

            if admins is not None:
                if staff_form.cleaned_data['allow_cv_viewing_by'] == "O":
                    admins.grant_object_perm(staff.person_ptr,"read cv")
                else:
                    admins.revoke_object_perm(staff.person_ptr,"read cv")

            staff_form.save()
            request.user.message_set.create(message="Profile changes were saved.")

            return HttpResponseRedirect( reverse(view_person_profile, args=[staff.id]) )

    else:
        staff.tags = tagging.utils.edit_string_for_tags(staff.ptags)

        #check permissions settings
        admin_read_cv = False
        admin_read_syllabi = False

        if admins is not None:
            group_perms = staff.person_ptr.group_perms_set.filter(group = admins)
            if group_perms.count() > 0:
                for perm in group_perms:
                    if "read cv" in Person.perms.as_string_list(int(perm.permission)): #@UndefinedVariable
                        admin_read_cv = True
                    if  "read syllabi" in Person.perms.as_string_list(int(perm.permission)): #@UndefinedVariable
                        admin_read_syllabi = True
        
        default_data = {}
        
        if admin_read_cv:
            default_data["allow_cv_viewing_by"] = "O"
        else:
            default_data["allow_cv_viewing_by"] = "A"

        if admin_read_syllabi:
            default_data["allow_syllabus_viewing_by"] = "O"
        else:
            default_data["allow_syllabus_viewing_by"] = "A"

        if user.is_staff:
            staff_form = AdminStaffForm(initial=default_data, instance=staff)
        else:
            staff_form = StaffForm(initial=default_data, instance=staff)
                

    return render_to_response('profiles/edit/staff.html', {
            'staff': staff,
            'selected_areas': selected_areas,
            'areas_of_expertise': areas_of_expertise,
            'staff_form': staff_form,
            },
            RequestContext(request, {}),
            )

            
@login_required
def edit_course_profile(request, course_id):
    """
    This view allows for the editing of courses on the public site.
    Like the ``Person`` profile views, it has both admin and non-admin
    versions, so be careful with that distinction.  It also uses the 
    unit permissions and Django permissions code.  While simpler here than
    in other parts of the site (cf. ``edit_organization``), the ability to 
    edit is probably best determined with a object method written into the 
    model and not in the view code, as this makes the permissions system
    overly brittle.
    
    """
    
    course = get_object_or_404(Course, pk=int(course_id))
    
    user = getattr(request, 'user', None)
    
    if not (course.has_unit_permission(user) and user.has_perm("profiles.change_course") or user.is_staff):
        return HttpResponseForbidden("You do not have access to edit this course.")
        
    if request.method == 'POST':
        if user.is_staff:
            course_form = AdminCourseForm(request.POST, instance=course)
        else:
            course_form = CourseForm(request.POST, instance=course)
        
        if (course_form.is_valid()):
            course_form.save()
            request.user.message_set.create(message="Course profile changes were saved.")
            return HttpResponseRedirect( reverse(view_course, args=[course.id]) )
        else:
            request.user.message_set.create(message="Error.")
    else:
        if user.is_staff:
            course_form = AdminCourseForm(instance=course)
        else:
            course_form = CourseForm(instance=course)
        course
    return render_to_response('edit_course_profile.html', {
            'course': course,
            'course_form': course_form,
            },
            RequestContext(request, {}),
            )

@login_required
def edit_section_profile(request, section_id):
    """
    This view allows for the editing of sections on the public site.
    Like the ``Person`` profile views, it has both admin and non-admin
    versions, so be careful with that distinction.  It also uses the 
    unit permissions and Django permissions code.  While simpler here than
    in other parts of the site (cf. ``edit_organization``), the ability to 
    edit is probably best determined with a object method written into the 
    model and not in the view code, as this makes the permissions system
    overly brittle.  
    
    One important consideration for the editting permissions is that we
    allow assigned faculty to edit this page, as well as the usual 
    administrators.
    
    """
    
    section = get_object_or_404(Section, pk=int(section_id))
    
    user = getattr(request, 'user', None)
    
    if user is None or user.is_anonymous():
        return HttpResponseForbidden("You do not have access to edit this section.")
    
    edittable = section.has_unit_permission(user) and user.has_perm("profiles.change_section")
    edittable |= user.is_staff
    
    person = Person.objects.get(user_account = user)
    
    for instructor in section.instructors.all():
        edittable |= person.id == instructor.id
    
    if not (edittable):
        return HttpResponseForbidden("You do not have access to edit this section.")
        
    if request.method == 'POST':
        if user.is_staff:
            section_form = AdminSectionForm(request.POST, instance=section)
        else:
            section_form = SectionForm(request.POST, instance=section)
        
        if (section_form.is_valid()):
            section_form.save()
            request.user.message_set.create(message="Section changes were saved.")
            return HttpResponseRedirect( reverse(view_section, args=[section.id]) )
        else:
            request.user.message_set.create(message="Error.")
    else:
        if user.is_staff:
            section_form = AdminSectionForm(instance=section)
        else:
            section_form = SectionForm(instance=section)
    
    return render_to_response('edit_section_profile.html', {
            'section': section,
            'section_form': section_form,
            },
            RequestContext(request, {}),
            )

def download_syllabus(request, section_id):
    """
    This view generates a document based on the uploaded syllabus.
    It tries to create a name for the file that matches the university's
    guidelines for naming syllabus documents rather than defaulting to
    the user's file naming scheme.
    
    """
    
    section = get_object_or_404(Section, pk=int(section_id))
    #see http://stackoverflow.com/questions/1930983/django-download-csv-file-using-a-link
    wrapper      = FileWrapper(section.syllabus)
    content_type = mimetypes.guess_type(section.syllabus.path)[0]
    print content_type
    path,filename = os.path.split(section.syllabus.path)
    shortname,ext = os.path.splitext(filename)
    faculty_abbr_list = []
    for faculty_member in section.instructors.all():
        faculty_abbr_list.append(faculty_member.last_name.upper() + faculty_member.first_name.upper()[0])
    faculty_abbr = "_".join(faculty_abbr_list)
    
    term = section.semester.term[:1].upper()
    
    #TODO: $%$@#^%!  We don't have the section letter!   Try to guess if from the filename
    syllabus_name_components = shortname.split("_")
    if len(syllabus_name_components) >= 3 and len(syllabus_name_components[2]) == 1:
        section_letter = syllabus_name_components[2].upper()
    else:
        section_letter = "X"
    
    download_name ="%s_%s_%s_%s_%s%s%s" % (section.course.subject.abbreviation,
                                          section.course.coursenumber,
                                          section_letter, 
                                          faculty_abbr,
                                          term,
                                          str(section.semester.year)[-2:],
                                          ext)
    
    response     = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = (section.syllabus.size)    
    response['Content-Disposition'] = "attachment; filename=%s"%download_name
    return response
    

@user_passes_test(lambda u: u.is_staff)
def activate(request, person_id):
    """
    This is a deprecated method that preceded the move to LDAP authentication.
    
    """
    
    person = get_object_or_404(Person, pk=int(person_id))

    if request.method == 'POST':

        form = PersonActivateForm(request.POST)
        if form.is_valid():
            person = Person.objects.get(pk=form.cleaned_data['person_id'])
            user = User.objects.create_user( person.default_username(),
                                             form.cleaned_data['email'],
                                             person.n_number )
            person.user_account = user
            person.save()
            request.user.message_set.create(message="Person was activated with user_id=%s" % user.id)
            return HttpResponseRedirect( reverse(home) )

    else:
        form = PersonActivateForm(initial={'person_id': person.id})
            
    return render_to_response('activate.html', {
            'person': person,
            'form': form,
            },
            RequestContext(request, {}),
            )

@login_required
def add_syllabus(request, section_id):
    """
    This view allows specific users the ability to upload a syllabus
    and attach it to the ``Section`` object.
    
    """
    section = get_object_or_404(Section, pk=int(section_id))

    user = getattr(request, 'user', None)
    
    if user is None or user.is_anonymous():
        return HttpResponseForbidden("You do not have access to edit this section.")
    
    edittable = section.has_unit_permission(user) and user.has_perm("profiles.change_section")
    edittable |= user.is_staff
    
    person = Person.objects.get(user_account = user)
    
    for instructor in section.instructors.all():
        edittable |= person.id == instructor.id
    
    if not (edittable):
        return HttpResponseForbidden("You do not have access to edit this section.")
        
    if request.method == 'POST':

        form = SyllabusForm(request.POST,request.FILES,instance=section)
        if form.is_valid():
            section = form.save(commit=False)
            section.syllabus_orig_filename = '%s' % request.FILES['syllabus']
            section.save()
            
            request.user.message_set.create(message="Profile changes were saved.")

            id = request.POST.get('next',None)
            if id:
                url = reverse(edit_profile, args=[id])
            else:
                url = '/'
            return HttpResponseRedirect( url )

    else:
        form = SyllabusForm(instance=section)

    return render_to_response('add_syllabus.html', {
            'section': section,
            'form': form,
            'next': request.GET.get('next',''),
            },
            RequestContext(request, {}),
        )

def view_course(request,course_id):
    """
    This view displays the course.  It's surprisingly simple, given how much work has
    been done with courses over time.  In fact, a lot of the work of displaying the
    page appears on the template itself, for good or ill.
    
    Like other simple model views, this view could benefit from being refactored so
    that the security logic exists in the Course model itself and not in the course
    view.
    
    """
    
    course = get_object_or_404(Course, pk=int(course_id))
    
    mlt = SearchQuerySet().more_like_this(course)[:5]

    user = getattr(request, 'user', None)

    edittable = False
    if user is not None:
        edittable = course.has_unit_permission(user)
        edittable &= user.has_perm("profiles.change_course")
        edittable |= user.is_staff
    
    courseimages = course.courseimage_set.all()
    
#    for i in range(len(courseimages),4): #@UnusedVariable
#        courseimages.append(None)
#    
   
    cloud = Tag.objects.get_for_object(course)
    
    docs = CalaisDocument.objects.filter(content_type__name = "course", object_id = course.id)
    if docs.count() > 0:
        document = docs[0]
    else:
        if course.description is not None:
            document = CalaisDocument.objects.analyze(course,fields=[('title','text/txt'),('description','text/html')])
        else:
            document = CalaisDocument.objects.analyze(course,fields=[('title','text/txt')])
    
    return render_to_response('view_course.html',
                              { 'course': course,
                                'courseimages': courseimages,
                                'cloud': cloud,
                                'edittable': edittable,
                                'mlt':mlt,
                                'document': document,
                                },
                              RequestContext(request,{}),
                              )


def view_section(request,section_id):
    """
    This view displays a ``Section`` of a ``Course`` (see the model
    documentation for a complete description of the distinction between
    the two.)
    
    This view is notable as being one of the places in which the object-based
    permissions are used.  Object-based permissions are applied at the level of
    a specific object -- in this case, whether the user is allowed to read the
    syllabus of a specific instructor.
    
    As with other view, the edittable flag here would best be refactored into the
    model code itself rather than remain in the view.
    """
    
    section = get_object_or_404(Section, pk=int(section_id))
    
    user = getattr(request, 'user', None)

    edittable = False
    if user is not None:
        edittable = section.has_unit_permission(user)
        edittable &= user.has_perm("profiles.change_section")
        edittable |= user.is_staff
    
    course_edittable = False
    if user is not None:
        course_edittable = section.course.has_unit_permission(user)
        course_edittable &= user.has_perm("profiles.change_course")
    
    for faculty in section.instructors.all():
        edittable |= (request.user == faculty.user_account)
 	
    if edittable:
        can_read_syllabi = True
    elif request.user.is_authenticated():
        can_read_syllabi = True
        for faculty in section.instructors.all():
            #if one faculty member wants their syllabus hidden, it stays hidden
            can_read_syllabi &= request.user.has_object_perm(faculty.person_ptr,"read syllabi") 
            #unless no permission is set, then we assume it's open
            #TODO: Make sure this conforms to policy!!!
            can_read_syllabi |= not(
                                faculty.person_ptr.group_perms_set.filter(
                                    Q(permission = Person.perms.as_int('read syllabi'))|#@UndefinedVariable
                                    Q(permission = Person.perms.as_int(('read cv','read syllabi'))) #@UndefinedVariable
                                    ).count() > 0
                                )
    else:
        can_read_syllabi = False
    
    if section.title is None or section.title == "":
        title = section.course.title
    else:
        title = section.title
    
    return render_to_response('profiles/section.html',
                            { 'section': section,
                            'course': section.course,
                            'title': title,
                            'can_read_syllabi': can_read_syllabi,
                            'edittable': edittable,
                            'course_edittable': edittable,
                              },
                            RequestContext(request,{}),
                            )


def view_program(request,program_id):
    """
    This view is more or less a stub of pag for displaying the ``Program``
    organizational unit.  Ultimately, this should be a place where admins and other
    authorized users can go to work with program-related functions, like managing
    ``Committee`` and ``Authority`` relationships, etc.  Other org units should 
    probably get similar pages.
    
    """
    
    program = get_object_or_404(Program, pk=int(program_id))
    
    user = getattr(request, 'user', None)    
    edittable = program.has_unit_permission(user) 

    return render_to_response('view_program.html',
                              { 'program': program,
                                'edittable':edittable
                                },
                              RequestContext(request,{}),
                          )

def edit_program(request,program_id):

    program = get_object_or_404(Program, pk=int(program_id))
    
    edittable = False
    
    user = getattr(request, 'user', None)
    
    edittable = program.has_unit_permission(user) 

    # why is it necessary for a user to have both 
    # unit permission set up in the program's unit (a school/department), 
    # and the specific action permission that's in the line below? --Or
    #
    # edittable &= user.has_perm("profiles.change_program")    
    
    if not edittable:
        return HttpResponseForbidden("You do not have access to edit this group.")    

    if request.method == 'POST':
        program_form = ProgramForm(request.POST, instance=program)

        if (program_form.is_valid()):
            program_form.save()
            request.user.message_set.create(message="Program changes were saved.")
            return HttpResponseRedirect( reverse(view_program, args=[program.id]) )
        else:
            request.user.message_set.create(message="Error.")
    else:
        program_form = ProgramForm(instance=program)

    return render_to_response('edit_program.html', {
            'program': program,
            'program_form': program_form
            },
            RequestContext(request, {}),
            )
	
	

def view_areasofstudy(request, aos_id):
    
    aos = get_object_or_404(AreaOfStudy, pk=int(aos_id))

    return render_to_response('view_aos.html',
                              { 'aos': aos,
                                },
                              RequestContext(request,{}),
                              )

def view_organization(request,organization_id):
    """
    This view displays an ``Organization`` object.  See the model documentation
    for a more complete description of what an organization represents.
    
    Along with the ``Committee`` model, organizations represent one of the most
    complicated objects in terms of security.  This model should be refactored first
    as part of a general clean up to remove edittable from the view code and port
    it into the model code itself.
    
    It would also be a good idea to add an "invite" permission that could allow
    members with fewer security privileges to still invite new members.
    
    Also note the use of the ``current`` and ``past`` managers for the member
    and leader affiliations.  This is one of the benefits of using the 
    ``Affiliation`` object over a ``ManyToManyField``: we can retain historical
    information even after the connection is no longer active.  For example, 
    we can know all of the previous leaders of an organization while still allowing 
    the current ones to be the only recipients of security clearance, public display,
    etc.
    
    """
    
    organization = get_object_or_404(Organization, pk=int(organization_id))

    mlt = SearchQuerySet().more_like_this(organization)[:5]
    
    user = getattr(request, 'user', None)
    
    invitations = []
    edittable = False
    

    if user is not None and not user.is_anonymous():
        person = Person.objects.get(user_account = user)
        invitations = Invitation.objects.filter(object_id = organization_id, guest=person, accepted_at__isnull = True )
        edittable = organization.has_unit_permission(user) 
        edittable &= user.has_perm("profiles.change_organization")
        
    edittable |= user.is_staff
    
    leaders = Person.objects.filter(affiliations__organization = organization, affiliations__role__title = "leader")
    members = Person.objects.filter(affiliations__organization = organization, affiliations__role__title = "member")


    current_leaders = Affiliation.current.filter(role__title="leader",
                                                 content_type__name="organization",
                                                 object_id = organization_id)

    past_leaders = Affiliation.past.filter(role__title="leader",
                                           content_type__name="organization",
                                           object_id = organization_id)


    current_members = Affiliation.current.filter(role__title="member",
                                                 content_type__name="organization",
                                                 object_id = organization_id)

    past_members = Affiliation.past.filter(role__title="member",
                                           content_type__name="organization",
                                           object_id = organization_id)

    if user is not None and not user.is_anonymous:
        edittable = organization.has_unit_permission(user)
        edittable &= user.has_perm("profiles.change_organization")
    
    for leader in current_leaders:
        edittable |= leader.person.user_account == user

    can_invite = edittable
        
    for member in current_members:
        can_invite |= member.person.user_account == user



    return render_to_response('profiles/organization.html',
                              { 'organization': organization,
                                'leaders': leaders,
                                'members': members,
                                'invitations': invitations,
                                'current_leaders': current_leaders,
                                'past_leaders': past_leaders,
                                'current_members': current_members,
                                'past_members': past_members,
                                'edittable': edittable,
                                'can_invite': can_invite,
                                'mlt':mlt,
                                },
                              RequestContext(request,{}),
                              )

@login_required
def edit_organization(request,organization_id=None):
    """
    This view edits an ``Organization`` object.  See the model documentation
    for a more complete description of what an organization represents.
    
    Along with the ``Committee`` model, organizations represent one of the most
    complicated objects in terms of security.  This model should be refactored first
    as part of a general clean up to remove edittable from the view code and port
    it into the model code itself.
    
    Also note the use of the ``current`` and ``past`` managers for the member
    and leader affiliations.  This is one of the benefits of using the 
    ``Affiliation`` object over a ``ManyToManyField``: we can retain historical
    information even after the connection is no longer active.  For example, 
    we can know all of the previous leaders of an organization while still allowing 
    the current ones to be the only recipients of security clearance, public display,
    etc.
    
    In addition, the ``Affiliation`` managers have the ``begin`` and ``retire`` methods
    that allow connections to see easily set to current or past without having to 
    rewrite complicated code.  "Retirement" is the preferred way for disposing of a current
    affiliation.  It has the same effect as a deletion, while still retaining the 
    connections for historical and data-mining purposes.
    
    """
    
    organization = None
    content_type = ContentType.objects.get_by_natural_key("profiles", "organization")

    leaders = []
    members = []
    
    if organization_id is not None:
        organization = get_object_or_404(Organization, pk=int(organization_id))
        #members = [id[0] for id in Person.objects.filter(affiliations__organization = organization, affiliations__role__title = "member").values_list('pk')]
        members = [a['person_id'] for a in Affiliation.current.filter(role__title="member",content_type__name="organization",object_id = organization_id).values('person_id')]
        #leaders = [id[0] for id in Person.objects.filter(affiliations__organization = organization, affiliations__role__title = "leader").values_list('pk')]
        leaders = [a['person_id'] for a in Affiliation.current.filter(role__title="leader",content_type__name="organization",object_id = organization_id).values('person_id')]
        organization_form = OrganizationForm(instance=organization,
                                             initial={'members':members,
                                                      'leaders':leaders})
    else:
        organization_form = OrganizationForm()
    
    invitation_form = InvitationForm()
    
    user = getattr(request, "user", None)
    person = Person.objects.get(user_account = user)
    
    edittable = False

    if organization is not None:
        if user is not None and not user.is_anonymous():
            person = Person.objects.get(user_account = user)
            edittable = organization.has_unit_permission(user) 
            edittable &= user.has_perm("profiles.change_organization")
            
        edittable |= user.is_staff
        
        
        for leader_id in leaders:
            edittable |= leader_id == person.id
    else:
        edittable = True
        
    if not edittable:
        return HttpResponseForbidden("You do not have access to edit this group.")
        
    if request.method == 'POST':
        print request.FILES
        organization_form = OrganizationForm(request.POST, request.FILES, instance=organization)
        
        if (organization_form.is_valid()):
            print "Fields", organization_form.fields
            print
            print "Clean", organization_form.cleaned_data
            print
            print request.POST
            
            organization = organization_form.save()
            
            leader_role,created = Role.objects.get_or_create(title="leader",content_type=content_type)
            member_role,created = Role.objects.get_or_create(title="member",content_type=content_type)
            
            Affiliation.current.retire_all(role=leader_role,content_type=content_type,object_id=organization.id)
            Affiliation.current.retire_all(role=member_role,content_type=content_type,object_id=organization.id)

            for id in organization_form.cleaned_data["leaders"]:
                leader = Person.objects.get(id=id)
                affiliation,created = Affiliation.objects.get_or_create(person=leader,
                                                                        role=leader_role,
                                                                        content_type=content_type,
                                                                        object_id=organization.id)
                affiliation.begin()
                print affiliation
            
            for id in organization_form.cleaned_data["members"]:
                member = Person.objects.get(id=id)
                affiliation,created = Affiliation.objects.get_or_create(person=member,
                                                                        role=member_role,
                                                                        content_type=content_type,
                                                                        object_id=organization.id)
                affiliation.begin()
                print affiliation
                
            request.user.message_set.create(message="Group changes were saved.")
            
            invitation_form = InvitationForm(request.POST,request.FILES)
            
            if (invitation_form.is_valid() and organization is not None):
                if invitation_form.cleaned_data["invites"].find(",") >= 0:
                    invites = invitation_form.cleaned_data["invites"].split(",")
                else:
                    invites = invitation_form.cleaned_data["invites"].split()

                validate_listed_email = EmailValidator(email_re, _(u'Enter a list of valid e-mail addresses, separated by commas or spaces.'), 'invalid')
                
                for invite in invites:
                    invite = invite.strip()
                    
                    host = Person.objects.get(user_account=user)
                    
                    guest = None
                    
                    print invite
                    
                    try:
                        validate_listed_email(invite)
                    except:
                        continue
    
                    guest_email = invite
                    
                    try:
                        username,domain = guest_email.split("@")
                        if domain == settings.SCHOOL_URL:
                            guest = Person.objects.get(user_account__username=username)
                    except Person.DoesNotExist:
                        pass
                    
                    message = invitation_form.cleaned_data["message"]
                    
                    invitation, created = Invitation.objects.get_or_create(host=host, guest=guest, guest_email=guest_email, object_id=organization.id, content_type=content_type)
                    if created:
                        invitation.message=message
                        invitation.save()
                        d = DataminingEmail( to=[guest_email],
                                 from_email="%s <%s>" % (host.full_name(),host.user_account.email),
                                 subject="You've been invited to join %s on DataMYNE!" % (organization.title),
                                 body= render_to_string('profiles/email/organization_invite.txt', 
                                                        {'message': message,
                                                         'host': host,
                                                         'organization': organization,
                                                         'domain': Site.objects.get_current().domain,
                                                         'url': invitation.get_absolute_url() },
                                                         RequestContext(request,{})),
                                 )
                        d.send(fail_silently=False)

                if len(invites) > 0:
                    request.user.message_set.create(message="People were invited to the group.")

            return HttpResponseRedirect( reverse(view_organization, args=[organization.id]) )
        else:
            request.user.message_set.create(message="Error.")


    return render_to_response('profiles/edit/organization.html',
                              { 'organization': organization,
                                'organization_form': organization_form,
                                'invitation_form': invitation_form,
                                },
                              RequestContext(request,{}),
                              )

@login_required
def accept_organization_invitation(request,slug,invitation):
    """
    This view marks an invitation to an organization as accepted.
    
    Note that this should be deprecated in favor of the more general
    ``accept_organization`` view, but requires that the ``Organization``
    model have an ``accept_organization`` model built into it.
    
    """
    
    organization = invitation.content_object
    
    content_type = ContentType.objects.get_by_natural_key("profiles", "organization")
    member_role,created = Role.objects.get_or_create(title="member",content_type=content_type)
    
    current_membership,created = Affiliation.objects.get_or_create(role=member_role,content_type=content_type,person = invitation.guest, object_id = organization.id)
    
    current_membership.begin()
    
    if created:
        request.user.message_set.create(message="Welcome to %s." % (organization.title))
    else:
        request.user.message_set.create(message="Welcome back to %s." % (organization.title))
        
    if invitation.accepted_at is None:
        invitation.accepted_at = datetime.datetime.now()
        invitation.save()
    
    return view_invitation(request,slug,invitation)



@user_passes_test(lambda u: u.is_staff)
def admin(request):
    """
    Deprecated.  A new and more complete admin section needs to be created to
    handle the move from DataMYNE as a Parsons-based experiment to university-
    wide infrastrucure.
    """

    from datetime import datetime #@Reimport

    logged_in_today = FacultyMember.objects.filter(
        user_account__last_login__gte=datetime.now().date()).order_by("-user_account__last_login")
    logged_in_ever = FacultyMember.objects.filter(
        user_account__last_login__gte=datetime(2009,5,13)).order_by("-user_account__last_login")

    modified_today = FacultyMember.objects.filter(
        updated_at__gte=datetime.now().date()).order_by("-updated_at")
    modified_ever = FacultyMember.objects.filter(
        updated_at__gte=datetime(2009,5,13)).order_by("-updated_at")

    return render_to_response('admin.html', {
            "logged_in_today": logged_in_today,
            "logged_in_ever": logged_in_ever,
            "modified_today": modified_today,
            "modified_ever": modified_ever,
            },
            RequestContext(request, {}),
        )

def _raw_sql_helper(sql):
    """
    Deprecated.  All queries should use the Django ORM for the sake of
    security and API consistency.
    
    """
    from django.db import connection
    cursor = connection.cursor() #@UndefinedVariable
    cursor.execute(sql)
    return cursor.fetchall()
    
@user_passes_test(lambda u: u.is_staff)
def stats_report(request):
    """
    Deprecated.  A new admin (with stats) needs to be created.
    
    """
    
    num_profiles = FacultyMember.objects.all().count()
    num_active_faculty = FacultyMember.objects.filter(user_account__isnull=False).filter(user_account__is_active=True).distinct().count()
    num_bios = FacultyMember.objects.filter(bio__isnull=False).exclude(bio=u'').count()

    num_faculty_with_photos = FacultyMember.objects.exclude(photo=u'').distinct().count()
    num_faculty_with_tags = FacultyMember.objects.exclude(tags=u'').distinct().count()
    num_faculty_with_expertise = FacultyMember.objects.filter(expertise__isnull=False).exclude(tags=u'').distinct().count()

    num_syllabi = Section.objects.all().exclude(syllabus=u'').count()
    syllabi_leaders = _raw_sql_helper("""
select count(ps.id) c, concat(pp.first_name, pp.last_name) name
from profiles_section ps
  left join profiles_section_instructors psi on ps.id = psi.section_id
  left join profiles_person pp on psi.facultymember_id = pp.id
 where syllabus != '' group by facultymember_id 
 order by c desc
 limit 5;""")

    num_portfolio_urls = WorkURL.objects.all().count()
    num_works = Work.objects.all().count()

    num_tags = Tag.objects.all().count()
    tag_leaders = _raw_sql_helper("""
select count(t.id) c, t.name
from tagging_taggeditem tt, tagging_tag t
where tt.tag_id = t.id
group by tag_id
order by c desc
limit 5;""")

    num_selected_expertise = _raw_sql_helper("select count(*) from profiles_person_expertise;")[0][0]
    expertise_leaders = _raw_sql_helper("""
select count(pe.id) as c, pe.name
from profiles_person_expertise ppe, profiles_expertise pe
where ppe.expertise_id = pe.id 
group by expertise_id 
order by c desc
limit 5;""")

    return render_to_response('stats-report.html', {
            "num_profiles": num_profiles,
            "num_active_faculty": num_active_faculty,
            "num_bios": num_bios,

            "num_faculty_with_photos": num_faculty_with_photos,
            "num_faculty_with_tags": num_faculty_with_tags,
            "num_faculty_with_expertise": num_faculty_with_expertise,

            "num_syllabi": num_syllabi,
            "syllabi_leaders": syllabi_leaders,

            "num_portfolio_urls": num_portfolio_urls,
            "num_work_images": num_works,

            "num_tags": num_tags,
            "tag_leaders": tag_leaders,

            "num_selected_expertise": num_selected_expertise,
            "expertise_leaders": expertise_leaders,            
            },
            RequestContext(request, {}),
        )

@password_required
def api(request):
    """
    Deprecated
    ... except still used.  See ticket 165
    """
    
    import csv
    from sorl.thumbnail.main import DjangoThumbnail
    from django.db import connection

    fields = (
        ('DB_ID', 'p.id'),
        ('N_NUMBER', 'n_number'),
        ('LAST_NAME', 'p.last_name'),
        ('FIRST_NAME', 'p.first_name'),
        ('EMAIL', "IF(au.username or au.username != '',CONCAT(au.username,'@%s'),'')" % settings.SCHOOL_URL),
        ('ACADEMIC_TITLE', 'academic_title'),
        ('ADMINISTRATIVE_TITLE', 'admin_title'),
        # ('ACADEMIC_TITLE', 'academic_title'),
        # ('ADMINISTRATIVE_TITLE', 'admin_title'),
        # ('STATUS', 'status'),
        ('STATUS', 'IF(fm.status="PT","Part time", IF(fm.status="FT","Full time","") )'),
        ('BIO', 'bio'),
        ('OFFICE', 'office'),
        ('PHONE', 'phone'),
        ('EXPERTISE_AREAS', "GROUP_CONCAT(DISTINCT ex.name ORDER BY ex.name ASC SEPARATOR ',')"),
        ('SUBJECT_CODES', "GROUP_CONCAT(DISTINCT su.abbreviation ORDER BY su.abbreviation ASC SEPARATOR ',')"),
        ('SCHOOL', 'sc.fullname'),
        ('PHOTO_URL', "IF(photo or photo != '',photo,'')"), # using DjangoThumbnail below instead (hack)
        ('PORTFOLIO_URL', 'wu.url'),
        )

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=faculty.csv'

    writer = csv.writer(response)
    writer.writerow( [ f[0] for f in fields ] )

    # settings.MEDIA_URL
    
    cursor = connection.cursor() #@UndefinedVariable

    # get current year so we only output data from current + last year
    now = datetime.datetime.now()
    year = now.year
    
    sql_fields = ", ".join( [ f[1] for f in fields ] )

    custom_query = \
        """select %s
    from profiles_person p
    left join profiles_facultymember fm on p.id = fm.person_ptr_id
    left join profiles_section_instructors si on si.facultymember_id = p.id
    left join profiles_section s on s.id = si.section_id
    left join profiles_semester ps on ps.id = s.semester_id
    left join profiles_course c on c.id = s.course_id
    left join profiles_subject su on su.id = c.subject_id
    left join profiles_school sc on sc.id = fm.homeschool_id
    left join profiles_person_expertise fm_ex on fm_ex.person_id = p.id
    left join profiles_expertise ex on ex.id = fm_ex.expertise_id
    left join profiles_workurl wu on wu.person_id = p.id
    inner join auth_user au on p.user_account_id = au.id
    where au.is_active = 1 and ps.year >= year-1
    group by p.id""" % sql_fields

    cursor.execute(custom_query)
    while (True):
        faculty = cursor.fetchone()

        if faculty == None:
            break
        
        li = list(faculty)

        # replace all None's with '' ... isn't there a Python one-liner for this?  TODO -rory
        for i in range(0,len(li)):
            if li[i] is None:
                li[i] = ''

        # this is a horrible awful hack. this whole function should be re-thought out
        # probably add a "to_csv" method on the Faculty class?  TODO -rory
        if li[14] and li[14] != '':
            try:
                d = DjangoThumbnail(li[14],[240,240],['crop'])
                li[14] = unicode(d)
            except:
                li[14] = ""
        
        # the next lines handle html tags in faculty bio.
        # don't we want to make sure that data is escaped prior to insertion? TODO - or
        
        # extract href attributes from anchors in bio field
        # and append them to the anchor text
        li[8] = extractlinks(li[8])
        
        # strip html tags from bio field
        li[8] = strip_tags(li[8]) 

        # this is not handling certain characters correctly and needs
        # to be fixed
        lii = [ unicode(l).encode('cp1252','replace') for l in li ]

        writer.writerow(lii)

    return response


def extractlinks(html):
    soup = BeautifulSoup(html)
    anchors = soup.findAll('a')
    for a in anchors:
        soup.a.replaceWith(a.string + ' ["'+ a['href'] + '"] ')
    return soup


def wordpress(request, faculty_id):
    f = get_object_or_404(FacultyMember, pk=int(faculty_id))
    return render_to_response('wordpress.html', {
            "faculty": f,
            },
            RequestContext(request, {}),
        )    

def filter(request):
    """
    This view has been deprecated since the introduction of new ``Student``
    and ``Staff`` models.  A more comprehensive browse/filter view is in
    the planning stages at the time of writing.
    
    """

    areas_of_expertise = Expertise.objects.all()

    faculty_list = []
    
    selected_areas = []
    
    if request.method == 'POST':
        
        form = FilterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['filteroption'] == "or":
                faculty_list = FacultyMember.objects.filter(
                    status__in=form.cleaned_data['status']).filter(
                    expertise__in=form.cleaned_data['expertise'] ).distinct()
            
            if form.cleaned_data['filteroption'] == "and":
                f = FacultyMember.objects.filter(status__in=form.cleaned_data['status']).distinct()
                for i in form.cleaned_data['expertise']:
                    f = f.filter(expertise=i)
                faculty_list = f
            
            selected_areas = ", ".join( [ str(e.id) for e in form.cleaned_data['expertise'] ] )


        else:
            pass # (form error)
    
    else:
        form = FilterForm()
    
    return render_to_response('filter.html', {
            'form': form,
            'areas_of_expertise': areas_of_expertise,
            'selected_areas': selected_areas,
            'faculty_list': faculty_list,
            },
            RequestContext(request, {}),
        )
        
def contact(request):
    """
    A simple contact-form processor.
    """
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subj = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            recipients = []
            for i in ContactEmail.objects.filter(subject=subj).distinct():
                recipients.append(i.recipient)
            
            d = DataminingEmail( to=recipients,
                                 from_email="%s <%s>" % (name, email),
                                 subject=subj,
                                 body=message,
                                 headers = {'Reply-To': "%s <%s>" % (name, email)} )
            d.send(fail_silently=False)
            
            thankyou = 'Thank you for your comments.'
        else:
            thankyou = 'Invalid form.'
    else:
        user = getattr(request, 'user', None)
        if user.id:
            form = ContactForm(initial={'name': user, 'email': user.email})
        else:
            form = ContactForm()
        thankyou = ''

    return render_to_response('contact.html', {
            'form': form,
            'thankyou': thankyou,
            },
            RequestContext(request, {}),
        )

def view_work(request,work_id):
    """
    This view displays a ``Work`` object and its affiliated creators.
    
    """
    
    work = get_object_or_404(Work, pk=int(work_id))
    user = getattr(request, 'user', None)
    
    mlt = SearchQuerySet().more_like_this(work)[:5]

    current_creators = Affiliation.current.filter(role__title="creator",
                                                 content_type__name="work",
                                                 object_id = work.id).order_by("person__last_name","person__first_name")
    edittable = False
    if user is not None:
        edittable = work.has_unit_permission(user)
        edittable &= user.has_perm("profiles.change_work")
    
    for creator in current_creators:
        edittable |= creator.person.user_account == user

    return render_to_response('profiles/work.html',
                              { 'work': work,
                                'edittable': edittable,
                                'mlt': mlt,
                                'creators': current_creators,
                                },
                              RequestContext(request,{}),
                              )

@login_required
def edit_work(request,work_id=None):
    """
    This view edits a ``Work`` object and its affiliated creators.
    
    As with other model views, this should be refactored to move the
    security code into the model itself rather than re-writing the 
    "edittable" flag within the view code.
    
    """

    work = None
    creators = []
    content_type = ContentType.objects.get_by_natural_key("profiles", "work")
    creator_role = Role.objects.get_or_create(title="creator",content_type=content_type)[0]
    
    user = getattr(request, 'user', None)

    try:
        person = Person.objects.get(user_account = user)
    except Person.DoesNotExist:
        return HttpResponseForbidden("You must be logged in to add or edit work.")
    
    if work_id is not None:
        work = get_object_or_404(Work, pk=int(work_id))
        if work.type:
            work_type = [t['id'] for t in WorkType.objects.filter(works__id = work_id).values('id')]
        else:
            work_type = None
        creators = [a['person_id'] for a in Affiliation.current.filter(role__title="creator",content_type__name="work",object_id = work_id).values('person_id')]
    else:
        work_type = None
        creators = [person.id]
    
    if work is not None:
        edittable = False
    
        if user is not None:
            edittable = work.has_unit_permission(user)
            edittable &= user.has_perm("profiles.change_work")
        
        for creator_id in creators:
            edittable |= creator_id == person.id
    else:
        edittable = True
        
    if not edittable:
        return HttpResponseForbidden("You do not have access to edit this work.")
    
    from_profile = False

    if request.method == 'POST':
        work_form = WorkForm(request.POST, request.FILES, instance=work)

        if (work_form.is_valid()):
            work = work_form.save()
            work.type = []
            for i in work_form.cleaned_data["work_type"]:
                work.type.add(i)
            request.user.message_set.create(message="Your changes were saved.")
            
            Affiliation.current.retire_all(role=creator_role,content_type=content_type,object_id=work.id)

            for id in work_form.cleaned_data["creators"]:
                creator = Person.objects.get(id=id)
                affiliation = Affiliation.objects.get_or_create(person=creator,
                                                                role=creator_role,
                                                                content_type=content_type,
                                                                object_id=work.id)[0]
                affiliation.begin()
                affiliation.save()
            
            if request.POST.get("saveadd",None) is not None:
                return HttpResponseRedirect( reverse(edit_work) )
            elif request.POST.get("saveprofile",None) is not None:
                return HttpResponseRedirect( reverse(view_person_profile, args=[person.id]) )
            else:
                return HttpResponseRedirect( reverse(view_work, args=[work.id]) )
    else:
        work_form = WorkForm(instance=work,initial={'creators':creators,
                                                    'work_type':work_type,})

        try:
            referrer = request.META["HTTP_REFERER"]
            view,args,kwargs = resolve(urlparse(referrer)[2])
            if view == view_profile or view == view_student_profile or view == view_person_profile or view == view_staff_profile:
                from_profile = True
        except KeyError:
            pass
        except Http404:
            pass

           
    return render_to_response('profiles/edit/work.html',
                              { 'work': work,
                                'form': work_form,
                                'creators': creators,
                                'from_profile': from_profile, 
                                },
                              RequestContext(request,{}),
                              )

def delete_work(request,work_id,person_id):
    """
    This view deletes a ``Work`` object.  It is one of the few models
    that we allow to be publicly deleted.  Since this is user-contributed content,
    however, it only seems fair that we respect their wishes about the display
    and use of their own work.
    
    """
    
    content_type = ContentType.objects.get_by_natural_key("profiles", "work")
    creator_role = Role.objects.get_or_create(title="creator",content_type=content_type)[0]
    
    user = getattr(request, 'user', None)
    
    work = get_object_or_404(Work, pk=int(work_id))
    creators = [a['person_id'] for a in Affiliation.current.filter(role__title="creator",content_type__name="work",object_id = work_id).values('person_id')]
        
    if user.is_staff and person_id is not None:
        person = Person.objects.get(id = person_id)
    else:
        person = Person.objects.get(user_account = user)
        
    print person
    
    if work is not None:
        edittable = False

        if user is not None:
            edittable = work.has_unit_permission(user)
            edittable &= user.has_perm("profiles.change_work")
        
        for creator_id in creators:
            edittable |= creator_id == person.id
    else:
        edittable = True
        
    if not edittable:
        return HttpResponseForbidden("You do not have access to delete this work.")
    
    affiliations = Affiliation.current.filter(role__title="creator",content_type__name="work",object_id = work.id)
    print affiliations
    if len(affiliations) > 1:
        person_affiliations = Affiliation.current.filter(person = person,role__title="creator",content_type__name="work",object_id = work.id)
        print person_affiliations
        person_affiliations.delete()
    else:
        print "deleting work"
        work.delete()
        
    view, args, kwargs = resolve(urlparse(request.META["HTTP_REFERER"])[2])
    return HttpResponseRedirect(urlparse(request.META["HTTP_REFERER"])[2])


#@login_required
#def add_organization(request):
#    user = getattr(request, 'user', None)
#    
#    if request.method == 'POST':
#        organization_form = OrganizationForm(request.POST, request.FILES)
#        
#        if (organization_form.is_valid()):
#            neworg = organization_form.save()
#            request.user.message_set.create(message="Group created.")
#            return HttpResponseRedirect( reverse('profiles_view_organization', args=[neworg.id]) )
#        else:
#            request.user.message_set.create(message="Error.")
#    else:
#        organization_form = OrganizationForm()
#    
#    return render_to_response('add_organization.html', {
#            'organization_form': organization_form,
#            },
#            RequestContext(request, {}),
#            )
    
@login_required
def view_invitation(request,slug, invitation = None):
    """
    If the user if logged in, this view simply redirects that user to the
    appropriate view and marks the invite as received.

    """
    
    if invitation is None:
        invitation = get_object_or_404(Invitation,slug=slug)
    
    user = getattr(request, 'user', None)
    
    if invitation.received_at is None:
        invitation.received_at = datetime.datetime.now()

    if invitation.guest is None:
        guest = Person.objects.get(user_account=user)
        invitation.guest = guest
        
    invitation.save()
    return HttpResponseRedirect(invitation.content_object.get_absolute_url())
    
@login_required
def accept_invitation(request,slug):
    """
    If the user if logged in, this view simply redirects that user to the
    appropriate view and marks the invite as accepted.

    This view requires that an object that can have an accepted invitation
    possess an ``accept_invitiation`` method.

    """
    
    invitation = get_object_or_404(Invitation,slug=slug)
    
    # TODO: add more types for object that can invites, like committees, etc.
    if invitation.content_type.name == "organization":
        return accept_organization_invitation(request,slug,invitation)
    else:
        created = invitation.content_object.accept_invitation(invitation)       
        if created:
            request.user.message_set.create(message="Welcome to %s." % (invitation.content_object))
        else:
            request.user.message_set.create(message="Welcome back to %s." % (invitation.content_object))

        return view_invitation(request,slug,invitation)

@login_required
def decline_invitation(request,slug):
    """
    If the user if logged in, this view simply redirects that user back to his or
    her previous view and deletes the invitation.  The ``Invitation`` is one of the
    very few objects that get deleted in the DataMYNE system.  In the future, it
    may prove useful to only "logically" delete these, but still retain the connection
    in order to mine more data on social dynamics.

    """
    invitation = get_object_or_404(Invitation,slug=slug)
    
    request.user.message_set.create(message="You have declined an invitation to %s." % (invitation.content_object))
    
    invitation.delete()
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

#@login_required
def grant_permission(request):
    user = getattr(request, 'user', None)
    
    #if user is None or user.is_anonymous():
    #    return HttpResponseForbidden("You do not have access to edit this section.")
    
    # multi-level perm to be inserted
    #if not (user.is_staff):
    #    return HttpResponseForbidden("You do not have access to edit this section.")
    
    department_visible = False
    school_visible = False
    program_visible = False
        
    if request.method == 'POST':
        form = GrantPermissionForm(request.POST)
        
        if form.is_valid():
            
            if form.cleaned_data['division']:
                if form.cleaned_data['division'].name == 'Parsons':
                    department_visible = False
                    school_visible = True
                    if form.cleaned_data['school']:
                        program_visible = True
                    else:
                        program_visible = False
                else:
                    department_visible = True
                    school_visible = False
                    program_visible = False
            
            for u in form.cleaned_data['users']:
                person = get_object_or_404(Person, pk=int(u))
                request.user.message_set.create(message="Set permission for " + person.first_name + ' ' + person.last_name)
        else:
            request.user.message_set.create(message="Form error")
    else:
        form = GrantPermissionForm()
        
    return render_to_response('grant_permission.html', {
            'form': form,
            'department_visible': department_visible,
            'school_visible': school_visible,
            'program_visible': program_visible,
            },
            RequestContext(request, {}),
            )
