from django.forms import *

from importer.models import ImportRecord

class ImportRecordForm(ModelForm):
    class Meta:
        model = ImportRecord
        fields = ( 'importfile', 'user_notes', 'type')

    type = CharField(max_length=13,widget=HiddenInput)
