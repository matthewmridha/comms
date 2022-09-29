from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from profiles.models import Profile
from eventmanage.models import Event as Events
from eventmanage.views import getUserProfile, getUserName
from allauth.account.decorators import verified_email_required
from django.core.exceptions import PermissionDenied
import csv
from django.core.exceptions import ObjectDoesNotExist
import datetime



# Create your views here.

# DOWNLOAD TO CSV
@verified_email_required
def download( request, event_id ):
    
    if event_id == "all":

        response = HttpResponse(content_type='text/csv')
        response[ 'Content-Disposition' ] = 'attachment; filename="all_profiles.csv"'

        writer = csv.writer( response )
        writer.writerow(
            [ 
                'Created', 
                'Email', 
                'First Name', 
                'Last Name', 
                'Gender', 
                'Phone', 
                'State', 
                'Sport'
            ]
        )
        for profile in Profile.objects.all():
            email = profile.user.email
            firstname = profile.first_name
            lastname = profile.last_name
            gender = profile.gender
            phone = profile.phone
            state = profile.state
            created = profile.profile_created.strftime("%c")
            sport = []
            for s in profile.sport.all():
                sport.append(s.sport)
            
            writer.writerow(
                [ 
                    created,
                    email, 
                    firstname, 
                    lastname, 
                    gender, 
                    phone, 
                    state, 
                    sport
                ] 
            )

    else:
        event = get_object_or_404( Events, pk=event_id )
        print(request.user)
        print(event.manager.manager)
        if request.user != event.manager.manager:
            return HttpResponseForbidden("Access Denied")
        response = HttpResponse( content_type='text/csv' )
        response[ 'Content-Disposition' ] = f'attachment; filename="{event.title}.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                event.title,
                event.date,
                event.manager
            ]
        )
        writer.writerow(
            [ 
                'Email', 
                'First Name', 
                'Last Name', 
                'Gender', 
                'Phone', 
                'State', 
                'Birthday',
            ]
        )
        for person in event.registrants.all():
            try:
                profile = Profile.objects.get( user=person )
            except ObjectDoesNotExist:
                pass
            email = profile.user.email
            firstname = profile.first_name
            lastname = profile.last_name
            gender = profile.gender
            phone = profile.phone
            state = profile.state
            created = profile.profile_created.strftime("%c")
            birthday = profile.birthday.strftime("%d/%m/%Y")
            sport = []
            for s in profile.sport.all():
                sport.append(s.sport)
            
            writer.writerow(
                [ 
                    
                    email, 
                    firstname, 
                    lastname, 
                    gender, 
                    phone, 
                    state, 
                    birthday,
                ] 
            )

    return response

@verified_email_required
def data_view( request ):
    user = request.user
    name = getUserName( request )
    if user.is_superuser or user.is_staff:
        staff = True
        events = Events.objects.all() or None
        event_data = None
        all_data = None
        if request.POST:
            data_select = request.POST[ "data_select" ]
            if data_select == "all":
                all_data = UserProfile.objects.all() or None
            else:
                event_data = get_object_or_404( Events, pk=data_select )
    else:
        raise PermissionDenied
    context = {
        "name" : name,
        "staff" : staff,
        "events" : events,
        "all_data" : all_data,
        "event_data" : event_data,
    }
    return render( request, "data_view.html", context )
    
