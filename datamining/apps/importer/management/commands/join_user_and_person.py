'''
Created on Oct 25, 2010

@author: edwards
'''
import csv
from datamining.apps.profiles.models import *
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Rejoins missing profiles with their users'

    def handle(self, *args, **options):
        email_addresses = csv.DictReader(open(args[0],"rU"), delimiter=',', quotechar='"')
        
        i = 0
        
        for row in email_addresses:
            n_number = row['Id']
            username = row['Email'][0:row['Email'].find("@")].lower()
            try:
                person = Person.objects.get(n_number=n_number)
            except:
                person = None
            try:
                user = User.objects.get(username=username,is_active=True)
            except:
                user = None
            if user is not None and person is not None:
                try:
                    profile = user.person_profile
                except:
                    profile = None
                if profile is None:
                    i += 1
                    print i,user,person
                    person.user_account = user
                    person.save()