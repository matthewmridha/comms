from django.urls import path, include
from . import views

urlpatterns = [
    path( "", views.teams, name="teams" ),
    path( "team_builder", views.team_builder, name="team_builder" ),
    path( "<int:team_id>/team_view", views.team_view, name="team_view" ),
    path( "leave_team/<int:team_id>", views.leave_team, name="leave_team" ),
    path( "join_team/<int:team_id>", views.join_team, name="join_team" )
]

