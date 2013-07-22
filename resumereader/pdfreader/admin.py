'''
Created on Aug 28, 2009

@author: edwards
'''
from django.contrib import admin
from models import Document,SegmentType,Segment

class DocumentAdmin(admin.ModelAdmin):
    fields = ['path','created','modified']

class SegmentTypeAdmin(admin.ModelAdmin):
    pass

class SegmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Document, DocumentAdmin)
admin.site.register(SegmentType, SegmentTypeAdmin)
admin.site.register(Segment, SegmentAdmin)
