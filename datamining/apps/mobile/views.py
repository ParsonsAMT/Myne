from datamining.apps.profiles.views import _random_images
from datamining.apps.profiles.models import FacultyMember
from tagging.models import Tag
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def home(request):

    cloud = Tag.objects.cloud_for_model(FacultyMember,steps=5,min_count=6)

    images = _random_images(6)
    
    from datamining.libs.truncate import truncate
    short_names = [ (truncate(str(i[0]), 6)) for i in images ]

    return render_to_response('mobile/home.html', {
            'cloud': cloud,
            'images': images,
            'short_names': short_names,
            },
            RequestContext(request, {}),
            )
