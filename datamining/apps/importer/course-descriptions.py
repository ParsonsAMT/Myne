#!/usr/bin/python


import csv
from datetime import date

from datamining.apps.profiles.models import *

#
# script for importing course description data
#
print "starting ..."

csv_filename = 'apps/importer/Course_Desc_Worksheet_Spring_2010.csv'

dataReader = csv.DictReader(open(csv_filename,'rU'), delimiter=',', quotechar='"')

i = 0
new_subjects = 0
new_courses = 0
admin = User.objects.get(id=1)

for row in dataReader:

    print "row %s" % i

    description = unicode( row['Course Description'], 'mac-roman' ).encode('utf-8')

    if description == '':
        print "  skipping empty description." 
        continue

    # find the subject or create one
    try:
        subject_abbr = row['Subject Code']
        subject = Subject.objects.get(abbreviation=subject_abbr)
        print "  found subject"
    except Subject.DoesNotExist:
        subject = Subject(abbreviation=subject_abbr,created_by=admin)
        subject.save()
        print "  added subject: %s" % subject_abbr
        new_subjects += 1

    # find the course, using above subject, or create it
    try:
        course_number = row['Course Number']
        course = Course.objects.get(subject=subject,coursenumber=course_number)
        print "  found course"

    except Course.DoesNotExist:
        course_title = row['Title']
        course = Course( coursenumber=course_number, subject=subject,
                         title=course_title, created_by=admin)
        course.save()
        print "  added course: %s %s" % ( subject, course_number )
        new_courses += 1

    course.description = description
    course.save()
    print "  added new description"

    i = i + 1


print "done."

print "Processed %s rows" % i
print "Added %s new subjects" % ( new_subjects )
print "Added %s new courses" % ( new_courses )





