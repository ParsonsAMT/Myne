# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):
    
    def forwards(self, orm):
        if not db.dry_run:
            for student in orm.Student.objects.all():
                if student.program == "Fashion Studies":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Studies MA")
                elif student.program == "MA Fashion Studies":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Studies MA")
                elif student.program == "Fashion Studies MA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Studies MA")
                elif student.program == "History of Decorative Arts and Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "History of Decorative Arts and Design MA")
                elif student.program == "MA History of Decorative Arts and Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "History of Decorative Arts and Design MA")
                elif student.program == "History of Decorative Arts and Design MA":
                    student.homeprogram = orm.Program.objects.get(fullname = "History of Decorative Arts and Design MA")
                elif student.program == "Communication Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Communication Design BFA")
                elif student.program == "BFA Communication Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Communication Design BFA")
                elif student.program == "BFACD":
                    student.homeprogram = orm.Program.objects.get(fullname = "Communication Design BFA")
                elif student.program == "Communication Design BFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Communication Design BFA")
                elif student.program == "Design and Technology":
                    student.homeprogram = orm.Program.objects.get(fullname = "Design and Technology BFA")
                elif student.program == "BFA Design and Technology":
                    student.homeprogram = orm.Program.objects.get(fullname = "Design and Technology BFA")
                elif student.program == "BFADT":
                    student.homeprogram = orm.Program.objects.get(fullname = "Design and Technology BFA")
                elif student.program == "Design and Technology BFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Design and Technology BFA")
                elif student.program == "MFA Design and Technology":
                    student.homeprogram = orm.Program.objects.get(fullname = "Design and Technology MFA")
                elif student.program == "MFADT":
                    student.homeprogram = orm.Program.objects.get(fullname = "Design and Technology MFA")
                elif student.program == "Design and Technology MFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Design and Technology MFA")
                elif student.program == "Fine Arts":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fine Arts BFA")
                elif student.program == "BFA Fine Arts":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fine Arts BFA")
                elif student.program == "Fine Arts BFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fine Arts BFA")
                elif student.program == "MFA Fine Arts":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fine Arts MFA")
                elif student.program == "Fine Arts MFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fine Arts MFA")
                elif student.program == "Graphic Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Graphic Design AAS")
                elif student.program == "AAS Graphic Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Graphic Design AAS")
                elif student.program == "Graphic Design AAS":
                    student.homeprogram = orm.Program.objects.get(fullname = "Graphic Design AAS")
                elif student.program == "Illustration":
                    student.homeprogram = orm.Program.objects.get(fullname = "Illustration BFA")
                elif student.program == "BFA Illustration":
                    student.homeprogram = orm.Program.objects.get(fullname = "Illustration BFA")
                elif student.program == "Illustration BFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Illustration BFA")
                elif student.program == "Photography":
                    student.homeprogram = orm.Program.objects.get(fullname = "Photography BFA")
                elif student.program == "BFA Photography":
                    student.homeprogram = orm.Program.objects.get(fullname = "Photography BFA")
                elif student.program == "Photography BFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Photography BFA")
                elif student.program == "MFA Photography":
                    student.homeprogram = orm.Program.objects.get(fullname = "Photography MFA")
                elif student.program == "Photography MFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Photography MFA")
                elif student.program == "Architectural Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Architectural Design BFA")
                elif student.program == "BFA Architectural Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Architectural Design BFA")
                elif student.program == "Architectural Design BFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Architectural Design BFA")
                elif student.program == "MArch Architectural Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Architectural Design MArch")
                elif student.program == "Architectural Design MArch":
                    student.homeprogram = orm.Program.objects.get(fullname = "Architectural Design MArch")
                elif student.program == "AAS Interior Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Interior Design AAS")
                elif student.program == "AASID":
                    student.homeprogram = orm.Program.objects.get(fullname = "Interior Design AAS")
                elif student.program == "Interior Design AAS":
                    student.homeprogram = orm.Program.objects.get(fullname = "Interior Design AAS")
                elif student.program == "Interior Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Interior Design BFA")
                elif student.program == "BFA Interior Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Interior Design BFA")
                elif student.program == "BFAID":
                    student.homeprogram = orm.Program.objects.get(fullname = "Interior Design BFA")
                elif student.program == "Interior Design BFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Interior Design BFA")
                elif student.program == "MFA Interior Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Interior Design MFA")
                elif student.program == "MFAID":
                    student.homeprogram = orm.Program.objects.get(fullname = "Interior Design MFA")
                elif student.program == "Interior Design MFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Interior Design MFA")
                elif student.program == "Lighting Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Lighting Design MFA")
                elif student.program == "MFA Lighting Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Lighting Design MFA")
                elif student.program == "Lighting Design MFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Lighting Design MFA")
                elif student.program == "Product Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Product Design BFA")
                elif student.program == "BFA Product Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Product Design BFA")
                elif student.program == "Product Design BFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Product Design BFA")
                elif student.program == "Design and Management":
                    student.homeprogram = orm.Program.objects.get(fullname = "Design and Management BFA")
                elif student.program == "BFA Design and Management":
                    student.homeprogram = orm.Program.objects.get(fullname = "Design and Management BFA")
                elif student.program == "Design and Management BFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Design and Management BFA")
                elif student.program == "Environmental Studies":
                    student.homeprogram = orm.Program.objects.get(fullname = "Environmental Studies BS")
                elif student.program == "BS Environmental Studies":
                    student.homeprogram = orm.Program.objects.get(fullname = "Environmental Studies BS")
                elif student.program == "Environmental Studies BS":
                    student.homeprogram = orm.Program.objects.get(fullname = "Environmental Studies BS")
                elif student.program == "Integrated Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Integrated Design BFA")
                elif student.program == "BFA Integrated Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Integrated Design BFA")
                elif student.program == "Integrated Design BFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Integrated Design BFA")
                elif student.program == "Transdisciplinary Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Transdisciplinary Design MFA")
                elif student.program == "MFA Transdisciplinary Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Transdisciplinary Design MFA")
                elif student.program == "Transdisciplinary Design MFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Transdisciplinary Design MFA")
                elif student.program == "Urban Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Urban Design BS")
                elif student.program == "BS Urban Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Urban Design BS")
                elif student.program == "Urban Design BS":
                    student.homeprogram = orm.Program.objects.get(fullname = "Urban Design BS")
                elif student.program == "AAS Fashion Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Design AAS")
                elif student.program == "AASFD":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Design AAS")
                elif student.program == "Fashion Design AAS":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Design AAS")
                elif student.program == "Fashion Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Design BFA")
                elif student.program == "BFA Fashion Design":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Design BFA")
                elif student.program == "BFAFD":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Design BFA")
                elif student.program == "Fashion Design BFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Design BFA")
                elif student.program == "Fashion Design and Society":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Design and Society MFA")
                elif student.program == "MFA Fashion Design and Society":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Design and Society MFA")
                elif student.program == "MFAFD":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Design and Society MFA")
                elif student.program == "Fashion Design and Society MFA":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Design and Society MFA")
                elif student.program == "Fashion Marketing":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Marketing AAS")
                elif student.program == "AAS Fashion Marketing":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Marketing AAS")
                elif student.program == "Fashion Marketing AAS":
                    student.homeprogram = orm.Program.objects.get(fullname = "Fashion Marketing AAS")
                else:
                    student.homeprogram = orm.Program.objects.get(fullname = "Please select your program")
                student.save()
    
    def backwards(self, orm):
        if not db.dry_run:
            for student in orm.Student.objects.all():
                student.homeprogram = None
                
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
        'feedjack.feed': {
            'Meta': {'object_name': 'Feed'},
            'etag': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'feed_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
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
        'profiles.areaofstudy': {
            'Meta': {'object_name': 'AreaOfStudy'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'areas_of_study'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['profiles.Course']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'archived_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'attributes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'coursenumber': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'credit_range_type': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '2'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
        'profiles.courseimage': {
            'Meta': {'object_name': 'CourseImage'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Course']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
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
            'Meta': {'object_name': 'FacultyMember', '_ormbases': ['profiles.Person']},
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
        'profiles.invitation': {
            'Meta': {'object_name': 'Invitation'},
            'accepted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'guest': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invitations_received'", 'null': 'True', 'to': "orm['profiles.Person']"}),
            'guest_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitations_sent'", 'to': "orm['profiles.Person']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'received_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.link': {
            'Meta': {'object_name': 'Link'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'profiles.organization': {
            'Meta': {'object_name': 'Organization'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'org_courses'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['profiles.Course']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'projects': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'org_projects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['profiles.Project']"}),
            'tags': ('tagging.fields.TagField', [], {'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organizations'", 'to': "orm['profiles.OrganizationType']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'profiles.organizationtype': {
            'Meta': {'object_name': 'OrganizationType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.person': {
            'Meta': {'object_name': 'Person'},
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
        'profiles.requirement': {
            'Meta': {'object_name': 'Requirement'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'fulfils_requirements'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['profiles.Course']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requirements'", 'to': "orm['profiles.Program']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
            'credits': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'crn': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '4'}),
            'feeds': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['feedjack.Feed']", 'null': 'True', 'blank': 'True'}),
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
        'profiles.sponsorship': {
            'Meta': {'unique_together': "(('organization', 'content_type', 'object_id'),)", 'object_name': 'Sponsorship'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sponsorships'", 'to': "orm['profiles.Organization']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'profiles.staff': {
            'Meta': {'object_name': 'Staff', '_ormbases': ['profiles.Person']},
            'admin_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'division': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Division']", 'null': 'True', 'blank': 'True'}),
            'job_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'office_location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pidm': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'profiles.student': {
            'Meta': {'object_name': 'Student', '_ormbases': ['profiles.Person']},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'homeprogram': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Program']", 'null': 'True', 'blank': 'True'}),
            'homeschool': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.School']", 'null': 'True', 'blank': 'True'}),
            'person_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['profiles.Person']", 'unique': 'True', 'primary_key': 'True'}),
            'program': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '2'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
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
        'profiles.unitpermission': {
            'Meta': {'unique_together': "(('user', 'content_type', 'object_id'),)", 'object_name': 'UnitPermission'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unit_permissions'", 'to': "orm['auth.User']"})
        },
        'profiles.work': {
            'Meta': {'object_name': 'Work'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'max_length': '2000'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'work'", 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
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
    
    complete_apps = ['profiles']
