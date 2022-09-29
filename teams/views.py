from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Team
from eventmanage.views import getUserProfile, getUserName, home
from .forms import TeamBuildingForm
from profiles.views import profileView
from django.contrib import messages
from allauth.account.decorators import verified_email_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from datetime import datetime

team_association_limit = 3

@verified_email_required
def teams( request ):
    name = getUserName( request )
    userProfile = getUserProfile( request )
    if userProfile == None:
        messages.info( request, f"Please complete your profile before registering to Events or joinig Teams.")
        return HttpResponseRedirect( reverse( "profileView" ))
    all_teams = Team.objects.all()
    context = {
        "name" : name,
        "all_teams" : all_teams,
    }
    return render( request, 'teams.html', context )

@verified_email_required
def team_view( request, team_id ):
    user=request.user or None
    team_id = team_id
    name = getUserName( request )
    team = get_object_or_404( Team, pk=team_id )
    team_manager = team.manager or None
    is_member = False
    is_manager = False
    if user is not None:
        if team_manager == user:
            is_manager = True
        if team.members.filter( email=user.email ).count() == 1:
            is_member = True
    if is_manager or is_member:
        team_members = team.members.all() or None
    else:
        team_members = None
    now = datetime.now()
    upcoming_events = team.registered_teams.filter(Q(date__gte=now.date())).order_by("-date", "-time") or None
    past_events =  team.registered_teams.filter(Q(date__lt=now.date())) or None
    context = {
        "name" : name,
        "team" : team,
        "team_members" : team_members,
        "team_manager" : team_manager,
        "is_manager" : is_manager,
        "is_member" : is_member,
        "upcoming_events" : upcoming_events,
        "past_events" : past_events,
    }
    return render( request, "teamView.html", context )

@verified_email_required
def team_builder( request ):
    user = request.user
    name = getUserName( request )
    if request.method == "POST":
        if request.user.is_authenticated:
            userProfile = getUserProfile( request )
            if userProfile == None:
                messages.info( request, f"Please complete your profile before registering to Events or joinig Teams." )
                return HttpResponseRedirect( reverse( "profileView" ))
            else:
                if user.team_member.all().count() + user.team_manager.all().count() > team_association_limit:
                    messages.info( request, f"Exceeding maximum team association limit of {team_association_limit}" )
                    return HttpResponseRedirect( reverse("home"))
                form = TeamBuildingForm( request.POST , request.FILES )
                if form.is_valid():
                    model_instance = form.save( commit=False )
                    model_instance.manager = user
                    model_instance.save()
                    model_instance.members.add( user )
                    form.save_m2m()
                    messages.info( request, "Your Team has been created" )
                    return HttpResponseRedirect( reverse( "teams" ) )
                else: 
                    form = TeamBuildingForm
                    context = {
                    "name" : name,
                    "form" : form,
                    }
                    messages.info( request, "Please fill all the fields correctly" )
                    return render( request, "team_builder.html", context )
        else:
            messages.info( request, "Login required" )
            return HttpResponseRedirect( reverse( "home" ) )
    else:
        form = TeamBuildingForm
        context = {
            "name" : name,
            "form" : form,
        }
    return render( request, "team_builder.html", context )

@verified_email_required
def join_team( request, team_id ):
    user = request.user or None
    if request.method == "POST":
        team = get_object_or_404( Team, pk=team_id )
        userProfile = getUserProfile( request )
        if userProfile == None:
            messages.info( request, f"Please complete your profile before registering to Events or joinig Teams." )
            return HttpResponseRedirect( reverse( "profileView" ) )
        else:
            if user.team_member.all().count() + user.team_manager.all().count() > team_association_limit:
                messages.info( request, f"Exceeding maximum team association limit of { team_association_limit }" )
                return HttpResponseRedirect( reverse("home") )
            input_team_password = request.POST[ "team_password" ]
            set_team_password = team.password
            if set_team_password == input_team_password:
                team.members.add( request.user )
                team.save()
                return HttpResponseRedirect( reverse( "teams" ))
            else:
                messages.info( request, f"Invalid Password" )
                return HttpResponseRedirect( reverse( "teams" ))
        

@verified_email_required
def leave_team( request, team_id ):
    team = get_object_or_404( Team, pk=team_id )
    userProfile = getUserProfile( request )
    if userProfile == None:
        messages.info( request, f"Please complete your profile before registering to Events or joinig Teams." )
        return HttpResponseRedirect( reverse( "profileView" ))
    else:
        member_in_team = team.members.filter( email=request.user.email ).first() or None
        if member_in_team:
            team.members.remove( request.user )
            messages.info( request, f"Left { team.name }" )
        else:
            messages.info( request, f" Could not find {userProfile.first_name} {userProfile.last_name} in {team.name}" )
        return HttpResponseRedirect( reverse( "teams" ))
    