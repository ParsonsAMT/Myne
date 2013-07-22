from django.db import models
from django.conf import settings
import os
import pyPdf

class Document(models.Model):
    path = models.FilePathField(path=settings.PDF_ROOT, match="^[A-Zaz0-9].*\.pdf$", recursive=False)
    contents = models.TextField(blank=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    #user = models.ForeignKey(User)
    
    def extract_contents(self):
        pdf_file = open(self.path,'r')
        pdf_obj = pyPdf.PdfFileReader(pdf_file)
        contents = []
        for page in pdf_obj.pages:
            contents.append(page.extractText())
        self.contents = ' '.join(contents)
        self.save()

    def __unicode__(self):
        return os.path.basename(self.path)

    
class SegmentType(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name
    

class Segment(models.Model):
    document = models.ForeignKey(Document,related_name="segments")
    type = models.ForeignKey(SegmentType,related_name="segments")
    contents = models.TextField()
    created = models.DateTimeField()

    def __unicode__(self):
        return "%s: %s" % (self.document,self.type)
