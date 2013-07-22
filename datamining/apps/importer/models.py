from django.db.models import *
from django.contrib.auth.models import User

def notify():
    from django.core.mail import EmailMessage
    email = EmailMessage( subject='[datamyne] new import uploaded',
                          body='http://stage.mining.parsons.edu/django/admin/importer/importrecord/',
                          to=('datamine@parsons.edu','rsolomon@gmail.com',) )
    email.send()


class ImportRecord(Model):

    def get_import_filename(self,filename):
        return 'user/dataimports/%s-%s' % (self.id,filename)

    SCHEDULED = 'scheduled'
    RUNNING = 'running'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'

    STATUS_CHOICES = (
        ( SCHEDULED, SCHEDULED ),
        ( RUNNING, RUNNING ),
        ( SUCCEEDED, SUCCEEDED ),
        ( FAILED, FAILED ),
        )

    TYPE_CHOICES = (
        ( 'sections', 'Sections and Teaching Assignments' ),
        ( 'deactivations', 'Faculty Deactivations'),
        ( 'courses', 'Course Data'),
        ( 'course_master', 'Course Master'),
        )

    created_by          = ForeignKey(User,blank=True,editable=False)
    created_at          = DateTimeField(auto_now_add=True,editable=False)
    completed_at        = DateTimeField(blank=True,null=True,editable=False)

    type                = CharField(max_length=13,choices=TYPE_CHOICES)

    importfile          = FileField("Import File",upload_to=get_import_filename,blank=False)
    dbbackupfile        = CharField(max_length=255)
    user_notes          = TextField(blank=True)
    result_notes        = TextField(blank=True)

    status      = CharField(max_length=10,choices=STATUS_CHOICES)
    progress    = FloatField('Progress (%)')

    def __unicode__ (self):
        return "%s (%s)" % ( self.created_at, self.created_by)

    # see http://code.djangoproject.com/wiki/CookBookThreadlocalsAndUser
    def save (self, *args, **kwargs):
        from datamining.middleware import threadlocals

        if not self.id:

            """ set created_by from current user. """
            self.created_by = threadlocals.get_current_user()

            self.status = ImportRecord.STATUS_CHOICES[0][0]
            self.progress = 0

            notify()

        super(ImportRecord,self).save(*args,**kwargs)


        
