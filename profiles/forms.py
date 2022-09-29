from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, Area, Sport
from django.forms import widgets
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from allauth.account.forms import SignupForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, MultiField, Field, HTML
from crispy_forms.bootstrap import InlineRadios, PrependedText

class DateInput(forms.DateInput):
    input_type = "date"
    input_formats=('%d/%m/%Y')

class PhoneInput(forms.TextInput):
    input_type = "tel"

class ProfileForm( ModelForm ):

    class Meta:
        
        model = Profile
        fields = ( 
            "first_name",
            "last_name", 
            "gender", 
            "phone", 
            "birthday", 
            "state", 
            "city", 
            "country", 
            "sport",
            "communication"
        )
        widgets = {
            "sport" : forms.CheckboxSelectMultiple(),
            "gender" : forms.RadioSelect(),
            "phone" : PhoneInput(),
            "birthday" : DateInput(),
        }
        labels = {
            "sport" : "",
            "communication" : "I would like to receive online communications from Decathlon Dhaka"
        }
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field( "first_name" ),
            Field( "last_name" ),
            InlineRadios( "gender", required=True ),
            PrependedText("phone", "+88", active=True),
            Field( "birthday" ),
            Field( "state" ),
            Field( "city" ),
            Field( "country" ),
            HTML("""
            <label>Passion Sport (Select All That Apply)*</label>
        """),
            Field(Div("sport", css_class="form-sport form-group", required=True )),
            Field( "communication" ),
            Field(Div(Submit("submit", "Submit", css_class="btn btn-block btn-primary"), css_class="d-grid gap-2"))
            
        )
        

    def clean_first_name(self):
        return self.cleaned_data["first_name"].capitalize()

    def clean_last_name(self):
        return self.cleaned_data["last_name"].capitalize()

    def clean_city(self):
        return self.cleaned_data["city"].capitalize()

    def clean_country(self):
        return self.cleaned_data["country"].capitalize()





