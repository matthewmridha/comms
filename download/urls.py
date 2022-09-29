from django.urls import path, include
from . import views

urlpatterns = [
    path( "", views.data_view, name="data_view" ),
    path( "download_data/<int:event_id>", views.download, name="download_data" ),
    
]