'''
Created on Apr 27, 2011

@author: Mike_Edwards
'''
from django import forms
from django.db import models
from django.template.loader import render_to_string
from django.forms.widgets import Select, MultiWidget, DateInput, TextInput,\
    TimeInput
from time import strftime
from django.contrib.auth.models import User

def _remove_password():
    
    users = User.objects.all()
    
    for u in users:
        u.set_unusable_password()
        u.save()

class DataMyneSplitDateTimeWidget(MultiWidget):
    """
    based on: http://copiesofcopies.org/webl/2010/04/26/a-better-datetime-widget-for-django/
    """

    def __init__(self, attrs=None, date_format=None, time_format=None):
        date_class = attrs['date_class']
        time_class = attrs['time_class']
        del attrs['date_class']
        del attrs['time_class']

        time_attrs = attrs.copy()
        time_attrs['class'] = time_class
        date_attrs = attrs.copy()
        date_attrs['class'] = date_class

        widgets = (DateInput(attrs=date_attrs, format=date_format),
                   TimeInput(attrs=time_attrs),
                   )

        super(DataMyneSplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            d = strftime("%Y-%m-%d", value.timetuple())
            t = strftime("%H:%M", value.timetuple())
            return (d, t)
        else:
            return (None, None)

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        return "Date: %s<br/>Time: %s" % (rendered_widgets[0], rendered_widgets[1])

    class Media:
        css = (
            "js/jquery-ui-timepicker.css",
            )
        js = (
            "js/jquery.ui.timepicker.js",
            )