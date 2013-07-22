'''
Created on Apr 7, 2011

@author: Mike_Edwards
'''
from django.forms.models import ModelForm
from datamining.apps.reporting.models import Committee, Meeting, Affiliation
from ajax_select.fields import AutoCompleteSelectField,\
    AutoCompleteSelectMultipleField
from django.forms.fields import DateField, DateTimeField, TimeField
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget,\
    AdminSplitDateTime
from datamining.apps.profiles.fields import DataMyneSplitDateTimeField
from datamining.apps.profiles.widgets import DataMyneSplitDateTimeWidget

class CommitteeForm(ModelForm):
    chairpersons = AutoCompleteSelectMultipleField('person', required=False)
    members = AutoCompleteSelectMultipleField('person', required=False)
    schools = AutoCompleteSelectMultipleField('school', required=False)
    departments = AutoCompleteSelectMultipleField('department', required=False)
    divisions = AutoCompleteSelectMultipleField('division', required=False)
    programs = AutoCompleteSelectMultipleField('program', required=False)
    class Meta:
        model = Committee
        
class MeetingForm(ModelForm):
    start_time = DataMyneSplitDateTimeField(widget=DataMyneSplitDateTimeWidget(attrs={'date_class':'vDateField','time_class':'vTimeField'}),
                                            required=True)
    end_time = DataMyneSplitDateTimeField(widget=DataMyneSplitDateTimeWidget(attrs={'date_class':'vDateField','time_class':'vTimeField'}),
                                          required=True)
    invitees = AutoCompleteSelectMultipleField('person', required=False)
    class Meta:
        model = Meeting
        exclude = ("content_type","object_id",)
        
class CommitteeAffiliationForm(ModelForm):
    committee = AutoCompleteSelectField('committee')
    class Meta:
        model = Affiliation

