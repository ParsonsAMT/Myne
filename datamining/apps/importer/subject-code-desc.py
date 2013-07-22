import csv

from django.contrib.auth.models import User
from datamining.apps.profiles.models import Subject, Division

print "starting ..."

dataReader = csv.DictReader(open('apps/importer/SubjectCodeDesc.csv','rU'), delimiter=',', quotechar='"')

i = 0

for row in dataReader:
    
    user = User.objects.get(pk=1)
    
    abbr    = row['SUBJ']
    desc    = row['DESC']
    div     = row['DIVISION']
    print '%s:  %s - %s (%s)' % (i, abbr, desc, div)
    
    try:
        subject = Subject.objects.get(abbreviation = abbr)
    except Subject.DoesNotExist:
        subject = Subject.objects.create(abbreviation = abbr, created_by = user)
        
    subject.fullname = desc
    
    division = None
    if div == "Mannes College":
        division = Division.objects.get(name = "Mannes")
    elif div == "New School for Social Research":
        division = Division.objects.get(name = "New School for Social Research")
    elif div == "Jazz":
        division = Division.objects.get(name = "Jazz")
    elif div == "Lang College":
        division = Division.objects.get(name = "Lang")
    elif div == "Milano":
        division = Division.objects.get(name = "Milano")
    elif div == "New School for Public Engagement":
        division = Division.objects.get(name = "New School for Public Engagement")
    elif div == "Parsons School of Design":
        division = Division.objects.get(name = "Parsons")
    elif div == "Drama":
        division = Division.objects.get(name = "Drama")
    elif div == "University Liberal Studies":
        division = Division.objects.get(name = "University Liberal Studies")
    elif div == "Mannes Extension":
        division = Division.objects.get(name = "Mannes Extension")
    
    if division:
        subject.division = division
    
    subject.save()
    
    i = i + 1
    
print "done."
print "Processed %s rows" % i