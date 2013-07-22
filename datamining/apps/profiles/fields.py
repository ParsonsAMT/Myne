'''
Created on Apr 27, 2011

@author: Mike_Edwards
'''
from time import strptime, strftime
from django import forms
from django.db import models
from django.forms import fields
from datamining.apps.profiles.widgets import DataMyneSplitDateTimeWidget

class DataMyneSplitDateTimeField(fields.MultiValueField):
    """
    based on: http://copiesofcopies.org/webl/2010/04/26/a-better-datetime-widget-for-django/
    
    This field allows for split date/time form entries with ajax-powered widgets
    
    """
    widget = DataMyneSplitDateTimeWidget

    def __init__(self, *args, **kwargs):
        """
        Have to pass a list of field types to the constructor, else we
        won't get any data to our compress method.
        """
        all_fields = (
            fields.CharField(max_length=10),
            fields.CharField(max_length=8),
            )
        super(DataMyneSplitDateTimeField, self).__init__(all_fields, *args, **kwargs)

    def compress(self, data_list):
        """
        Takes the values from the MultiWidget and passes them as a
        list to this function. This function needs to compress the
        list into a single object to save.
        """
        if data_list:
            if not (data_list[0] and data_list[1]):
                raise forms.ValidationError("Field is missing data.")
            input_time = strptime(data_list[1], "%H:%M")
            datetime_string = "%s %s" % (data_list[0], strftime('%H:%M', input_time))
            print "Datetime: %s"%datetime_string
            return datetime_string
        return None