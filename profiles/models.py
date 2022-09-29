from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



# Create your models here.

class Area(models.Model):
    area = models.CharField( max_length=164, unique=True)

    class Meta:
        ordering = ('area',)

    def __str__(self):
        return self.area

class Sport(models.Model):
    sport = models.CharField( max_length=164, unique=True)

    class Meta:
        ordering = ('sport',)

    def __str__(self):
        return self.sport

class Profile(models.Model):
    Male = 'Male'
    Female = 'Female'
    Other = 'Other'
    GENDER_CHOICES = (
        ( Male, 'Male' ),
        ( Female, 'Female' ),
        ( Other, 'Other' )
    )
    user = models.OneToOneField( User, on_delete=models.CASCADE )
    phone = models.CharField( max_length=17, blank=True, unique=True )
    first_name = models.CharField( max_length=64 )
    last_name = models.CharField( max_length=64 )
    gender = models.CharField( choices=GENDER_CHOICES, max_length=8, blank=False, default='Unspecified' )
    birthday = models.DateField( auto_now=False, auto_now_add=False )
    state = models.ForeignKey( Area, null=True, on_delete=models.PROTECT )
    city = models.CharField( max_length=164 )
    country = models.CharField( default="Bangladesh", max_length=164 )
    address = models.CharField( blank=True, null=True, max_length=256 )
    sport = models.ManyToManyField( Sport )
    communication = models.BooleanField( default=True )
    profile_created = models.DateTimeField( auto_now_add=True, auto_now=False )
    profile_updated = models.DateTimeField( auto_now=True )

    def __str__(self):
        return (f"{self.user.email}")

    



    