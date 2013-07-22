'''
Created on Oct 11, 2010

@author: edwards
'''
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from datamining.apps.profiles.models import Section
from django.db.models.aggregates import Count

class Command(BaseCommand):
    args = ''
    help = 'Removes duplicate section data from faulty imports'

    def handle(self, *args, **options):
        #deletes sections from what appears to be an abortive first run of the import
        print "weeding out early import"
        Section.objects.filter(created_at__range=(datetime.datetime(2010,7,26,15,0),datetime.datetime(2010,7,26,15,30,21))).order_by("-created_at").delete()
        #deletes sections from semesters where we already have information
        print "removing duplicate semesters"
        Section.objects.filter(created_at__range=(datetime.datetime(2010,7,26),datetime.datetime(2010,7,27))).filter(Q(semester__year__range=(2005,2008))|Q(semester__year__exact=2009,semester__term="sp")).delete()
        #reunite split sections
        print "reuniting split sections"
        splits = Section.objects.all().values("crn","course__subject__abbreviation","course__coursenumber","semester").annotate(dupes=Count("crn")).filter(dupes__gt = 1)
        print "found %d sections" % splits.count()
        
        for index,split in enumerate(splits):
            if index % 10 == 0:
                print index,
            head = None
            sections = Section.objects.filter(crn=                          split["crn"],
                                              course__subject__abbreviation=split["course__subject__abbreviation"],
                                              course__coursenumber=         split["course__coursenumber"],
                                              semester=                     split["semester"])
            for section in sections:
                if head is None:
                    head = section
                else:
                    instructors = section.instructors.all()
                    for instructor in instructors:
                        if instructor not in head.instructors.all():
                            head.instructors.add(instructor)
                    section.delete()
        print
        print "finished"