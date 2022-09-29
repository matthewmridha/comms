from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from django import forms
from .forms import ProfileForm
from django.utils import timezone
from allauth.account.decorators import verified_email_required
from .models import Profile, Area, Sport
from eventmanage.views import getUserProfile, getUserName, get_host
from django.contrib import messages 
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your views here.

# MAIN PROFILE VIEW - aUTHENTICATION REQUIRED
# RENDERS PROFILE CREATION FORM IF NO PROFILE IS FOUND
# EDIT PROFILE, SHOW REGISTERED EVENTS IF PROFILE 
@verified_email_required
def profileView( request ):
    name = getUserName( request )
    manager = get_host( request )
    user = request.user
    if request.method == "POST":
        try:
            profile = Profile.objects.get( user=user )
        except Profile.DoesNotExist:
            profile = None
        if profile == None:
            form = ProfileForm( request.POST )
            if form.is_valid():
                model_instance = form.save( commit=False )
                model_instance.user = user
                model_instance.save()
                form.save_m2m()
                messages.info( request, "Thank you for completing your profile" )
                return HttpResponseRedirect(reverse("home"))
            else:
                context = {
                    "form" : form,
                    "name" : name,
                    "manager" : manager,
                }
                return render( request, "profile.html", context )
    else:
        try:
            profile = Profile.objects.get( user=user )
        except ObjectDoesNotExist:
            form = ProfileForm()
            context = {
                "form" : form,
                "name" : name,
                "manager" : manager,
            }
            return render( request, "profile.html", context )
        now = datetime.now()
        upcoming_events = user.registrants.filter(Q(date__gte=now.date())).order_by("-date", "-time") or None
        past_events =  user.registrants.filter(Q(date__lt=now.date())) or None
        teams = user.team_member.all() or None
        team_events = []
        if teams != None:
            for team in teams:
                for event in team.registered_teams.filter(Q(date__gte=now.date())):
                    team_events.append( event )
        managed_teams = user.team_manager.all() or None
        form = ProfileForm( instance=profile )
        context = {
            "profile" : profile,
            "name" : name, 
            "upcoming_events" : upcoming_events,
            "past_events" : past_events,
            "teams" : teams,
            "managed_teams" : managed_teams,
            "team_events" : team_events,
            "manager" : manager,
            "populated_form" : form,
        }
        return render( request, "profile.html", context )

# EDIT EXISTING PROFILE
@verified_email_required
def edit_profile( request ):
    user = request.user
    profile = get_object_or_404( Profile, user=user )
    if request.method == "POST":
        form = ProfileForm( request.POST, instance=profile )
        if form.is_valid():
            form.save()
        messages.info( request, "Your Profile has been Updated" )
        return HttpResponseRedirect( reverse( "home" ))
    else:
        return HttpResponseNotAllowed( "POST", )

