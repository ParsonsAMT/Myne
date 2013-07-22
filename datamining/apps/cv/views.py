from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import *
from django.template import RequestContext

from datamining.apps.cv.models import *
from datamining.apps.cv.forms import *

from datamining.apps.profiles.models import Person, FacultyMember, Student,\
    Staff
from datamining.apps.cv.models import CV
from datamining.apps.cv.forms import CVForm
from django.http import HttpResponseForbidden
from datamining.apps.cv.forms import DeleteCVForm

def home(request):

    return HttpResponse("ok")

@login_required
def edit(request,person_id):
    person = get_object_or_404(Person, pk=int(person_id))

    if (not request.user.is_staff) and (request.user != person.user_account):
        print request.user.is_staff
        print person.user_account
        return HttpResponseForbidden("You do not have access to edit this profile.")

    try:
        cv = person.generated_cv
    except CV.DoesNotExist: #@UndefinedVariable
        cv = None

    if request.method == 'POST':

        if cv:
            cv_form = CVForm(request.POST,instance=cv)
        else:
            cv_form = CVForm(request.POST)

        if cv_form.is_valid():
            cv = cv_form.save(commit=False)
            cv.owner = person
            cv.save()
            request.user.message_set.create(
                message="CV Saved. Continue editing or <a href='%s'>click here to return to profile</a>." % reverse(
                    'profiles.views.edit_profile',args=[person.id]
                    )
                )

    else:

        basic_info = _get_person_basic_info(person)

        if cv:
            cv_form = CVForm(instance=cv,initial={'basic_info': basic_info})
        else:
            cv_form = CVForm(initial={'basic_info': basic_info})

    return render_to_response('edit_cv.html', {
            'person': person,
            'cv_form': cv_form,
            },
            RequestContext(request, {}),
            )

@login_required
def delete(request, person_id):
    person = get_object_or_404(Person, pk=int(person_id))

    if not request.user.is_staff and request.user != person.user_account:
        return HttpResponseForbidden("You do not have access to delete this CV.")

    if request.method == 'POST':
        form = DeleteCVForm(request.POST)
        
        if form.is_valid():
            form_person_id = int(form.cleaned_data['person_id'])
            
            if int(person_id) != form_person_id:
                return HttpResponseForbidden("You do not have access to delete this CV.")
            
            try:
                cv = person.generated_cv
            except CV.DoesNotExist: #@UndefinedVariable
                cv = None
        
            if cv is not None:
                cv.delete()
                
            if person.cv.name != u'':
                person.cv.delete()
            
            try:
                return HttpResponseRedirect(reverse("profiles_edit_profile",args=[person.faculty_member.id]))
            except AttributeError:    
                try:
                    return HttpResponseRedirect(reverse("profiles_edit_student_profile",args=[person.student.id]))
                except AttributeError:    
                    try:
                        return HttpResponseRedirect(reverse("profiles_edit_staff_profile",args=[person.staff.id]))
                    except AttributeError:    
                        return HttpResponseForbidden("Invalid form.")
        else:
            return HttpResponseForbidden("Invalid form.")

    else:
        form = DeleteCVForm(initial={"person_id":person_id})
        
    return render_to_response('delete_cv.html', {
            'person': person,
            'form': form,
            },
            RequestContext(request, {}),
            )


def _get_person_basic_info(p):
    try:
        p = p.facultymember
        basic_info = "%s %s\n%s\n%s\n%s\n%s" % ( 
            p.first_name, p.last_name, p.get_academic_title_display(), p.admin_title, p.office, p.phone
            )
    except FacultyMember.DoesNotExist:
        basic_info = "%s %s" % ( 
            p.first_name, p.last_name
            )
    return basic_info

def view(request,person_id):
    person = get_object_or_404(Person, pk=int(person_id))
    cv = get_object_or_404(CV, owner=person)

    fields = [
        (cv.degrees, "Degrees Held"),
        (cv.affiliations, "Professional Affiliations"),
        (cv.clients, "Clients"),
        (cv.publications, "Publications"),
        (cv.press, "Press"),
        (cv.presentations, "Presentations / Artist Talks / Conferences / Symposiums"),
        (cv.exhibitions, "Exhibitions"),
        (cv.discography, "Discography"),
        (cv.performances, "Performances"),
        (cv.awards, "Awards and Honors"),
        (cv.screenings, "Screenings / Festivals"),
        (cv.grants, "Grants and Fellowships"),
        (cv.collections, "Collections and Commissions"),
        ]

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'filename=cv.pdf'

    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch 

    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    style = getSampleStyleSheet()
    pdf = SimpleDocTemplate(response, pagesize = letter)

    story = []

    field = str(cv.basic_info).replace("\n","<br/>")
    para = Paragraph( field, style["Normal"])
    story.append(para)
    story.append(Spacer(inch * .5, inch * .2))

    for field, title in fields:
        if field:
            field = field.replace("\n","<br/>")
            para = Paragraph( "<strong>%s</strong><br/>%s" % (title,field), style["Normal"])
            story.append(para)
            story.append(Spacer(inch * .5, inch * .1))

    pdf.build(story)

    return response
    
