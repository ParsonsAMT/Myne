from datamining.apps.profiles.models import Person, FacultyMember, Project, \
    Course, Student, Organization, Staff
from basic.blog.models import Post
from django.http import get_host
from django.conf import settings


def template_settings(request):
    user = getattr(request, 'user', None)
    if user is not None and user.is_authenticated():
        try:
            current_person = Person.objects.get(user_account=user)
        except Person.DoesNotExist:  #@UndefinedVariable
            current_person = {}
    else:
        current_person = {}


    return {'stage_name': settings.STAGE_NAME,
            'is_secure': request.is_secure(),
            'secure_login': settings.SECURE_LOGIN,
            'host': get_host(request),
            'subdir_prefix': settings.SUBDIR_PREFIX,
            'current_person': current_person}


def recent_updates(request):
    """

    :param request:
    :return: :rtype:
    """
    recently_updated = {'facultymember': FacultyMember.actives.order_by("-updated_at")[:5],
                        'project': Project.objects.all().order_by("-updated_at")[:5],
                        'course': Course.objects.all().order_by("-updated_at")[:5],
                        'student': Student.objects.all().order_by("-updated_at")[:5],
                        'organization': Organization.objects.all().order_by("-updated_at")[:5],
                        'staff': Staff.objects.all().order_by("-updated_at")[:5],
                        'posts': Post.objects.all().order_by("-created")[:5]}

    return {'recently_updated': recently_updated}


def school_url(request):
    """

    :param request:
    :return: SCHOOL_URL :rtype: dict
    """
    return {'SCHOOL_URL' : settings.SCHOOL_URL}