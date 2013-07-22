#!/usr/bin/python


#####
# bootstrapping:
#####
import sys, os

# this should be the location of directory containing settings file:
project_path = os.path.split( os.path.split( os.path.split( __file__ )[0] )[0] )[0]

# include the project directory and its parent:
sys.path.append( project_path )
sys.path.append( os.path.split( project_path )[0] )

os.environ['DJANGO_SETTINGS_MODULE'] = 'datamining.settings'

#####
# ok, now we have access to all the Django stuff
#####

from django import conf
import csv
import re
from datetime import datetime
from datamining.apps.importer.models import *
from datamining.apps.profiles.models import *


# does a little setup and then dispatches procesing to appropriate
# function
def process_job(import_job):

    import_job.result_notes = "starting ...\n"

    csv_filename = conf.settings.MEDIA_ROOT + ( '/%s' % import_job.importfile )

    # determine total lines of file (for progress)
    for i, l in enumerate( open(csv_filename,'rU') ):
        pass
    total_lines = i + 1.0

    # 'importer/Faculty_Courses_and_Percents_NEW_050610.csv'
    data_reader = csv.DictReader(open(csv_filename,'rU'), delimiter=',', quotechar='"')

    if import_job.type == 'sections':
        process_sections(import_job,total_lines,data_reader)
    elif import_job.type == 'deactivations':
        process_deactivations(import_job,total_lines,data_reader)
    elif import_job.type == 'courses':
        process_courses(import_job,total_lines,data_reader)
    elif import_job.type == 'course_master':
        process_course_master(import_job,total_lines,data_reader)
    else:
        #TODO: add a condition for the course master function below
        import_job.result_notes = "Invalid import type specified"
        import_job.status = ImportRecord.FAILED
        import_job.save()


def process_sections(import_job,total_lines,data_reader):

    i = 0
    new_faculty = 0
    new_subjects = 0
    new_courses = 0
    changed_courses = 0
    new_sections = 0

    admin = User.objects.get(id=1)

    for row in data_reader:

        result_msg = ''

        n_number = row['Asgn Faculty Id']

        faculty = None

        if not n_number.startswith('N00'):
            result_msg += "  encountered row with N number %s. skipping ...\n" % n_number
        else:
            # find faculty member, or create one
            try:
                result_msg += '%s -- %s\n' % (i, n_number)
    
                faculty = FacultyMember.objects.get(n_number=n_number)
    
                result_msg += "  found faculty member\n"
    
            except FacultyMember.DoesNotExist:
                if row.has_key('Email'):
                    first_name = row['Asgn Faculty First Name']
                    last_name = row['Asgn Faculty Last Name']
        
                    if row['Fctg Desc'] == 'Full-Time Faculty':
                        status = 'FT'
                    elif row['Fctg Desc'] == 'Part-Time Faculty':
                        status = 'PT'
                    else:
                        status = ''
        
                    faculty = FacultyMember(n_number=n_number,status=status,
                                            first_name=first_name,last_name=last_name,
                                            created_by=import_job.created_by)
                    faculty.save()
                    faculty.activate(row['Email'])
                    result_msg += "  added faculty member: %s %s, %s\n" % ( first_name, last_name, n_number )
                    new_faculty += 1


        # find the semester or fail
        try:
            term_year = row['Sect Term Code']

            year = int(term_year[0:4])
            term_num = term_year[4:6]
            term = ''
            if term_num == '10':
                term = 'fa'
            elif term_num == '30':
                term = 'sp'
                year += 1
            elif term_num == '40':
                term = 'su'
                year += 1

            semester = Semester.objects.get(term=term,year=year)
            result_msg += "  found semester\n"

        except Semester.DoesNotExist:
            raise Exception, "encountered a semester that does not exist (%s)" % term_year


        # find the section by CRN and semester, or create one
        crn = row['Sect Crn']
        try:
            section = Section.objects.get(crn=crn,semester=semester)
            result_msg += "  found existing section\n"

        except Section.DoesNotExist:

            result_msg += "  creating new section\n"

            # find the subject or create one
            try:
                if 'Subj Code' in row:
                    subject_abbr = row['Subj Code']
                elif 'Sect Subj Code' in row:
                    subject_abbr = row['Sect Subj Code']
                subject = Subject.objects.get(abbreviation=subject_abbr)
                result_msg += "  found subject\n"
            except Subject.DoesNotExist:
                subject = Subject(abbreviation=subject_abbr,created_by=import_job.created_by)
                subject.save()
                result_msg += "  added subject: %s\n" % subject_abbr
                new_subjects += 1

            try:
                course_title = row['Title'].strip()
                if 'Crse Number' in row:
                    course_number = row['Crse Number']
                elif 'Sect Crse Numb' in row:
                    course_number = row['Sect Crse Numb']
                course = Course.objects.get(coursenumber=course_number,subject=subject,is_archived=False)
                result_msg += "  found course\n"
                # if the course title changes, we assume a new course has been created
                        
            except Course.DoesNotExist:
                course = Course.objects.create( coursenumber=course_number,subject=subject,title=course_title,
                                 created_by=import_job.created_by,created_at = datetime.now())
                result_msg += "  added course: %s %s\n" % ( subject, course_number )
                new_courses += 1
            
            if 'Section Credit Hours' in row:
                credit_text = row['Section Credit Hours']
                credit_data = credit_text.split(' ')[:-1]
                if len(credit_data) == 1:
                    course.minimum_credits = credit_data[0]
                elif len(credit_data) == 3:
                    course.minimum_credits = credit_data[0]
                    course.maximum_credits = credit_data[2]
                    if credit_data[1] == "TO":
                        course.credit_range_type = "to"
                    elif credit_data[1] == "OR":
                        course.credit_range_type = "or"

            if 'Section Credit Hours' in row:
                code = row['Sect Schd Code']
    
                if code == 'A':
                    course.type = 'admin'
                elif code == 'B':
                    course.type = 'lab'
                elif code == 'C':
                    course.type = 'discussion'
                elif code == 'I':
                    course.type = 'independent'
                elif code == 'L':
                    course.type = 'lecture'
                elif code == 'N':
                    course.type = 'internextern'
                elif code == 'R':
                    course.type = 'seminar'
                elif code == 'S':
                    course.type = 'studio'
                elif code == 'W':
                    course.type = 'workshop'
    
            course.title = row['Title']
            if course.created_at is None:
                course.created_at = datetime.now()
            course.save()

            # ok, so now we have a semester and a course,
            # make a section and link them

            section = Section(crn=crn,course=course,semester=semester,created_by=admin)
            section.save()
            result_msg += "  saved new section\n"
            new_sections += 1
    

        # and now that we have a section, add the faculty member to it
        if faculty is not None:
            result_msg += "  adding %s to section\n" % faculty
            section.instructors.add(faculty)

        i = i + 1

        import_job.progress = '%.2f' % (100.0 * i / total_lines)
        # @todo import_job.result_notes += result_msg NOTE: this was causing max_packet_size error. need to fix. -rory
        import_job.save()


    msg = "done.\n"

    msg += "Processed %s rows\n" % i
    msg += "Added %s new faculty\n" % ( new_faculty )
    msg += "Added %s new subjects\n" % ( new_subjects )
    msg += "Added %s new courses\n" % ( new_courses )
    msg += "Added %s new sections\n" % ( new_sections )

    import_job.result_notes += msg
    import_job.save()


# @todo this has not been sufficiently tested yet. -rory
def process_deactivations(import_job,total_lines,data_reader):

    i = 0

    for row in data_reader:

        result_msg = ''

        n_number = row['Id']

        faculty = None

        if n_number.startswith('N00'):

            # find faculty member, or fail
            try:
                result_msg += '%s -- %s\n' % (i, n_number)

                faculty = FacultyMember.objects.get(n_number=n_number)

                result_msg += "  found faculty member\n"

            except FacultyMember.DoesNotExist:
                pass

        if faculty is None:
            result_msg += "  encountered invalid N number %s. skipping ...\n" % n_number
            continue

        # now that we have a faculty member, deactivate
        faculty.deactivate()
        result_msg += "  deactivated\n"

        i = i + 1

        import_job.progress = '%.2f' % (100.0 * i / total_lines)
        # @todo import_job.result_notes += result_msg NOTE: this was causing max_packet_size error. need to fix. -rory
        import_job.save()


    msg = "done.\n"

    msg += "Processed %s rows\n" % i
    msg += "Added %s new faculty\n" % ( new_faculty )
    msg += "Added %s new subjects\n" % ( new_subjects )
    msg += "Added %s new courses\n" % ( new_courses )
    msg += "Added %s new sections\n" % ( new_sections )

    import_job.result_notes += msg
    import_job.save()


def process_courses(import_job,total_lines,data_reader):

    i = 0
    new_subjects = 0
    new_courses = 0
    admin = User.objects.get(id=1)

    for row in data_reader:

        desc_data = row['Course Description']
        if desc_data == '':
            # @todo we were getting reports with multiple lines for one course. redundant lines had
            # empty descriptions. so we can skip those. in the future, need to ensure we are getting
            # one row per course. -rory
            continue

        description = unicode( desc_data, 'mac-roman' ).encode('utf-8')

        prerequisites = []
        try:
            prereq_data = row['Prerequisite']
            prereq_iter = re.finditer('([A-Z][A-Z][A-Z][A-Z]) ([0-9][0-9][0-9][0-9])',prereq_data)

            for p in prereq_iter:
                # find the subject or fail
                try:
                    s = Subject.objects.get(abbreviation=p.group(1))
                except Subject.DoesNotExist:
                    continue

                # find the course or fail
                try:
                    c = Course.objects.get(subject=s,coursenumber=p.group(2))
                except Course.DoesNotExist:
                    continue

                # add the course to the list of prerequisites
                prerequisites.append(c)

        except KeyError, e:
            print "  no prerequisites specified in file"

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

        # add prereqs
        if len(prerequisites) > 0:
            course.prerequisites.add( *prerequisites )
            print "  added prerequisites"

        course.description = description
        print "  added new description"

        # @todo decide what to do with credits. The data import files
        # we've received have characters and credit ranges. options:
        # - convert field from Integer to Char and just accept whatever we get
        # - ensure we get proper Integer values in import files
        try:
            credit_text = row['Section Credit Hours']
            credit_data = credit_text.split(' ')[:-1]
            if len(credit_data) == 1:
                course.minimum_credits = credit_data[0]
            elif len(credit_data) == 3:
                course.minimum_credits = credit_data[0]
                course.maximum_credits = credit_data[2]
                if credit_data[1] == "TO":
                    course.credit_range_type = "to"
                elif credit_data[1] == "OR":
                    course.credit_range_type = "or"
        except KeyError, e:
            pass

        course.save()

        import_job.progress = '%.2f' % (100.0 * i / total_lines)
        import_job.save()

    i = i + 1


def process_course_master(import_job,total_lines,data_reader):
    #TODO: this is an incomplete first pass at building an importer for the course master that resembles the section import
    i = 0
    new_subjects = 0
    new_courses = 0
    
    admin = User.objects.get(id=1)

    for row in data_reader:

        result_msg = ''

                # find the semester or fail
        print "semesters"
        try:
            term_year = row['Sect Term Code']

            year = int(term_year[0:4])
            term_num = term_year[4:6]
            term = ''
            if term_num == '10':
                term = 'fa'
            elif term_num == '30':
                term = 'sp'
                year += 1
            elif term_num == '40':
                term = 'su'
                year += 1

            semester = Semester.objects.get(term=term,year=year)
            result_msg += "  found semester\n"

        except Semester.DoesNotExist:
            raise Exception, "encountered a semester that does not exist (%s)" % term_year

        print "subjects"
        try:
            subject_abbr = row['Subj Code']
            subject = Subject.objects.get(abbreviation=subject_abbr)
            result_msg += "  found subject\n"
        except Subject.DoesNotExist:
            subject = Subject(abbreviation=subject_abbr,created_by=import_job.created_by)
            subject.save()
            result_msg += "  added subject: %s\n" % subject_abbr
            new_subjects += 1

        new_courses = 0
        changed_courses = 0

        print "courses"
        try:
            course_title = row['Title'].strip()
            course_number = row['Crse Number']
            course = Course.objects.get(coursenumber=course_number,subject=subject,is_archived=False)
            result_msg += "  found course\n"
            # if the course title changes, we assume a new course has been created
            if course.title.strip() != course_title:
                changed_courses += 1
                
                #all of the sections for semesters that ended before now will be title and stay with the old course
                for section in course.section_set.filter(semester__end_date__lt = datetime.now()):
                    if section.title != "":
                        section.title = course.title
                        section.save()
                
                #archive the old course
                course.is_archived = True
                print course.created_at
                if course.created_at is None:
                    course.created_at = datetime.now()
                course.archived_at = datetime.now()
                course.save()
                
                #make a new course with the minimum info we can get from the old one
                course = Course.objects.create( coursenumber=course_number,subject=subject,title=course_title,
                             created_by=import_job.created_by,created_at = datetime.now())
                
                print course.created_at
                #for any sections that end in the future, assign them to the new course
                for section in course.section_set.filter(semester__end_date__gte = datetime.now()):
                    if section.title != "":
                        section.title = course.title
                    section.course = course
                    section.save()
                    
        except Course.DoesNotExist:
            course = Course.objects.create( coursenumber=course_number,subject=subject,title=course_title,
                             created_by=import_job.created_by,created_at = datetime.now())
            print course.created_at
            result_msg += "  added course: %s %s\n" % ( subject, course_number )
            new_courses += 1

        credit_text = row['Section Credit Hours']
        credit_data = credit_text.split(' ')[:-1]
        if len(credit_data) == 1:
            course.minimum_credits = credit_data[0]
        elif len(credit_data) == 1:
            course.minimum_credits = credit_data[0]
            course.maximum_credits = credit_data[2]
            if credit_data[1] == "TO":
                course.credit_range_type = "to"
            elif credit_data[1] == "OR":
                course.credit_range_type = "or"

        code = row['Sect Schd Code']

        if code == 'A':
            course.type = 'admin'
        elif code == 'B':
            course.type = 'lab'
        elif code == 'C':
            course.type = 'discussion'
        elif code == 'I':
            course.type = 'independent'
        elif code == 'L':
            course.type = 'lecture'
        elif code == 'N':
            course.type = 'internextern'
        elif code == 'R':
            course.type = 'seminar'
        elif code == 'S':
            course.type = 'studio'
        elif code == 'W':
            course.type = 'workshop'

        course.title = row['Title']
        if course.created_at is None:
            course.created_at = datetime.now()
        course.save()

        i = i + 1

        msg = "in progress...\n"
    
        msg += "Processed %s rows\n" % i
        msg += "Added %s new subjects\n" % ( new_subjects )
        msg += "Added %s new courses\n" % ( new_courses )
        msg += "Changed %s existing courses\n" % ( changed_courses )

        import_job.result_notes = msg
        import_job.progress = '%.2f' % (100.0 * i / total_lines)
        #TODO: import_job.result_notes += result_msg NOTE: this was causing max_packet_size error. need to fix. -rory
        import_job.save()


    msg = "done.\n"

    msg += "Processed %s rows\n" % i
    msg += "Added %s new subjects\n" % ( new_subjects )
    msg += "Added %s new courses\n" % ( new_courses )
    msg += "Changed %s existing courses\n" % ( changed_courses )

    import_job.result_notes += msg
    import_job.save()


# determine if there are any imports currently running
num_running = ImportRecord.objects.filter(status=ImportRecord.RUNNING).count()
if num_running > 0:
    print "%s : found a running import. exiting." % datetime.now().isoformat()

    sys.exit()

# if not, determine if there are any imports scheduled
num_scheduled = ImportRecord.objects.filter(status=ImportRecord.SCHEDULED).count()

if num_scheduled == 0:

    print "%s : no scheduled import jobs. exiting." % datetime.now().isoformat()
    sys.exit()

else:

    # if so, grab the oldest
    import_job = ImportRecord.objects.filter(status=ImportRecord.SCHEDULED).order_by('created_at')[0]

    import_job.status = ImportRecord.RUNNING # result_notes = "starting at %s ...\n" % date.today().isoformat()
    import_job.progress = 0
    import_job.save()

    # to run:
    # 1. do a mysqldump, gzip it, save it somewhere, store the filename in the import record
    # 2. run the import script
    #    - (which will update progress as percentage)
    # 3. try/except the entire thing so we can mark job as failed in the event of any error
    # 4. if succeeds mark job as completed
    # 5. either way, save all output / notes

    try:
        d = datetime.now()
        dump_filename = conf.settings.DB_BACKUP_DIR + ( '/datamining.db.%s.sql.gz' % d.isoformat() )

        import subprocess
        p1 = subprocess.Popen( [ conf.settings.MYSQLDUMP_CMD,
                                 '-u', conf.settings.DATABASE_USER,
                                 '-p%s' % conf.settings.DATABASE_PASSWORD,
                                 conf.settings.DATABASE_NAME ], stdout=subprocess.PIPE )
        f = open(dump_filename,'w')
        p2 = subprocess.Popen([ conf.settings.GZIP_CMD,'--stdout' ], stdin=p1.stdout, stdout=f )
        p2.communicate()[0]

        import_job.dbbackupfile = dump_filename
        import_job.save()


        # now start the actual import process:

        process_job(import_job)
        import_job.status = ImportRecord.SUCCEEDED

    except Exception, e:
        import_job.result_notes += "\ncaught exception: %s\n" % e
        import_job.status = ImportRecord.FAILED

    import_job.save()

    print "%s : cron job ran to completion. exiting." % datetime.now().isoformat()
    sys.exit()
