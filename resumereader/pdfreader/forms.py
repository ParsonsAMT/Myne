'''
Created on Aug 29, 2009

@author: edwards
'''
from django import forms

class SegmentsForm(forms.Form):
    def __init__(self, segment_types, *args, **kwargs):
        super(SegmentsForm, self).__init__(*args, **kwargs)
        # now we add each question individually
        for segment_type in segment_types:
             self.fields['segment%d_area' % (segment_type.id)] = forms.CharField(label=segment_type,widget=forms.Textarea,required=False)
