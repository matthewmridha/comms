from django.urls import path

from . import views

urlpatterns = [
    path( "", views.profileView, name="profileView" ),
    path( "edit_profile", views.edit_profile, name="edit_profile" ),
]