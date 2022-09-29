from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
     path("<int:event_id>", views.event, name="event"),
    path("<int:event_id>/register", views.register, name="register"),
    path("<int:event_id>/register_team", views.register_team, name="register_team"),
    path("<int:event_id>/unregister", views.unregister, name="unregister"),
    path("<int:event_id>,<int:team_id>/unregister_team", views.unregister_team, name="unregister_team" ),
    path("<int:event_id>/register_paid", views.register_paid, name="register_paid"),
    path("create_event", views.create_event, name="create_event" ),
    path("host", views.host, name="host"),
    path("<int:event_id>/view_event_data", views.view_event_data, name="view_event_data"),
    path( "delete_event/<int:event_id>", views.delete_event, name="delete_event" ),
    path( "edit_event/<int:event_id>", views.edit_event, name="edit_event" ),
]