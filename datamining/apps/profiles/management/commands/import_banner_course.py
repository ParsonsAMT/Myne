'''
Created on Apr 13, 2011

@author: Mike_Edwards
'''
from datamining import settings
'''
Created on Oct 11, 2010

@author: edwards
'''
import datetime, csv, glob
from stat import ST_MTIME
from django.core.management.base import BaseCommand
from datamining.apps.profiles.models import Course, Subject, Section,\
    FacultyMember, Semester
from django.contrib.auth.models import User
from datamining.settings import BANNER_IMPORT_PREFIX

class Command(BaseCommand):
    args = ''
    help = 'Imports course information from Banner exports'

    def handle(self, *args, **options):
        settings.BANNER_IMPORT_SCRIPT = True
        
        exports = glob.glob(BANNER_IMPORT_PREFIX + "dataMyneCourse_*.csv")
        exports.sort()
        reader = csv.reader(open(exports[-1]))
        existing = 0
        created = 0

        user = User.objects.get(pk=1)
        row = reader.next()
        
        print row

        for row in reader:
            try:
                subject = Subject.objects.get(abbreviation = row[3],created_by=user)
            except Subject.DoesNotExist:
                subject = Subject.objects.create(abbreviation = row[3],created_by=user)
            
            level = None
            
            if row[12] == "AU":
                level = "associate"
            elif row[12] == "UG":
                level = "undergraduate"
            elif row[12] == "GR":
                level = "graduate"
            elif row[12] == "NC":
                level = "non-credit"
            elif row[12] == "ND":
                level = "non-degree"
            elif row[12] == "CT":
                level = "certificate"
                
            if level is None:
                print "l",level
                print row
                raise Course.DoesNotExist        

            type = None
            
            for val,disp in Course.TYPE_CHOICES:
                if row[11].strip() == disp:
                    type = val
                    
                    
            if type is None:
                if row[11].strip() == "Laboratory":
                    type = "lab"
                else:
                    print "t",type
                    print row
                    raise Course.DoesNotExist        

            changed = False

            try:
                course = Course.objects.get(subject = subject,
                                                      coursenumber = row[4])
                if course.title != row[16]:
                    course.title = row[16]
                    changed = True
            except Course.DoesNotExist:
                course = Course.objects.create(title=row[16],
                                                      subject = subject,
                                                      coursenumber = row[4],
                                                      created_by=user)
            if course.levels is None:
                #print "change l |%s| |%s|" % (course.levels.strip(),level.strip())
                course.levels = level.strip()
                changed = True

            if course.type != type:
                print "change t"
                course.type = type
                changed = True

            if course.format is None:
                #print "change f %s %s" % (course.format,row[14].lower())
                course.format = row[14].lower()
                changed = True

            if course.minimum_credits != float(row[6]):
                course.minimum_credits = float(row[6])
                print "change mi"
                changed = True

            if row[8] != "":
                maximum_credits = float(row[8])
            else:
                maximum_credits = None                    
            if course.maximum_credits != maximum_credits:
                course.maximum_credits = maximum_credits
                print "change ma"
                changed = True

            if row[7] != "":
                credit_range_type = row[7].lower()
            else:
                credit_range_type = "no"
            if course.credit_range_type != credit_range_type:
                course.credit_range_type = credit_range_type
                print "change ra"
                changed = True
            
            if changed:
                course.scripted = True
                course.save()
                course.scripted = False
                print "Saving"

            try:
                faculty = FacultyMember.objects.get(pidm=int(row[0]))
            except FacultyMember.DoesNotExist:
                faculty = None
            year = int(row[1][:4])
            sem_code = int(row[1][4:])
            if sem_code == 30 or sem_code == 40:
                year += 1
                
            print year,sem_code,
            if sem_code == 10:
                sem = "fa"
                start = datetime.datetime(year,9,1)
                end = datetime.datetime(year,12,15)
            elif sem_code == 20:
                sem = "wi"
                start = datetime.datetime(year,12,15)
                end = datetime.datetime(year+1,1,15)
            elif sem_code == 30:
                sem = "sp"
                start = datetime.datetime(year,1,15)
                end = datetime.datetime(year,5,15)
            elif sem_code == 40:
                sem = "su"
                start = datetime.datetime(year,5,15)
                end = datetime.datetime(year,8,1)
                
            try:
                semester = Semester.objects.get(year=year,term=sem)
            except Semester.DoesNotExist:
                semester = Semester.objects.create(year=year,term=sem,start_date=start,end_date=end,created_by=user)
            
            try:
                section = Section.objects.get(course=course,crn=row[2],semester=semester)
            except Section.DoesNotExist:
                section = Section.objects.create(course=course,title=row[5],crn=row[2],semester=semester,created_by=user)
            
            if faculty is not None and faculty not in section.instructors.all():
                section.instructors.add(faculty)

            print course,section,row[2],faculty
#                 try:
#                    fm = FacultyMember.objects.get(n_number=row[1])
#                    existing += 1
#                    if fm.pidm is None:
#                        fm.pidm = int(row[0])
#                    if fm.academic_title is None:
#                        fm.academic_title = row[8]
#                    if fm.admin_title is None:
#                        fm.admin_title = row[9]
#                    if fm.status is None:
#                        fm.status = choice
#                    if fm.office is None:
#                        fm.office = row[16]
#                    if fm.homeprogram is None:
#                        fm.homeprogram = program
#                    if fm.homedepartment is None:
#                        fm.homedepartment = department
#                    if fm.homedivision is None:
#                        fm.homedivision = division
#                    fm.save()
#                    
#                except (FacultyMember.DoesNotExist):
#                    FacultyMember.objects.create(pidm=int(row[0]),
#                                                 n_number=row[1],
#                                                 first_name=row[3],
#                                                 last_name=row[2],
#                                                 academic_title=row[8],
#                                                 admin_title=row[9],
#                                                 status=choice,
#                                                 office=row[16],
#                                                 homeprogram=program,
#                                                 homedepartment=department,
#                                                 homedivision=division,
#                                                 created_by=user)
#                
#                    created += 1

        print existing, created
        settings.BANNER_IMPORT_SCRIPT = False
