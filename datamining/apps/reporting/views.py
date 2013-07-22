from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from datamining.apps.reporting.models import Committee, Affiliation, Role,\
    Meeting, Authority
from datamining.apps.profiles.models import Person, Invitation, School,\
    Organization
from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from datamining.apps.profiles.forms import InvitationForm
from datamining.apps.reporting.forms import CommitteeForm, MeetingForm
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from datamining.libs.utils import DataminingEmail
from django.core.urlresolvers import reverse
from django.core.validators import EmailValidator, email_re
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.db.models import Q
import datetime
from django.conf import settings


def view_committee(request,committee_id):
    """
    This view displays an ``Committee`` object.  See the model documentation
    for a more complete description of what an organization represents.
    
    Along with the ``Organization`` model, committees represent one of the most
    complicated objects in terms of security.  This model should be refactored first
    as part of a general clean up to remove edittable from the view code and port
    it into the model code itself.
    
    It would be good to add a "admin" role to the committees, in
    addition to the current "chairperson" and "member" roles.
    
    Also note the use of the ``current`` and ``past`` managers for the member
    and chairperson affiliations.  This is one of the benefits of using the 
    ``Affiliation`` object over a ``ManyToManyField``: we can retain historical
    information even after the connection is no longer active.  For example, 
    we can know all of the previous chairs of a committee while still allowing 
    the current ones to be the only recipients of security clearance, public display,
    etc.
    
    """
    
    committee = get_object_or_404(Committee, pk=int(committee_id))

    mlt = SearchQuerySet().more_like_this(committee)[:5]
    
    user = getattr(request, 'user', None)
    
    invitations = []
    edittable = False
    can_invite = False
    person = None
    

    if user is not None and not user.is_anonymous():
        person = Person.objects.get(user_account = user)
        invitations = Invitation.objects.filter(object_id = committee_id, guest=person, accepted_at__isnull = True )
        edittable = committee.has_unit_permission(user)
        edittable &= user.has_perm("reporting.change_committee")
        
    edittable |= user.is_staff

        
    current_chairpersons = Affiliation.current.filter(role__title="chairperson",
                                                 content_type__name="committee",
                                                 object_id = committee_id)

    past_chairpersons = Affiliation.past.filter(role__title="chairperson",
                                           content_type__name="committee",
                                           object_id = committee_id)


    current_members = Affiliation.current.filter(role__title="member",
                                                 content_type__name="committee",
                                                 object_id = committee_id)

    past_members = Affiliation.past.filter(role__title="member",
                                           content_type__name="committee",
                                           object_id = committee_id)

    for chair in current_chairpersons:
        edittable |= chair.person == person
        can_invite |= edittable

    return render_to_response('reporting/committee.html',
                              { 'committee': committee,
                                'invitations': invitations,
                                'current_chairpersons': current_chairpersons,
                                'past_chairpersons': past_chairpersons,
                                'current_members': current_members,
                                'past_members': past_members,
                                'edittable': edittable,
                                'mlt':mlt,
                                },
                              RequestContext(request,{}),
                              )

@login_required
def edit_committee(request,committee_id=None):
    """
    This view edits a ``Committee`` object.  See the model documentation
    for a more complete description of what an organization represents.
    
    Along with the ``Organization`` model, committees represent one of the most
    complicated objects in terms of security.  This model should be refactored first
    as part of a general clean up to remove edittable from the view code and port
    it into the model code itself.
    
    Also note the use of the ``current`` and ``past`` managers for the member
    and chairperson affiliations.  This is one of the benefits of using the 
    ``Affiliation`` object over a ``ManyToManyField``: we can retain historical
    information even after the connection is no longer active.  For example, 
    we can know all of the previous chairs of a committee while still allowing 
    the current ones to be the only recipients of security clearance, public display,
    etc.
    
    In addition, the ``Affiliation`` managers have the ``begin`` and ``retire`` methods
    that allow connections to see easily set to current or past without having to 
    rewrite complicated code.  "Retirement" is the preferred way for disposing of a current
    affiliation.  It has the same effect as a deletion, while still retaining the 
    connections for historical and data-mining purposes.
    
    """
    
    committee = None
    content_type = ContentType.objects.get_by_natural_key("reporting", "committee")
    
    if committee_id is not None:
        committee = get_object_or_404(Committee, pk=int(committee_id))
    
    user = getattr(request, "user", None)
    

    if committee is None:
        if not user.has_perm("reporting.add_committee"):
            return HttpResponseForbidden("You do not have access to add a committee.")
        
        committee_form = CommitteeForm()
    else:
        edittable = committee.has_unit_permission(user)
        edittable &= user.has_perm("reporting.change_committee")
        
        edittable |= user.is_staff

        members = [a['person_id'] for a in Affiliation.current.filter(role__title="member",content_type__name="committee",object_id = committee_id).values('person_id')]
        chairpersons = [a['person_id'] for a in Affiliation.current.filter(role__title="chairperson",content_type__name="committee",object_id = committee_id).values('person_id')]

        if user is not None and not user.is_anonymous():
            person = Person.objects.get(user_account = user)

            for chair in chairpersons:
                edittable |= chair == person.id

        if not (edittable):
            return HttpResponseForbidden("You do not have access to edit this committee.")
        
        committee_form = CommitteeForm(instance=committee,
                                             initial={'members':members,
                                                      'chairpersons':chairpersons})
    invitation_form = InvitationForm()
        
    
    if request.method == 'POST':
        committee_form = CommitteeForm(request.POST, request.FILES, instance=committee)
        
        if (committee_form.is_valid()):
            committee = committee_form.save()
            
            chairperson_role,created = Role.objects.get_or_create(title="chairperson",content_type=content_type)
            member_role,created = Role.objects.get_or_create(title="member",content_type=content_type)
            
            Affiliation.current.retire_all(role=chairperson_role,content_type=content_type,object_id=committee.id)
            Affiliation.current.retire_all(role=member_role,content_type=content_type,object_id=committee.id)

            for id in committee_form.cleaned_data["chairpersons"]:
                chairperson = Person.objects.get(id=id)
                affiliation,created = Affiliation.objects.get_or_create(person=chairperson,
                                                                        role=chairperson_role,
                                                                        content_type=content_type,
                                                                        object_id=committee.id)
                affiliation.begin()
                print affiliation
            
            for id in committee_form.cleaned_data["members"]:
                member = Person.objects.get(id=id)
                affiliation,created = Affiliation.objects.get_or_create(person=member,
                                                                        role=member_role,
                                                                        content_type=content_type,
                                                                        object_id=committee.id)
                affiliation.begin()
                print affiliation
                
            request.user.message_set.create(message="Committee changes were saved.")
            
            invitation_form = InvitationForm(request.POST)
            
            if (invitation_form.is_valid() and committee is not None):
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
                    
                    validate_listed_email(invite)
    
                    guest_email = invite
                    
                    try:
                        username,domain = guest_email.split("@")
                        if domain == settings.SCHOOL_URL:
                            guest = Person.objects.get(user_account__username=username)
                    except Person.DoesNotExist:
                        pass
                    
                    message = invitation_form.cleaned_data["message"]
                    
                    invitation, created = Invitation.objects.get_or_create(host=host, guest=guest, guest_email=guest_email, object_id=committee.id, content_type=content_type)
                    if created:
                        invitation.message=message
                        invitation.save()
                        d = DataminingEmail( to=[guest_email],
                                 from_email="%s <%s>" % (host.full_name(),host.user_account.email),
                                 subject="You've been invited to join the %s on DataMYNE!" % (committee.title),
                                 body= render_to_string('reporting/email/committee_invite.txt', 
                                                        {'message': message,
                                                         'host': host,
                                                         'committee': committee,
                                                         'domain': Site.objects.get_current().domain,
                                                         'url': invitation.get_absolute_url() },
                                                         RequestContext(request,{})),
                                                         )
                        d.send(fail_silently=False)

                if len(invites) > 0:
                    request.user.message_set.create(message="People were invited to the committee.")

            return HttpResponseRedirect( reverse(view_committee, args=[committee.id]) )
        else:
            request.user.message_set.create(message="Error.")
    
    return render_to_response('reporting/edit/committee.html',
                              { 'committee': committee,
                                'committee_form': committee_form,
                                'invitation_form': invitation_form,
                                },
                              RequestContext(request,{}),
                              )

def view_meeting(request,meeting_id):
    """
    This view displays a meeting.  
    
    Note that meetings, currently, can be attached to any object, specifically the
    ``Organization`` and ``Committee`` objects.  This creates a rather complex security
    situation, in that the ``Meeting`` mode is not only capable of having permissions 
    assigned to it directly but, logically, is also subject to the admin permissions for
    the ``Organization`` and ``Committee``.  As with other models, this should be 
    refactored, to as great an extent as possible, into the models themselves.
    
    """
    
    meeting = get_object_or_404(Meeting, pk=int(meeting_id))

    mlt = SearchQuerySet().more_like_this(meeting)[:5]
    
    user = getattr(request, 'user', None)
    
    invitations = []
    edittable = False
    can_invite = False
    can_view_invitees = False

    person = None
    
    if user is not None and not user.is_anonymous():
        person = Person.objects.get(user_account = user)
        invitations = Invitation.objects.filter(object_id = meeting_id, guest=person, accepted_at__isnull = True )
        edittable = meeting.has_unit_permission(user)
        edittable &= (user.has_perm("reporting.change_committee")|user.has_perm("reporting.change_organization"))
        
    edittable |= user.is_staff

        
    current_leaders = Affiliation.current.filter((Q(role__title="chairperson")|Q(role__title="leader"))&
                                                 Q(content_type=meeting.content_type)&
                                                 Q(object_id = meeting.object_id))


    current_invitees = Affiliation.current.filter(role__title="invitee",
                                                 content_type__name="meeting",
                                                 object_id = meeting_id)


    for leader in current_leaders:
        edittable |= leader.person == person
        can_invite |= edittable

    for invitee in current_invitees:
        can_view_invitees |= invitee.person == person
        can_view_invitees |= edittable

    return render_to_response('reporting/meeting.html',
                              { 'meeting': meeting,
                                'duration': (meeting.end_time - meeting.start_time).seconds/60,
                                'invitations': invitations,
                                'current_leaders': current_leaders,
                                'current_invitees': current_invitees,
                                'edittable': edittable,
                                'can_invite': can_invite,
                                'can_view_invitees': can_view_invitees,
                                'mlt':mlt,
                                },
                              RequestContext(request,{}),
                              )

@login_required
def edit_meeting(request,meeting_id=None,model_name=None,object_id=None):
    """
    This view edits a meeting.  
    
    Note that meetings, currently, can be attached to any object, specifically the
    ``Organization`` and ``Committee`` objects.  This creates a rather complex security
    situation, in that the ``Meeting`` mode is not only capable of having permissions 
    assigned to it directly but, logically, is also subject to the admin permissions for
    the ``Organization`` and ``Committee``.  As with other models, this should be 
    refactored, to as great an extent as possible, into the models themselves.
    
    """
    
    meeting = None
    content_type = ContentType.objects.get_by_natural_key("reporting", "meeting")
    
    if meeting_id is not None:
        meeting = get_object_or_404(Meeting, pk=int(meeting_id))
    
    user = getattr(request, "user", None)
    
    meeting_object = None
    invitees = []

    if meeting is None:
        if model_name is None or object_id is None:
            raise Http404
        if model_name == "organization":
            meeting_object = get_object_or_404(Organization, pk=int(object_id))
        if model_name == "committee":
            meeting_object = get_object_or_404(Committee, pk=int(object_id))

        edittable = meeting_object.has_unit_permission(user) and user.has_perm("reporting.add_meeting")
        edittable |= meeting_object.has_unit_permission(user) and user.has_perm("reporting.change_committee") and model_name == "committee"
        edittable |= meeting_object.has_unit_permission(user) and user.has_perm("reporting.change_organization") and model_name == "organization"
        
        edittable |= user.is_staff

        leaders = Affiliation.current.filter((Q(role__title="chairperson")|Q(role__title="leader"))&
                                                     Q(content_type__name=model_name)&
                                                     Q(object_id = meeting_object.id))
    
        if user is not None and not user.is_anonymous():
            person = Person.objects.get(user_account = user)

            for leader in leaders:
                edittable |= leader.person == person

        if not (edittable):
            return HttpResponseForbidden("You do not have access to add a meeting for this %s." % (model_name))
        
        meeting_form = MeetingForm()
    else:
        edittable = meeting.has_unit_permission(user) and user.has_perm("reporting.change_meeting")
        edittable |= meeting.content_object.has_unit_permission(user) and user.has_perm("reporting.change_committee") and meeting.content_type.name == "committee"
        edittable |= meeting.content_object.has_unit_permission(user) and user.has_perm("reporting.change_organization") and meeting.content_type.name == "organization"
        
        edittable |= user.is_staff

        leaders = Affiliation.current.filter((Q(role__title="chairperson")|Q(role__title="leader"))&
                                                     Q(content_type=meeting.content_type)&
                                                     Q(object_id = meeting.object_id))
    
    
        invitees = Person.objects.filter(affiliations__role__title="invitee",
                                                     affiliations__content_type__name="meeting",
                                                     affiliations__object_id = meeting_id)

        if user is not None and not user.is_anonymous():
            person = Person.objects.get(user_account = user)

            for leader in leaders:
                edittable |= leader.person == person

        if not (edittable):
            return HttpResponseForbidden("You do not have access to edit this meeting.")
        
        meeting_form = MeetingForm(instance=meeting,
                                             initial={'invitees':invitees})
    invitation_form = InvitationForm()
        
    
    if request.method == 'POST':
        meeting_form = MeetingForm(request.POST, request.FILES, instance=meeting)
        
        if (meeting_form.is_valid()):
            meeting = meeting_form.save(commit=False)
            if meeting.content_object is None:
                meeting.content_object = meeting_object
            meeting.save()
            
            invitee_role,created = Role.objects.get_or_create(title="invitee",content_type=content_type)
            
            Affiliation.current.retire_all(role=invitee_role,content_type=content_type,object_id=meeting.id)
            
            for id in meeting_form.cleaned_data["invitees"]:
                invitee = Person.objects.get(id=id)
                affiliation,created = Affiliation.objects.get_or_create(person=invitee,
                                                                        role=invitee_role,
                                                                        content_type=content_type,
                                                                        object_id=meeting.id)
                affiliation.begin()
                print affiliation
                
            request.user.message_set.create(message="Meeting changes were saved.")
            
            invitation_form = InvitationForm(request.POST)
            
            if (invitation_form.is_valid() and meeting is not None):
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
                    
                    validate_listed_email(invite)
    
                    guest_email = invite
                    
                    try:
                        username,domain = guest_email.split("@")
                        if domain == settings.SCHOOL_URL:
                            guest = Person.objects.get(user_account__username=username)
                    except Person.DoesNotExist:
                        pass
                    
                    message = invitation_form.cleaned_data["message"]
                    
                    invitation, created = Invitation.objects.get_or_create(host=host, guest=guest, guest_email=guest_email, object_id=meeting.id, content_type=content_type)
                    if created:
                        invitation.message=message
                        invitation.save()
                        d = DataminingEmail( to=[guest_email],
                                 from_email="%s <%s>" % (host.full_name(),host.user_account.email),
                                 subject="You've been invited to join the %s on DataMYNE!" % (meeting),
                                 body= render_to_string('reporting/email/meeting_invite.txt', 
                                                        {'message': message,
                                                         'host': host,
                                                         'meeting': meeting,
                                                         'domain': Site.objects.get_current().domain,
                                                         'url': invitation.get_absolute_url() },
                                                         RequestContext(request,{})),
                                                         )
                        d.send(fail_silently=False)

                if len(invites) > 0:
                    request.user.message_set.create(message="People were invited to the meeting.")

            return HttpResponseRedirect( reverse(view_meeting, args=[meeting.id]) )
        else:
            request.user.message_set.create(message="Error.")
    
    return render_to_response('reporting/edit/meeting.html',
                              { 'meeting': meeting,
                                'model_name': model_name,
                                'object_id': object_id,
                                'meeting_form': meeting_form,
                                'invitation_form': invitation_form,
                                'invitees': invitees,
                                },
                              RequestContext(request,{}),
                              )

    
def list_committees_by_school(request):
    """
    This view lists all of the committees of all the schools.
    
    """
    
    authorities = Authority.objects.all().order_by("school__fullname")
    schools = School.objects.all().order_by("fullname")
    
    return render_to_response('reporting/list/committees_by_school.html',
                              { 'authorities': authorities,
                               'schools': schools,
                                },
                              RequestContext(request,{}),
                              )
    