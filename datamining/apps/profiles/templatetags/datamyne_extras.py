from truncate import truncate       
from django.template.defaultfilters import stringfilter
from django.template import resolve_variable
from django.contrib.auth.models import Group
from django import template 

register = template.Library()

@register.filter
@stringfilter
def dmtruncate(value, length=1):
    return truncate(value,length=length)

#from http://djangosnippets.org/snippets/1259/
@register.filter
@stringfilter
def truncatesmart(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.
    
    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """
    
    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value
    
    # Make sure it's unicode
    value = unicode(value)
    
    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value
    
    # Cut the string
    value = value[:limit]
    
    # Break into words and remove the last
    words = value.split(' ')[:-1]
    
    # Join the words and return
    return ' '.join(words) + '...'

#from http://djangosnippets.org/snippets/282/    
@register.tag()
def ifusergroup(parser, token):
    """ Check to see if the currently logged in user belongs to a specific
    group. Requires the Django authentication contrib app and middleware.

    Usage: {% ifusergroup Admins %} ... {% endifusergroup %}

    """
    try:
        tag, group = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Tag 'ifusergroup' requires 1 argument.")
    nodelist = parser.parse(('endifusergroup',))
    parser.delete_first_token()
    return GroupCheckNode(group, nodelist)


class GroupCheckNode(template.Node):
    def __init__(self, group, nodelist):
        self.group = group
        self.nodelist = nodelist
    def render(self, context):
        user = resolve_variable('user', context)
        if not user.is_authenticated:
            return ''
        try:
            group = Group.objects.get(name=self.group)
        except Group.DoesNotExist:
            return ''
        if group in user.groups.all():
            return self.nodelist.render(context)
        return ''   