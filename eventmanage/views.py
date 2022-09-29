from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.core.mail import send_mail
from allauth.account.decorators import verified_email_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from profiles.models import Profile
from .models import PaymentMethod, TransactionID, Manager, EventType, Event
from .forms import EventCreationForm
import datetime
import markdown2
from markdown2 import Markdown
from datetime import datetime
from django.db.models import Q

# GET USER PROFILE or NONE
def getUserProfile( request ):
    if request.user.is_authenticated:
        user = request.user
        try:
            profile = Profile.objects.get( user = user )
        except Profile.DoesNotExist:
            profile = None
    else:
        profile = None
    return profile

# GET USERNAME OR EMAIL IF LOGGED IN, GUEST IF NOT LOGGED IN
def getUserName( request ):
    profile = getUserProfile( request )
    if profile == None:
        if request.user.is_authenticated:
            name = request.user.email
        else:
            name = "Guest"
    else:
        name = f"{profile.first_name}  {profile.last_name}"
    return name

# MANAGER OR NOT
def get_host( request ):
    if request.user.is_authenticated:
        try:
            manager = Manager.objects.get( manager=request.user )
        except Manager.DoesNotExist:
            manager = None
    else:
        manager = None
    return manager

# HOME PAGE, LIST OF EVENTS
def home( request ):
    name = getUserName( request )
    manager = get_host( request )
    now = datetime.now()
    future_events = Event.objects.filter(Q(date__gte=now.date())).order_by("-date", "-time") or None
    past_events = Event.objects.filter(Q(date__lt=now.date())).order_by( "date", "time" ) or None
    context = {
        "events" : future_events,
        "past_events" : past_events,
        "name" : name,
        "manager" : manager
    }
    return render( request, "home.html", context )


# EVENT LANDING PAGE 
def event( request, event_id ):
    if request.user.is_authenticated:
        user = request.user
    event = get_object_or_404( Event, pk=event_id )
    profile = getUserProfile( request )
    if profile == None:
        registered = False
        teams_managed = None
        teams_registered = None
    else:
        if event.team_event:
            teams_registered = event.teams.all()
        else:
            teams_registered = None
        try:
            teams_managed = profile.team_manager.all()
        except:
            teams_managed = None
        if user:
            if user.registrants.filter( pk=event_id ).count() == 1:
                registered = True
            else:
                registered = False
        else:
            registered = False
    name = getUserName( request )
    manager = get_host( request )
    raw_description = event.description
    markdowner = Markdown()
    marked = markdowner.convert( raw_description )
    context = {
        "name" : name,
        "event" : event,
        "profile" : profile,
        "registered" : registered,
        "teams_managed" : teams_managed,
        "teams_registered" : teams_registered,
        "manager" : manager,
        "marked" : marked
    }
    return render( request, "event.html", context )

#REGISTER TO NON TEAM EVENT IF EVENT IS FREE
@verified_email_required
def register( request, event_id ):
    user = request.user
    event = get_object_or_404( Event, pk=event_id )
    profile = getUserProfile( request )
    if profile == None:
        message = "Please complete your profile <a href='{% url 'profileView' %}'>here</a> before registering for an event"
        name = getUserName( request )
        context = {
            "name" : name,
            "event" : event,
        }
        messages.add_message( request, messages.INFO, message )
        return render( request, "event.html", context)
    else:
        if user.registrants.filter( pk=event_id ).count() == 1:
            message = f"You are already Registered to this event"
            messages.add_message( request, messages.INFO, message )
            return event( request, event_id )
        else:
            if event.registration_open:
                event.registrants.add( user )
                email = request.user.email
                event_name = event.title
                event_date = event.date
                name = f"{profile.first_name} {profile.last_name}"
                subject =  "Registration Confirmation"
                message = f"Hello {name}, \n You are now registered to {event_name} to be held on {event_date} "
                email_from = None
                email_to = email
                send_mail(
                    subject,
                    message,
                    email_from,
                    [email_to],
                    fail_silently=True,
                )
                message = f"Registered to {event_name} successfully"
                messages.add_message( request, messages.INFO, message )
                return home( request )
            else:
                return HttpResponse( "REGISTRATION CLOSED" )

# UNREGISTER FROM  NON TEAM EVENT 
@verified_email_required
def unregister( request, event_id ):
    user = request.user
    event = get_object_or_404( Event, pk=event_id )
    profile = getUserProfile( request )
    if profile == None:
        message = "Please complete your profile <a href='{% url 'profileView' %}'>here</a> before registering for an event"
        messages.add_message( request, messages.INFO, message )
        return event( request, event_id )
    else:
        if user.registrants.filter( pk=event_id ).count() == 1:
            event.registrants.remove( user )
            email = request.user.email
            event_name = event.title
            event_date = event.date
            name = f"{profile.first_name} {profile.last_name}"
            subject =  f"Unregisterd from {event_name}"
            message = f"Hello {name}, \n You have unregistered from {event_name} to be held on {event_date} "
            email_from = None
            email_to = email
            send_mail(
                subject,
                message,
                email_from,
                [email_to],
                fail_silently=False,
            )
            message = f"You have unregisterd from {event.title}"
            messages.add_message( request, messages.INFO, message )
            return home( request )
        else:
            message="Oops... Something went wrong. Please contact us."
            messages.add_message( request, messages.INFO, message )
            return event( request, event_id )

# REGISTER TO TEAM EVENT
@verified_email_required
def register_team( request, event_id ):
    if request.method == "POST":
        event_id = event_id
        team_id = request.POST.get( "team_select" )
        event = get_object_or_404( Event, pk=event_id )
        team = get_object_or_404( Team, pk=team_id )
        team_members = team.members.all()
        event.teams.add(team)
        for member in team_members:
            name = f"{member.first_name} {member.last_name}"
            subject =  f"Registerd to {event.title}"
            message = f"Hello {name}, \n Your team {team.name} have been registered to {event.title} "
            email_from = None
            email_to = member.user.email
            send_mail(
                subject,
                message,
                email_from,
                [email_to],
                fail_silently=False,
            )
        message=f"Registered to {event.title}"
        messages.add_message( request, messages.INFO, message )
        return HttpResponseRedirect( reverse( "event", args=[ event_id ] ) )
    else:
        return HttpResponseRedirect( reverse( "home" ) )

# UNREGISTER FROM TEAM EVENT
@verified_email_required
def unregister_team( request, event_id, team_id ):
    event = get_object_or_404( Event, pk=event_id )
    team = get_object_or_404( Team, pk=team_id )
    event.teams.remove( team )
    return HttpResponseRedirect( reverse("team_view", args=[ team_id ]) )

# REGISTER TO PAID NON TEAM EVENT
@verified_email_required
def register_paid( request, event_id ):
    if request.method == "POST":
        event_id = event_id
        event = get_object_or_404( Events, pk=event_id )
        profile = getUserProfile( request )
        if profile == None:
            return Http404( "User Not Found" )
        else: 
            payment_method_id = int( request.POST[ "payment_method" ] )
            transaction_id = str( request.POST[ "transaction_id" ] )
            payment_method = get_object_or_404( PaymentMethod, pk=payment_method_id )
            new_transaction = TransactionID.objects.Create( event=event, user=profile, method=payment_method, transaction_id=transaction_id )
            new_transaction.save()
            return register( request, event_id )

# CREATE EVENT
@verified_email_required
def create_event( request ):
    name = getUserName( request )
    if request.method == "POST":
        form = EventCreationForm( request.POST, request.FILES )
        manager = get_host(request)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.manager = manager
            model_instance.save()
            form.save_m2m()
            messages.info(request, "Event Created Successfully")
            return HttpResponseRedirect( reverse( "host" ) )
        else:
            form = EventCreationForm()
            context = {
                "form" : form,
                "name" : name,
                "host" : host
            }
            messages.error( request, "Failed to save Form" )
            return render( request, "event_creator.html", context )
    else:
        manager = get_host( request )
        if manager is None:
            return HttpResponseForbidden( "ACCESS DENIED" )
        form = EventCreationForm()
        context = {
                "form" : form,
                "name" : name,
                "manager" : manager,
        }
        return render(request, "event_creator.html", context)


# Community Admin
@verified_email_required
def host(request):
    name = getUserName( request )
    manager = get_host( request )
    if manager is None:
        return HttpResponseForbidden( "ACCESS DENIED - COMMUNITY ADMINS ONLY" )
    try:
        hosted_events = Event.objects.filter( manager=manager )
    except ObjectDoesNotExist:
        hosted_events = None
    context = {
        "name" : name,
        "manager" : manager,
        "hosted_events" : hosted_events,
    }
    return render(request, "host.html", context)
        
# Event Data
@verified_email_required
def view_event_data(request, event_id):
    name = getUserName(request)
    manager = get_host(request)
    event = get_object_or_404(Event, pk=event_id)
    if event.manager == manager:
        registrants = event.registrants.all()
        profiles = []
        for registrant in registrants:
            try:
                profile = Profile.objects.get( user=registrant )
                profiles.append(profile)
            except Profile.DoesNotExist:
                pass
        context = {
            "name" : name,
            "manager" : manager,
            "profiles" : profiles,
            "event" : event
        }
        return render(request, "event_data.html", context)
    else:
        return HttpResponseForbidden("Access Denied")

# EDIT EVENT
@verified_email_required
def edit_event( request, event_id ):
    user = request.user
    name = getUserName( request )
    manager = get_host( request )
    event = get_object_or_404( Event, pk=event_id, manager=manager )
    if request.method == "POST":
        form = EventCreationForm( request.POST, instance=event )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse("host") )
        else:
            form = EventCreationForm( instance=event )
        context = {
            "form" : form,
            "name" : name,
            "manager" : manager,
            "id" : event_id
        }
        return render(request, "event_creator.html", context)
        
    else:
        form = EventCreationForm( instance=event )
        context = {
                "form" : form,
                "name" : name,
                "manager" : manager,
                "id" : event_id
        }
        return render(request, "event_creator.html", context)
    

# DELETE EVENT
@verified_email_required
def delete_event( request, event_id ):
    user = request.user
    manager = get_host( request )
    event = get_object_or_404( Event, pk=event_id, manager=manager )
    event.delete()
    return HttpResponseRedirect( reverse("host") )