'''
Created on Oct 11, 2010

@author: edwards
'''
import datetime, csv, glob
from stat import ST_MTIME
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.db.models.aggregates import Count
from datamining.apps.profiles.models import FacultyMember, Division, Program,\
    Department, Staff, Person
from django.contrib.auth.models import User
from datamining.settings import BANNER_IMPORT_PREFIX, BANNER_IMPORT_SCRIPT
from datamining import settings

class Command(BaseCommand):
    args = ''
    help = 'Imports faculty information from Banner exports'

    def handle(self, *args, **options):
        settings.BANNER_IMPORT_SCRIPT = True
        exports = glob.glob(BANNER_IMPORT_PREFIX + "dataMyneFaculty_*.csv")
        exports.sort()
        reader = csv.reader(open(exports[-1]))
        existing = 0
        created = 0
        s_existing = 0
        s_created = 0
        user = User.objects.get(pk=1)
        reader.next()

        try:
            division = Division.objects.get(name="Mannis")
            division.name = "Mannes"
            division.created_at = datetime.datetime.now()
            division.save()
        except Division.DoesNotExist:
            pass

        try:
            program = Program.objects.get(fullname="Fine Art")
            program.fullname = "Fine Arts"
            program.created_at = datetime.datetime.now()
            program.save()
        except Program.DoesNotExist:
            pass

        for row in reader:
            division_name = row[13].strip()
            department_name = row[14].split(";")[0].strip()
            
            division = None

            if division_name == "New School for Design":
                division = Division.objects.get(name="Parsons")
            elif division_name == "New School for Jazz":
                division = Division.objects.get(name="Jazz")
            elif division_name == "New School for Drama":
                division = Division.objects.get(name="Drama")
            elif division_name == "New School for Liberal Arts":
                division = Division.objects.get(name="Lang")
            elif division_name == "New School for Music":
                division = Division.objects.get(name="Mannes")
            elif division_name == "New School for Mgt and Urb Pol":
                division = Division.objects.get(name="Milano")
            elif division_name != "" and division_name != "Undeclared":
                try:
                    division = Division.objects.get(name=division_name)
                except (Division.DoesNotExist):
                    division = Division.objects.create(name=division_name,created_by=user)
                if division.created_at is None:
                    division.created_at = datetime.datetime.now()
                    division.save()


            program = None
            department = None
            school = None

            if department_name != "" and department_name != "Undeclared":
                if division_name.find("New School for Design") >= 0:
                    try:
                        programs = Program.objects.filter(fullname__istartswith=department_name)
                        if programs.count() > 0:
                            program = programs[0]
                            if program.school is not None:
                                school = program.school
                                program = None
                    except (Program.DoesNotExist):
                        program = Program.objects.create(fullname=department_name, created_by=user)
                else:
                    try:
                        department = Department.objects.get(fullname=department_name)
                    except (Department.DoesNotExist):
                        department = Department.objects.create(fullname=department_name, division=division,created_by=user)
            
            if row[11] in ("FTFAC","FXFAC"):
                choice = "FT"
            elif row[11] in ("PTFAC","TEMPFC","3RDPRT","VSFAC"):
                choice = "PT"
            elif row[11] == "ADFAC":
                choice = "AD"
            elif row[11] in ("TCHFEL","TCHGR"):
                #this person is most likely a student.  Do not import them as a faculty member
                print "%s %s is a student.  Skipping..." % (row[3],row[2])
                continue
            else:
                choice = "STAFF"
                
            create = False
            staff = False
            
            try:
                people = Person.objects.filter(n_number=row[1]).order_by('-created_at')
                if people.count() > 0:
                    person = people[0]
                else:
                    raise Person.DoesNotExist
            except Person.DoesNotExist:
                create = True
                person = None
                if choice == "STAFF":
                    staff = True
                
            if person is not None:
                try:
                    person.facultymember
                except FacultyMember.DoesNotExist:
                    try:
                        person.staff
                        staff = True
                    except Staff.DoesNotExist:
                        #something really weird had happened, this person might be a student, etc.
                        continue
                
                
            if not staff:
                if not create:
                    fm = FacultyMember.objects.filter(n_number=row[1]).order_by('-created_at')[0]
                    existing += 1
                    changed = False
                    if fm.pidm is None or fm.pidm != int(row[0]):
                        fm.pidm = int(row[0]) 
                        changed = True
                    if fm.academic_title is None or fm.academic_title.strip() == "" or fm.academic_title != row[8]:
                        fm.academic_title = row[8]
                        changed = True
                    if fm.admin_title is None or fm.admin_title.strip() == "" or fm.academic_title != row[9]:
                        fm.admin_title = row[9]
                        changed = True
                    if fm.status is None or fm.status != choice:
                        fm.status = choice
                        changed = True
                    if fm.office is None or fm.office != row[16]:
                        fm.office = row[16]
                        changed = True
                    if fm.homeprogram is None or fm.homeprogram != program:
                        fm.homeprogram = program
                        changed = True
                    if fm.homeschool is None or fm.homeschool!= school:
                        fm.homeschool = school
                        changed = True
                    if fm.homedepartment is None or fm.homedepartment != department:
                        fm.homedepartment = department
                        changed = True
                    if fm.homedivision is None or fm.homedivision != division:
                        fm.homedivision = division
                        changed = True
                    if changed:
                        fm.save()
                    
                else:
                    fm = FacultyMember.objects.create(pidm=int(row[0]),
                                                 n_number=row[1],
                                                 first_name=row[3],
                                                 last_name=row[2],
                                                 academic_title=row[8],
                                                 admin_title=row[9],
                                                 status=choice,
                                                 office=row[16],
                                                 homeprogram=program,
                                                 homedepartment=department,
                                                 homeschool = school,
                                                 homedivision=division,
                                                 created_by=user)
                
                    created += 1
            else:
                if not create:
                    fm = Staff.objects.filter(n_number=row[1]).order_by('-created_at')[0]
                    s_existing += 1
                    if fm.pidm is None:
                        fm.pidm = int(row[0])
                    if fm.admin_title is None:
                        fm.admin_title = row[9]
                    if fm.status is None:
                        fm.status = "C"
                    if fm.office_location is None:
                        fm.office_location = row[16]
                    if fm.division is None:
                        fm.division = division
                    fm.save()
                    
                else:
                    fm = Staff.objects.create(pidm=int(row[0]),
                                                 n_number=row[1],
                                                 first_name=row[3],
                                                 last_name=row[2],
                                                 admin_title=row[9],
                                                 status="C",
                                                 office_location=row[16],
                                                 division=division,
                                                 created_by=user)
                
                    s_created += 1
            
            print fm
                
        print existing, created, s_existing, s_created