# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CV'
        db.create_table('cv_cv', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('owner', self.gf('django.db.models.fields.related.OneToOneField')(related_name='generated_cv', unique=True, null=True, to=orm['profiles.Person'])),
            ('basic_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('degrees', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('affiliations', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('clients', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('publications', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('press', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('presentations', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('exhibitions', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('discography', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('performances', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('awards', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('screenings', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('grants', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('collections', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('cv', ['CV'])


    def backwards(self, orm):
        
        # Deleting model 'CV'
        db.delete_table('cv_cv')


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
        'cv.cv': {
            'Meta': {'object_name': 'CV'},
            'affiliations': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'awards': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'basic_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'clients': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'collections': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'degrees': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'discography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'exhibitions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'grants': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'generated_cv'", 'unique': 'True', 'null': 'True', 'to': "orm['profiles.Person']"}),
            'performances': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'presentations': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'press': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'publications': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'screenings': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['cv']
