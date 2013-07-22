from django.contrib import admin

from importer.models import *

class ImportRecordAdmin(admin.ModelAdmin):
    list_display = ( '__unicode__', 'status', 'progress' )
    readonly_fields = ( 'created_at','created_by','completed_at','importfile','dbbackupfile','user_notes','result_notes','status','progress', )

#register classes for admin interface
admin.site.register(ImportRecord, ImportRecordAdmin)
