from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from profiles.models import Profile
from profiles.models import Sport

# Create your models here.

def team_upload_to(instance, filename):
    folder = instance.name
    return 'team/{0}/{1}'.format(folder, filename)

class Team(models.Model):
    name = models.CharField( max_length=164 )
    logo = models.ImageField( upload_to=team_upload_to, blank=True )
    description = models.TextField( blank=True, )
    sport = models.ForeignKey( Sport, on_delete=models.CASCADE, default=1 )
    manager = models.ForeignKey( User, related_name='team_manager', on_delete=models.CASCADE )
    members = models.ManyToManyField( User, blank=True, related_name='team_member' )
    password = models.CharField( max_length=50 )

    def __str__(self):
        return self.name

