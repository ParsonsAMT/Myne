# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from models import *
from forms import *

import datetime

def reader(request,id):
    segment_types = SegmentType.objects.all().order_by('name')

    document = get_object_or_404(Document,pk=id)

    if request.method == "POST":
        form = SegmentsForm(segment_types,request.POST)
        if form.is_valid():
            for segment_type in segment_types:
                data = form.cleaned_data['segment%d_area' % (segment_type.id)]
                segments = Segment.objects.filter(document=document,type=segment_type)
                if segments.count() == 0:
                    if len(data.strip()) > 0:
                        segment = Segment.objects.create(document=document,type=segment_type,contents=data,created=datetime.datetime.now())
                else:
                    segment = segments[0]
                    segment.contents = data
                    segment.save()
    else:
        form = SegmentsForm(segment_types)
        if len(document.contents.strip()) == 0:
            document.extract_contents()

    return render_to_response("pdfreader/reader.html",locals())

def success(request,id):
    document = get_object_or_404(Document,pk=id)
    return render_to_response("pdfreader/success.html",locals())
