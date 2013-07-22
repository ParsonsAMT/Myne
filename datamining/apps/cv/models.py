from django.db.models import *
from django.contrib.auth.models import User, Group

"""
Degrees Held
Professional Affiliations
Clients
Publications  -- including catalogs
Press
Presentations/Artist Talks/conferences/symposiums
Exhibitions
Discography
Performances
Awards and Honors
Screenings/Festivals
Grants and Fellowships
Collections and Commissions
"""

from profiles.models import BaseModel, Person

class CV (BaseModel):

    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CVs"

    owner = OneToOneField(Person,related_name="generated_cv",null=True,editable=False)

    basic_info = TextField("Basic Info",blank=True)
    degrees = TextField("Degrees Held",blank=True)
    affiliations = TextField("Professional Affiliations",blank=True)
    clients = TextField("Clients",blank=True)
    publications = TextField("Publications",blank=True)
    press = TextField("Press",blank=True)
    presentations = TextField("Presentations/Artist Talks/Conferences/Symposiums",blank=True)
    exhibitions = TextField("Exhibitions",blank=True)
    discography = TextField("Discography",blank=True)
    performances = TextField("Performances",blank=True)
    awards = TextField("Awards and Honors",blank=True)
    screenings = TextField("Screenings/Festivals",blank=True)
    grants = TextField("Grants and Fellowships",blank=True)
    collections = TextField("Collections and Commissions",blank=True)
