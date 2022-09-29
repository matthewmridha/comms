from django.contrib import admin
from profiles.models import Profile, Area, Sport
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class ProfileResource(resources.ModelResource):

    class Meta:
        model = Profile

class SportResource(resources.ModelResource):

    class Meta:
        model = Sport

class AreaResource(resources.ModelResource):

    class Meta:
        model = Area

class ProfileAdmin(ImportExportModelAdmin):

    resource_class = ProfileResource

class SportAdmin(ImportExportModelAdmin):

    resource_class = SportResource

class AreaAdmin(ImportExportModelAdmin):

    resource_class = AreaResource

      


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Sport, SportAdmin)