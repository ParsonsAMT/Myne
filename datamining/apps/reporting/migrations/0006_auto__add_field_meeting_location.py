# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Meeting.location'
        db.add_column('reporting_meeting', 'location', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Meeting.location'
        db.delete_column('reporting_meeting', 'location')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'feedjack.feed': {
            'Meta': {'ordering': "('name', 'feed_url')", 'object_name': 'Feed'},
            'etag': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'feed_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tagline': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'objectpermissions.grouppermission': {
            'Meta': {'object_name': 'GroupPermission'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'permission': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'objectpermissions.userpermission': {
            'Meta': {'object_name': 'UserPermission'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'permission': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'profiles.course': {
            'Meta': {'object_name': 'Course'},
            'archived_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'attributes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'coursenumber': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'credit_range_type': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '2'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'learning_outcomes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'levels': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'maximum_credits': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'minimum_credits': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'prerequisites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'dependents'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['profiles.Course']"}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['profiles.Project']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Subject']"}),
            'tags': ('tagging.fields.TagField', [], {'max_length': '2000'}),
            'taken': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['profiles.Student']", 'null': 'True', 'blank': 'True'}),
            'timeline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.department': {
            'Meta': {'object_name': 'Department'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'division': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Division']", 'null': 'True', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'FacultyMember', '_ormbases': ['profiles.Person']},
            'academic_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'admin_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'homedepartment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Department']", 'null': 'True', 'blank': 'True'}),
            'homedivision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Division']", 'null': 'True', 'blank': 'True'}),
            'homeprogram': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Program']", 'null': 'True', 'blank': 'True'}),
            'homeschool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.School']", 'null': 'True', 'blank': 'True'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'pidm': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'profiles.person': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Person'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'cv': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'expertise': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['profiles.Expertise']", 'null': 'True', 'blank': 'True'}),
            'feeds': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['feedjack.Feed']", 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'n_number': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['profiles.Project']", 'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'max_length': '2000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'use_which_cv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'user_account': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'person_profile'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'profiles.program': {
            'Meta': {'object_name': 'Program'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Department']", 'null': 'True', 'blank': 'True'}),
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
            'format': ('tagging.fields.TagField', [], {'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'participating_faculty': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.FacultyMember']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'ref_type': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '2'}),
            'scope_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'specifications': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'max_length': '2000'}),
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
        'profiles.student': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Student', '_ormbases': ['profiles.Person']},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'homeschool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.School']", 'null': 'True', 'blank': 'True'}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'program': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '2'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'profiles.subject': {
            'Meta': {'ordering': "['abbreviation']", 'object_name': 'Subject'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Program']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.unitpermission': {
            'Meta': {'unique_together': "(('user', 'content_type', 'object_id'),)", 'object_name': 'UnitPermission'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unit_permissions'", 'to': "orm['auth.User']"})
        },
        'reporting.affiliation': {
            'Meta': {'unique_together': "(('person', 'content_type', 'object_id', 'role'),)", 'object_name': 'Affiliation'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'affiliations'", 'to': "orm['profiles.Person']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'affiliations'", 'null': 'True', 'to': "orm['reporting.Role']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'reporting.authority': {
            'Meta': {'unique_together': "(('committee', 'content_type', 'object_id'),)", 'object_name': 'Authority'},
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authorities'", 'to': "orm['reporting.Committee']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'reporting.committee': {
            'Meta': {'object_name': 'Committee'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mandate': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subcommittees'", 'null': 'True', 'to': "orm['reporting.Committee']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'reporting.meeting': {
            'Meta': {'unique_together': "(('content_type', 'object_id'),)", 'object_name': 'Meeting'},
            'agenda': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'minutes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'reporting.role': {
            'Meta': {'object_name': 'Role'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roles'", 'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['reporting']
