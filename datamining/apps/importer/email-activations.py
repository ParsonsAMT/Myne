import csv

from profiles.models import *

print "starting ..."

dataReader = csv.DictReader(open('apps/importer/Email-addresses_060810.csv','rU'), delimiter=',', quotechar='"')

i = 0

admin = User.objects.get(id=1)

for row in dataReader:

    # find the faculty member or fail
    try:
        n_number = row['Id']

        print '%s -- %s' % (i, n_number)

        faculty = FacultyMember.objects.get(n_number=n_number)

        print "  found faculty member"

    except FacultyMember.DoesNotExist:
        print "  couldn't find faculty member. skipping"
        continue

    # activate faculty and set status
    email = row['Email']

    if email != '':
        faculty.activate(email)
        print "  activated"

    #if i >= 5:
    #raise Exception, "debugging"

    i = i + 1

print "done."
