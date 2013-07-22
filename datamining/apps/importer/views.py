from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404, HttpResponseForbidden
from django.shortcuts import *
from django.template import RequestContext, loader

from importer.models import ImportRecord
from importer.forms import ImportRecordForm
from django.contrib.auth.decorators import login_required

def home(request):

    return render_to_response('importer/home.html',
                              { },
                              RequestContext(request, {}),
                              )

@login_required
def add_import_helper(request, type, message, title):

    if request.method == 'POST':

        request.POST['type'] = type

        form = ImportRecordForm(request.POST,request.FILES)


        if form.is_valid():

            import_record = form.save()
            request.user.message_set.create(message=message)
            return HttpResponseRedirect( '/site-admin' )

    else:
        form = ImportRecordForm()

    return render_to_response( 'importer/add_import.html',
                               { 'form': form,
                                 'title' : title,
                                 },
                               RequestContext(request, {}),
                               )


@login_required
def add_sections_import(request):

    return add_import_helper( request, 'sections',
                              'Section data was scheduled for import.',
                              'Import Sections and Teaching Assigments' )

@login_required
def add_deactivations_import(request):

    return add_import_helper( request, 'deactivations',
                              'Faculty deactivations were scheduled for import.',
                              'Import Faculty Deactivations' )

@login_required
def add_course_import(request):

    return add_import_helper( request, 'courses',
                              'Course data was scheduled for import.',
                              'Import Course Data' )

@login_required
def add_course_master_import(request):

    return add_import_helper( request, 'course_master',
                              'Course master data was scheduled for import.',
                              'Import Course Master Data' )



