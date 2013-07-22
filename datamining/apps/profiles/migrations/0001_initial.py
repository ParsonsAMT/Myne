# encoding: utf-8 #


import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Division'
        db.create_table('profiles_division', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('profiles', ['Division'])

        # Adding model 'School'
        db.create_table('profiles_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('division', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Division'], null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['School'])

        # Adding model 'Department'
        db.create_table('profiles_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.School'], null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['Department'])

        # Adding model 'Subject'
        db.create_table('profiles_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Department'], null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['Subject'])

        # Adding model 'Expertise'
        db.create_table('profiles_expertise', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('profiles', ['Expertise'])

        # Adding model 'Person'
        db.create_table('profiles_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('n_number', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('user_account', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='person_profile', unique=True, null=True, to=orm['auth.User'])),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('cv', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('use_which_cv', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
        ))
        db.send_create_signal('profiles', ['Person'])

        # Adding model 'WorkURL'
        db.create_table('profiles_workurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Person'], null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['WorkURL'])

        # Adding model 'WorkImage'
        db.create_table('profiles_workimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Person'])),
        ))
        db.send_create_signal('profiles', ['WorkImage'])

        # Adding model 'FacultyMember'
        db.create_table('profiles_facultymember', (
            ('person_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['profiles.Person'], unique=True, primary_key=True)),
            ('academic_title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('admin_title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('homeschool', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.School'], null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['FacultyMember'])

        # Adding M2M table for field expertise on 'FacultyMember'
        db.create_table('profiles_facultymember_expertise', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('facultymember', models.ForeignKey(orm['profiles.facultymember'], null=False)),
            ('expertise', models.ForeignKey(orm['profiles.expertise'], null=False))
        ))
        db.create_unique('profiles_facultymember_expertise', ['facultymember_id', 'expertise_id'])

        # Adding model 'Student'
        db.create_table('profiles_student', (
            ('person_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['profiles.Person'], unique=True, primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('profiles', ['Student'])

        # Adding model 'Semester'
        db.create_table('profiles_semester', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('profiles', ['Semester'])

        # Adding model 'Course'
        db.create_table('profiles_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('coursenumber', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Subject'])),
        ))
        db.send_create_signal('profiles', ['Course'])

        # Adding model 'Section'
        db.create_table('profiles_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Course'])),
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.Semester'])),
            ('syllabus', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('syllabus_orig_filename', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('crn', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=4)),
        ))
        db.send_create_signal('profiles', ['Section'])

        # Adding M2M table for field instructors on 'Section'
        db.create_table('profiles_section_instructors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('section', models.ForeignKey(orm['profiles.section'], null=False)),
            ('facultymember', models.ForeignKey(orm['profiles.facultymember'], null=False))
        ))
        db.create_unique('profiles_section_instructors', ['section_id', 'facultymember_id'])


    def backwards(self, orm):
        
        # Deleting model 'Division'
        db.delete_table('profiles_division')

        # Deleting model 'School'
        db.delete_table('profiles_school')

        # Deleting model 'Department'
        db.delete_table('profiles_department')

        # Deleting model 'Subject'
        db.delete_table('profiles_subject')

        # Deleting model 'Expertise'
        db.delete_table('profiles_expertise')

        # Deleting model 'Person'
        db.delete_table('profiles_person')

        # Deleting model 'WorkURL'
        db.delete_table('profiles_workurl')

        # Deleting model 'WorkImage'
        db.delete_table('profiles_workimage')

        # Deleting model 'FacultyMember'
        db.delete_table('profiles_facultymember')

        # Removing M2M table for field expertise on 'FacultyMember'
        db.delete_table('profiles_facultymember_expertise')

        # Deleting model 'Student'
        db.delete_table('profiles_student')

        # Deleting model 'Semester'
        db.delete_table('profiles_semester')

        # Deleting model 'Course'
        db.delete_table('profiles_course')

        # Deleting model 'Section'
        db.delete_table('profiles_section')

        # Removing M2M table for field instructors on 'Section'
        db.delete_table('profiles_section_instructors')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.course': {
            'Meta': {'object_name': 'Course'},
            'coursenumber': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Subject']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.department': {
            'Meta': {'object_name': 'Department'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.School']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.division': {
            'Meta': {'object_name': 'Division'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.expertise': {
            'Meta': {'object_name': 'Expertise'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.facultymember': {
            'Meta': {'object_name': 'FacultyMember', '_ormbases': ['profiles.Person']},
            'academic_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'admin_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expertise': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['profiles.Expertise']", 'null': 'True', 'blank': 'True'}),
            'homeschool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.School']", 'null': 'True', 'blank': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'profiles.person': {
            'Meta': {'object_name': 'Person'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'cv': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'n_number': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'use_which_cv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'user_account': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'person_profile'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'profiles.school': {
            'Meta': {'object_name': 'School'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'division': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Division']", 'null': 'True', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.section': {
            'Meta': {'object_name': 'Section'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Course']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'crn': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['profiles.FacultyMember']"}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Semester']"}),
            'syllabus': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'syllabus_orig_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.semester': {
            'Meta': {'object_name': 'Semester'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'profiles.student': {
            'Meta': {'object_name': 'Student', '_ormbases': ['profiles.Person']},
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'profiles.subject': {
            'Meta': {'object_name': 'Subject'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Department']", 'null': 'True', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.workimage': {
            'Meta': {'object_name': 'WorkImage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Person']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'profiles.workurl': {
            'Meta': {'object_name': 'WorkURL'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Person']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['profiles']
