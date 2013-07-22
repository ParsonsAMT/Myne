from django.forms import *
from tagging.forms import TagField
from datamining.apps.profiles.models import Work, Section, FacultyMember,\
    Expertise, Student, Course, WorkURL, Organization, Person, Staff,\
    Division, School, Department, Program, WorkType
from django.contrib.admin.widgets import AdminDateWidget
from ajax_select.fields import AutoCompleteSelectMultipleField,\
    AutoCompleteSelectField


class PersonActivateForm (Form):
    person_id = IntegerField(widget=HiddenInput)
    email = EmailField(help_text="Enter person's email address")

class AdminFacultyForm (ModelForm):
    class Meta:
        model = FacultyMember
        exclude = ( 'user_account' )
#    expertise = ModelMultipleChoiceField( required=False,
#                                          queryset=Expertise.objects.all(),
#                                          widget=SelectMultiple(attrs={'size':5}),
#                                          help_text="Select up to five areas of teaching expertise", )
    #expertise = AutoCompleteSelectMultipleField( 'expertise', required=False, help_text="Add up to 5 areas of expertise that describe you and your work")
    expertise = ModelMultipleChoiceField(queryset=Expertise.objects.all(), required=False)
    
    homedivision = AutoCompleteSelectField( 'division', required=False)
    homeschool = AutoCompleteSelectField( 'school', required=False)
    homedepartment = AutoCompleteSelectField( 'department', required=False)
    homeprogram = AutoCompleteSelectField( 'program', required=False)
    tags = TagField( required=False,
                     widget=Textarea(),
                     max_length=2000,
                     help_text="Keywords that describe your areas of interest & research, separated by commas" )

    use_which_cv = ChoiceField( required=False,
                                widget=RadioSelect(),
                                choices=FacultyMember.CV_CHOICES )
    
    allow_cv_viewing_by = ChoiceField( required=False, 
                                    widget = Select(),
                                    choices= (('A','all registered users'),('O','administrators only')))

    allow_syllabus_viewing_by = ChoiceField( required=False, 
                                    widget = Select(),
                                    choices= (('A','all registered users'),('O','administrators only')))

    def clean_expertise(self):
        data = self.cleaned_data['expertise']
        if len(data) > 5:
            raise forms.ValidationError("Please select a maximum of 5 areas")
        return data

    def clean_bio(self):
        data = self.cleaned_data['bio']
        words = data.split()
        if len(words) > 250:
            raise forms.ValidationError("Please enter at most 250 words. (%s entered)" % len(words))
        return data
        

class FacultyForm (AdminFacultyForm):
    class Meta (AdminFacultyForm.Meta):
        exclude = ( 'n_number', 'status', 'academic_title', 'admin_title', 'user_account', 'first_name', 'last_name' )

    tags = TagField( required=False,
                     widget=Textarea(),
                     max_length=2000,
                     help_text="Keywords that describe your areas of interest & research, separated by commas" )

#    def clean_photo(self):
#        if ''==self.instance.photo and ( 'photo' not in self.cleaned_data or None==self.cleaned_data['photo'] ):
#            raise forms.ValidationError("Photo cannot be blank.")
#        return self.cleaned_data['photo']
      
class AdminStudentForm (ModelForm):    
        
    class Meta:
        model = Student
        exclude = ( 'n_number', 'user_account' )
        
    #expertise = AutoCompleteSelectMultipleField( 'expertise', required=False, help_text="Add up to 5 areas of expertise that describe you and your work")
    expertise = ModelMultipleChoiceField(queryset=Expertise.objects.all(), required=False, label="Areas of Interest")
    
    tags = TagField( required=False,
                     widget=Textarea(),
                     max_length=2000,
                     help_text="Keywords that describe your areas of interest & research, separated by commas" )

    use_which_cv = ChoiceField( required=False,
                                widget=RadioSelect(),
                                choices=Student.CV_CHOICES )
    
    allow_cv_viewing_by = ChoiceField( required=False, 
                                    widget = Select(),
                                    choices= (('P','the public'),
                                              ('A','all registered users'),
                                              ('O','administrators only')))

    allow_syllabus_viewing_by = ChoiceField( required=False, 
                                    widget = Select(),
                                    choices= (('P','the public'),
                                              ('A','all registered users'),
                                              ('O','administrators only')))

    def clean_expertise(self):
        data = self.cleaned_data['expertise']
        if len(data) > 5:
            raise forms.ValidationError("Please select a maximum of 5 areas")
        return data

    def clean_bio(self):
        data = self.cleaned_data['bio']
        words = data.split()
        if len(words) > 250:
            raise forms.ValidationError("Please enter at most 250 words. (%s entered)" % len(words))
        return data
        
class StudentForm (AdminStudentForm):
    class Meta (AdminStudentForm.Meta):
        exclude = ( 'n_number', 'status', 'user_account', 'first_name', 'last_name' )

    tags = TagField( required=False,
                     widget=Textarea(),
                     max_length=2000,
                     help_text="Keywords that describe your areas of interest & research, separated by commas" )

#    def clean_photo(self):
#        if ''==self.instance.photo and ( 'photo' not in self.cleaned_data or None==self.cleaned_data['photo'] ):
#            raise forms.ValidationError("Photo cannot be blank.")
#        return self.cleaned_data['photo']

class AdminStaffForm (ModelForm):
    class Meta:
        model = Staff
        exclude = ( 'user_account' )

    #expertise = AutoCompleteSelectMultipleField( 'expertise', required=False, help_text="Add up to 5 areas of expertise that describe you and your work")
    expertise = ModelMultipleChoiceField(queryset=Expertise.objects.all(), required=False)
    
    division = AutoCompleteSelectField( 'division', required=False)
    tags = TagField( required=False,
                     widget=Textarea(),
                     max_length=2000,
                     help_text="Keywords that describe your areas of interest & research, separated by commas" )

    status = ChoiceField( required=False,
                                widget=RadioSelect(),
                                choices=Staff.STATUS_CHOICES)
    
    use_which_cv = ChoiceField( required=False,
                                widget=RadioSelect(),
                                choices=Person.CV_CHOICES )
    
    allow_cv_viewing_by = ChoiceField( required=False, 
                                    widget = Select(),
                                    choices= (('A','all registered users'),('O','administrators only')))

    def clean_expertise(self):
        data = self.cleaned_data['expertise']
        if len(data) > 5:
            raise forms.ValidationError("Please select a maximum of 5 areas")
        return data

    def clean_bio(self):
        data = self.cleaned_data['bio']
        words = data.split()
        if len(words) > 250:
            raise forms.ValidationError("Please enter at most 250 words. (%s entered)" % len(words))
        return data
        

class StaffForm (AdminStaffForm):
    class Meta (AdminFacultyForm.Meta):
        exclude = ( 'n_number', 'status', 'user_account', 'first_name', 'last_name' )

    tags = TagField( required=False,
                     widget=Textarea(),
                     max_length=2000,
                     help_text="Keywords that describe your areas of interest, separated by commas" )


        
class AdminCourseForm (ModelForm):
    prerequisites = AutoCompleteSelectMultipleField('course', required=False)
    class Meta:
        model = Course
        exclude = ( 'projects', 'minimum_credits', 'credit_range_type', 'maximum_credits' )
        widgets = {
            'status': RadioSelect,
            'levels': RadioSelect,
            'format': RadioSelect,
            'method': RadioSelect,
            'projects': SelectMultiple(attrs={'size': 3}),
        }

class CourseForm (AdminCourseForm):
    class Meta (AdminCourseForm.Meta):
        exclude = ( 'projects', 'title', 'coursenumber', 'subject', 'minimum_credits', 'credit_range_type', 'maximum_credits' )

class AdminSectionForm (ModelForm):
    instructors = AutoCompleteSelectMultipleField('person', required=False)
    course = AutoCompleteSelectField('course', required=True)
    semester = AutoCompleteSelectField('semester', required=True)
    class Meta:
        model = Section
        widget = {
            'projects': SelectMultiple(attrs={'size': 3}),
        }
        exclude = ('projects',)
        
class SectionForm (AdminSectionForm):
    class Meta (AdminSectionForm):
        exclude = ('crn', 'course', 'projects')

class ProgramForm (ModelForm):
    facultylist = AutoCompleteSelectMultipleField('person', required=False)	
    groups = AutoCompleteSelectMultipleField('group', required=False)	
    class Meta:
        model = Program
        exclude = ('abbreviation')
		
class WorkURLForm (ModelForm):
    url = URLField(initial="http://",verify_exists=False)
    
    class Meta:
        model = WorkURL
        exclude = ( 'person' )
        
class WorkForm (ModelForm):
    creators = AutoCompleteSelectMultipleField('person', required=True, help_text="Include yourself and anyone else on DataMYNE who helped create this")
    #work_type = AutoCompleteSelectMultipleField('worktype', required=True, help_text="Select up to three")
    work_type = ModelMultipleChoiceField(queryset=WorkType.objects.all(), required=False)
    class Meta:
        model = Work
        exclude = ( 'person', 'type' )
    date = DateField(widget=AdminDateWidget(),required=False)
    url = URLField(widget=TextInput(),required=False,verify_exists=False,initial="http://")
    tags = TagField( required=False,
                 widget=Textarea(),
                 max_length=2000,
                 help_text="Keywords that describe your work, separated by commas" )

    def clean_work_type(self):
        data = self.cleaned_data['work_type']
        if len(data) > 3:
            raise forms.ValidationError("Please select a maximum of 3 types")
        return data

class SyllabusForm (ModelForm):
    class Meta:
        model = Section
        exclude = ( 'feeds', 'credits', 'course', 'semester', 'instructors', 'title', 'syllabus_orig_filename', 'crn', 'projects', 'use_as_demo', )

FilterChoices = (
    ('or', 'Search for faculty with ANY of the expertise selected above'),
    ('and', 'Search for faculty with ALL of the expertise selected above'),
)

class FilterForm (Form):
    status    = MultipleChoiceField( choices=FacultyMember.STATUS_CHOICES,
                                     initial=[c[0] for c in FacultyMember.STATUS_CHOICES],
                                     required=True )
    expertise = ModelMultipleChoiceField( queryset=Expertise.objects.all(),
                                          required=True )
    filteroption = ChoiceField(choices=FilterChoices, required=True)

SubjectChoices = (
    ('Account Management', 'Account Management'),
    ('Report Errors', 'Report Errors'),
    ('General Inquiry', 'General Inquiry'),
)

class ContactForm (Form):
    name = CharField(required=True)
    email = EmailField(required=True)
    subject = ChoiceField(choices=SubjectChoices, required=True)
    message = CharField(widget=Textarea, required=True)

class ContactStudentForm (Form):
    name = CharField(required=True)
    email = EmailField(required=True)
    subject = CharField(required=True)
    message = CharField(widget=Textarea, required=True)

class OrganizationForm (ModelForm):
    leaders = AutoCompleteSelectMultipleField('person', required=False)
#    leaders_text = CharField(required=True)
    members = AutoCompleteSelectMultipleField('person', required=False)
    courses = AutoCompleteSelectMultipleField('course', required=False)
    projects = AutoCompleteSelectMultipleField('work', required=False)
    tags = TagField( required=False,
                 widget=Textarea(),
                 max_length=2000,
                 help_text="Keywords that describe your group, separated by commas" )
    class Meta:
        model = Organization
        exclude = ("projects",)
        
class SearchForm (Form):
    content = CharField(required=True)
    start = IntegerField(required=False)

class InvitationForm (Form):
    invites = CharField(widget=Textarea(),required=False)
    message = CharField(widget=Textarea(),required=False)
        
class GrantPermissionForm (Form):
    users = AutoCompleteSelectMultipleField('person', required=False)
    division = ModelChoiceField(queryset=Division.objects.filter(type="ac"), required=False,
                                widget=Select(attrs={'onchange': 'this.form.submit();'}))
    department = ModelMultipleChoiceField(queryset=Department.objects.all(), required=False)
    school = ModelMultipleChoiceField(queryset=School.objects.all(), required=False,
                                        widget=SelectMultiple(attrs={'onchange': 'this.form.submit();'}))
    
    def __init__(self, *args, **kwargs):
        super(GrantPermissionForm, self).__init__(*args, **kwargs)
        if self.is_valid():
            parent = self.cleaned_data['school']
            if parent:
                program_list = Program.objects.none()
                for p in parent:
                    program_list |= Program.objects.filter(school = p.id)
                self.fields['program'] = ModelMultipleChoiceField(queryset=program_list, required=False)
        else:
            self.fields['program'] = ModelMultipleChoiceField(queryset=Program.objects.all(), required=False)