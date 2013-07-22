from django.forms import ModelForm,Form
from datamining.apps.cv.models import CV
from django.forms.fields import IntegerField
from django.forms.widgets import HiddenInput


class CVForm (ModelForm):
    class Meta:
        model = CV

class DeleteCVForm(Form):
    person_id = IntegerField(required=True,widget=HiddenInput())
      
