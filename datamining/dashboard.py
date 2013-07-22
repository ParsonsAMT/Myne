from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
#from admin_tools.dashboard.models import *
from admin_tools.dashboard import Dashboard,AppIndexDashboard,modules


# to activate your index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_INDEX_DASHBOARD = 'datamining.dashboard.CustomIndexDashboard'

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for datamining.
    """ 
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        self.columns = 3
        self.title = "FUN!"

        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            title=_('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                {
                    'title': _('Return to site'),
                    'url': '/',
                },
                {
                    'title': _('Change password'),
                    'url': reverse('admin:password_change'),
                },
                {
                    'title': _('Log out'),
                    'url': reverse('admin:logout')
                },
            ],
            column=3,
        ))

#        self.children.append(modules.ModelList(
#            title=_('People'),
#            models = ('profiles.models.Person','profiles.models.FacultyMember','profiles.models.Student'),
#        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            title=_('Content'),
            exclude_list=('datamining.apps.importer','datamining.apps.cv','piston','basic.inlines','django.contrib','feedjack','tagging'),
            column=1,
            css_classes=['collapse', 'open'],
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title=_('Administration'),
            include_list=('datamining.apps.importer','datamining.apps.cv','piston','basic.inlines','django.contrib','feedjack','tagging'),
            column=1,
            css_classes=['collapse', 'open'],
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            limit=5,
            column=2,
        ))

        # append a feed module
        self.children.append(modules.Feed(
            title=_('Latest DataMYNE Development'),
            feed_url='http://mining.parsons.edu/trac/timeline?ticket=on&changeset=on&milestone=on&wiki=on&max=50&daysback=90&format=rss',
            limit=5,
            column=3,
        ))

        # append another link list module for "support". 
        self.children.append(modules.LinkList(
            title=_('Support'),
            children=[
                {
                    'title': _('DataMYNE Trac'),
                    'url': 'http://mining.parsons.edu/trac/',
                    'external': True,
                },
                {
                    'title': _('File a Trac ticket'),
                    'url': 'http://mining.parsons.edu/trac/newticket',
                    'external': True,
                },
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
            ],
            column=3,
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass


# to activate your app index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'datamining.dashboard.CustomAppIndexDashboard'

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for datamining.
    """ 
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)
        self.columns = 2

        # we disable title because its redundant with the model list module
        self.title = ''

        # append a model list module
        self.children.append(modules.ModelList(
            title=self.app_title,
            include_list=self.models,
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            include_list=self.get_app_content_types(),
            column=2
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
