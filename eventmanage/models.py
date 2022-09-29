from django.db import models

# Create your models here.

from django.db import models
from profiles.models import Profile, Sport, Area
from teams.models import Team
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
import datetime
from django.core.exceptions import ValidationError
# Create your models here.

def manager_upload_to(instance, filename):
    folder = instance.name
    return 'manager/{0}/{1}'.format(folder, filename)


class Manager( models.Model ):
    name = models.CharField( max_length=164 )
    manager = models.ForeignKey( User, on_delete=models.PROTECT )
    logo = models.ImageField( upload_to=manager_upload_to, blank=True )
    
    class Meta:
        ordering = [ 'name' ]

    def __str__(self):
        return self.name

class PaymentMethod( models.Model ):
    name = models.CharField( max_length=16, unique=True )

    class Meta:
        ordering = [ 'name' ]

    def __str__(self):
        return self.name

class EventType( models.Model ):
    name = models.CharField( max_length=164, unique=True )

    class Meta:
        ordering = [ 'name' ]

    def __str__(self):
        return self.name

def event_upload_to(instance, filename):
    folder = instance.title
    return 'event/{0}/{1}'.format(folder, filename)

class Event( models.Model ):
    manager = models.ForeignKey( Manager, on_delete=models.SET_NULL, null=True, related_name="event")
    event_type = models.ForeignKey( EventType, on_delete=models.SET_NULL, null=True, related_name="event" )
    team_event = models.BooleanField( default=False )
    min_team = models.IntegerField(  blank=True, null=True )
    max_team = models.IntegerField( blank=True, null=True )
    sport = models.ForeignKey( Sport, blank=True, null=True, on_delete=models.PROTECT, related_name="event" )
    title = models.CharField( max_length=256, unique=True )
    description = models.TextField( blank=True )
    date = models.DateField( blank=True )
    time = models.TimeField( blank=True )
    end_date = models.DateField( blank=True, null=True )
    end_time = models.TimeField( blank=True, null=True )
    location = models.CharField( max_length=256 )
    state = models.ForeignKey( Area, null=True, on_delete=models.SET_NULL, related_name="event" )
    city = models.CharField( max_length=120, blank=True )
    banner = models.ImageField( upload_to=event_upload_to, blank=True )
    poster = models.ImageField( upload_to=event_upload_to, blank=True )
    payment_required = models.BooleanField( default=False )
    payment_methods = models.ManyToManyField( PaymentMethod, blank=True )
    payment_gateway = models.URLField( blank=True, null=True )
    payment_number = models.CharField( max_length=16, blank=True, null=True )
    payment_instruction = models.TextField( blank=True )
    price = models.DecimalField( blank=True, null=True, max_digits=6, decimal_places=2 )
    event_created = models.DateTimeField( auto_now=True )
    registration_open = models.BooleanField( default=True )
    instruction = models.TextField( blank=True )
    registrants = models.ManyToManyField( User, blank=True, related_name='registrants' )
    register_localy = models.BooleanField( default=True )
    external_link = models.URLField( blank=True )
    teams = models.ManyToManyField( Team, blank=True, related_name='registered_teams' )
    facebook = models.URLField( blank=True )
    
    class Meta:
        ordering = [ "-date" ]

    def save(self, *args, **kwargs):
        if self.date < datetime.date.today():
            raise ValidationError( "The date cannot be in the past!" )
        if self.end_date < self.date:
            raise ValidationError( "End date must be after start date" )
        if self.date == self.end_date:
            if self.end_time < self.time:
                raise ValidationError("Event end date and time must be after start date and time" )
        super(Event, self).save( *args, **kwargs )

    def __str__( self ):
        return self.title

class TransactionID( models.Model ):
    event = models.ForeignKey( Event, on_delete=models.CASCADE, related_name="transaction_event" )
    user = models.ForeignKey( User, on_delete=models.CASCADE, related_name="transaction_user" )
    method = models.ForeignKey( PaymentMethod, on_delete=models.CASCADE, related_name="trasaction_method" )
    transaction_id = models.CharField( max_length=64 )
    transaction_time = models.DateTimeField( auto_now=True )

    class Meta:
        order_with_respect_to = 'event'
        
    def __str__( self ):
        return self.transaction_id

def community_upload_to(instance, filename):
    folder = instance.name
    return 'community/{0}/{1}'.format(folder, filename)

class Community( models.Model ):
    primary_manager = models.ForeignKey( Manager, on_delete=models.PROTECT, related_name="primary_manager" )
    name = models.CharField( max_length=168 )
    short_description = models.TextField( blank=True )
    facebook = models.URLField( blank=True )
    twitter = models.URLField( blank=True )
    instagram = models.URLField( blank=True )
    area = models.ForeignKey( Area, on_delete=models.PROTECT, blank=True )
    sport = models.ManyToManyField( Sport )
    location = models.CharField( max_length=256, blank=True )
    phone = models.TextField( max_length=16, blank=True )
    community_logo = models.ImageField( upload_to=community_upload_to, blank=True )
    community_poster = models.ImageField( upload_to=community_upload_to, blank=True )
    members = models.ManyToManyField( User, blank=True, related_name="community" )

    def __str__(self):
        return self.name
    



