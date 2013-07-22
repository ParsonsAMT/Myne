# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Student.bio'
        db.add_column('profiles_student', 'bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Student.homeschool'
        db.add_column('profiles_student', 'homeschool', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.School'], null=True, blank=True), keep_default=False)

        # Adding field 'Student.program'
        db.add_column('profiles_student', 'program', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Student.year'
        db.add_column('profiles_student', 'year', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True), keep_default=False)

        # Adding M2M table for field expertise on 'Student'
        db.create_table('profiles_student_expertise', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm['profiles.student'], null=False)),
            ('expertise', models.ForeignKey(orm['profiles.expertise'], null=False))
        ))
        db.create_unique('profiles_student_expertise', ['student_id', 'expertise_id'])
    
    
    def backwards(self, orm):
        
        # Deleting field 'Student.bio'
        db.delete_column('profiles_student', 'bio')

        # Deleting field 'Student.homeschool'
        db.delete_column('profiles_student', 'homeschool_id')

        # Deleting field 'Student.program'
        db.delete_column('profiles_student', 'program')

        # Deleting field 'Student.year'
        db.delete_column('profiles_student', 'year')

        # Removing M2M table for field expertise on 'Student'
        db.delete_table('profiles_student_expertise')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.contactemail': {
            'Meta': {'object_name': 'ContactEmail'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.course': {
            'Meta': {'object_name': 'Course'},
            'attributes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'coursenumber': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'credits': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learning_outcomes': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'levels': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'prerequisite': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Course']", 'null': 'True', 'blank': 'True'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['profiles.Project']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Subject']"}),
            'tags': ('tagging.fields.TagField', [], {}),
            'timeline': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.courseimage': {
            'Meta': {'object_name': 'CourseImage'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Course']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
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
            'expertise': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['profiles.Expertise']", 'null': 'True', 'blank': 'True'}),
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
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['profiles.Project']", 'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'use_which_cv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'user_account': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'person_profile'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'profiles.program': {
            'Meta': {'object_name': 'Program'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.School']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.project': {
            'Meta': {'object_name': 'Project'},
            'collaborators': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Person']", 'null': 'True', 'blank': 'True'}),
            'creator_type': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '2'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'for_course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Course']", 'null': 'True', 'blank': 'True'}),
            'format': ('tagging.fields.TagField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'participating_faculty': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.FacultyMember']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'ref_type': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '2'}),
            'scope_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'specifications': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Untitled'", 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
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
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['profiles.FacultyMember']", 'symmetrical': 'False'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['profiles.Project']", 'null': 'True', 'blank': 'True'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Semester']"}),
            'syllabus': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'syllabus_orig_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'use_as_demo': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
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
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expertise': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['profiles.Expertise']", 'null': 'True', 'blank': 'True'}),
            'homeschool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.School']", 'null': 'True', 'blank': 'True'}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'program': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'profiles.subject': {
            'Meta': {'object_name': 'Subject'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Program']", 'null': 'True', 'blank': 'True'}),
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
