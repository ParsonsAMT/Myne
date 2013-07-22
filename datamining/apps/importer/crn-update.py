import csv

from profiles.models import *

#
# script for importing faculty / course / section data
#

print "starting ..."

# Faculty_Courses_and_Percents_NEW_050610.csv

dataReader = csv.DictReader(open('importer/Faculty_Courses_and_Percents_NEW_050610.csv','rU'), delimiter=',', quotechar='"')

i = 0
new_sections = []

admin = User.objects.get(id=1)

for row in dataReader:

    n_number = row['Asgn Faculty Id']

    if n_number.startswith('FACULTY'):
        print "  encountered row with N number %s. skipping ..." % n_number
        continue

    # find faculty member or fail
    try:
        print '%s -- %s' % (i, n_number)

        faculty = FacultyMember.objects.get(n_number=n_number)

        print "  found faculty member"

    except FacultyMember.DoesNotExist:
        print "  couldn't find faculty member %s %s, %s. skipping ..." % ( row['Asgn Faculty Last Name'], row['Asgn Faculty First Name'], n_number )
        continue

    # find the semester or fail
    try:
        term_year = row['Sect Term Code']

        year = term_year[0:4]
        term_num = term_year[4:6]
        term = ''
        if term_num == '10':
            term = 'fa'
        elif term_num == '30':
            term = 'sp'
        elif term_num == '40':
            term = 'su'

        semester = Semester.objects.get(term=term,year=year)
        print "  found semester"

    except Semester.DoesNotExist:
        raise Exception, "encountered a semester that does not exist (%s)" % term_year


    # find the section by CRN and semester, or create one
    crn = row['Sect Crn']
    try:
        section = Section.objects.get(crn=crn,semester=semester)
        print "  found existing section"

    except Section.DoesNotExist:

        print "  creating new section"

        # find the subject or fail
        try:
            subject_abbr = row['Sect Subj Code']
            subject = Subject.objects.get(abbreviation=subject_abbr)
            print "  found subject"
        except Subject.DoesNotExist:
            print "  couldn't find subject. skipping ..."
            continue

        # find the course, using above subject, or fail
        try:
            course_number = row['Sect Crse Numb']
            course = Course.objects.get(coursenumber=course_number,subject=subject)
            print "  found course"
        except Course.DoesNotExist:
            print "  couldn't find course. skipping ..."
            continue

        # ok, so now we have a semester and a course,
        # make a section and link them

        section = Section(crn=crn,course=course,semester=semester,created_by=admin)
        section.save()
        print "  saved new section"
        new_sections.append("%s" % section)


    # and now that we have a section, add the faculty member to it
    print "  adding %s to section" % faculty
    section.instructors.add(faculty)

    i = i + 1

print "done."

print "Processed %s rows" % i
print "Added %s new sections" % ( len(new_sections) )



