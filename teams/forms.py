from django import forms
from django.forms import ModelForm
from .models import Team

class TeamBuildingForm(ModelForm):
     class Meta:
        model = Team
        fields = (
            "logo",
            "name",
            "description",
            "sport",
            "password",
        )
        def clean_name(self):
            return self.cleaned_data["name"].capitalize()