'''
Created on Mar 2, 2011

@author: edwards
'''
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django_auth_ldap.backend import LDAPBackend
from datamining.apps.profiles.models import FacultyMember, Staff, Student


class SchoolLDAPBackend(LDAPBackend):
    """
    This is the LDAP authentication for New School faculty, students and staff.  At present,
    it does its best to figure out whether a new person is one of the three roles contained in
    the system.  In the future, we will need to find ways to create hybrid profiles for users
    who occupy multiple roles.
    
    To look into the LDAP itself, you can use the following commands (replace the example text with actual values)
    
    >>> import ldap
    >>> ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
    >>> conn = ldap.initialize("ldaps://your.ldap.server.edu")
    >>> conn.bind_s("cn=commonLoginName,o=organization","password",ldap.AUTH_SIMPLE)
    >>> conn.search_s("o=organization",ldap.SCOPE_SUBTREE, "(&(objectclass=user)(sn=Lastname)(givenName=Firstname))")
    
    """
    def get_or_create_user(self, username, ldap_user):
        user,created = User.objects.get_or_create(username=username)
        
        try:
            person = user.person_profile
        except Exception:
            person = None
               
        if person is None:
            if ldap_user.dn.find("ou=FACULTY") >= 0:
                person = FacultyMember(first_name = ldap_user.attrs['givenName'][0],
                                            last_name = ldap_user.attrs['sn'][0],
                                            n_number = ldap_user.attrs['physicalDeliveryOfficeName'][0],
                                            created_by = user)
 
            if ldap_user.dn.find("ou=STUDENT") >= 0:
                person = Student(first_name = ldap_user.attrs['givenName'][0],
                                            last_name = ldap_user.attrs['sn'][0],
                                            n_number = ldap_user.attrs['physicalDeliveryOfficeName'][0],
                                            created_by = user)
 
            if ldap_user.dn.find("ou=STAFF") >= 0:
                person = Staff(first_name = ldap_user.attrs['givenName'][0],
                                            last_name = ldap_user.attrs['sn'][0],
                                            n_number = ldap_user.attrs['physicalDeliveryOfficeName'][0],
                                            created_by = user)

            person.user_account = user
            person.save()
 
        return User.objects.get_or_create(username=username)


class EmailModelBackend(ModelBackend):
    """
    Authenticates against django.contrib.auth.models.User.  This is an older backend whose use
    preceded the SchoolLDAPBackend authentication.
    
    """
    # TODO: change to use email instead of username
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
