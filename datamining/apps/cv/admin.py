'''
Created on Aug 8, 2010

@author: edwards
'''
from django.contrib import admin

from models import CV

class CVAdmin(admin.ModelAdmin):
    pass

admin.site.register(CV, CVAdmin)