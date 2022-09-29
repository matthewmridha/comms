from django import forms
from django.forms import ModelForm
from .models import Event
from django.forms import widgets
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, MultiField, Field, HTML
from crispy_forms.bootstrap import InlineRadios, PrependedText


class DateInput(forms.DateInput):
    input_type = "date"

class TimeInput(forms.TimeInput):
    input_type = "time"

class EventCreationForm(ModelForm):
    class Meta:
        model = Event
        fields = [ 
            "event_type",
            "team_event",
            "min_team",
            "max_team", 
            "sport",
            "title",
            "description",
            "date",
            "time",
            "end_date",
            "end_time",
            "state",
            "city",
            "location",
            #"banner",
            "poster",
            "payment_required",
            "payment_methods",
            "payment_gateway",
            "payment_number",
            "payment_instruction",
            "price",
            "registration_open",
            "instruction",
            "facebook"
        ]
        widgets ={
            "date" : DateInput(),
            "time" : TimeInput(),
            "end_date": DateInput(),
            "end_time" : TimeInput()
        }
        labels = {
            "event_type" : "What type of event whill this be?",
            "team_event" : "Registering as Teams?",
            "min_team" : "minimum number of players in team",
            "max_team" : "maximum number of players in team",
            "sport" : "What sport are we playing?",
            "title" : "What will this event be called?",
            "description" : " Please describe this event.",
            "facebook" : "Facebook URL",
            "date" : "",
            "time" : "",
            "end_date" : "",
            "end_time" : "",
            "price" : "Price *(Leave empty if no reqistration fee is applicable)",
            "payment_required" : "Are users required to pay to register?",
            "payment_instruction" : "Payment Instructions *Incase of wallet Transfers, Registrants can make transfer and then send Transaction ID"
        }
    def __init__(self, *args, **kwargs):
        super(EventCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("title"),
            Field("event_type"),
            HTML('''<label>You can use Markdown to style the description and add images. <a href="https://codepen.io/matthewmridha/full/WqBKyZ" target="_blank">Click Here</a> To Preview your markdown in a markdown editor. <a href="https://www.markdownguide.org/basic-syntax/" target="_blank">Click here</a> to read how to write markdown.</label>'''),
            Field("description"),
            HTML('''<label>Output:</label>'''),
            Field("team_event"),
            Field(Div(Div("min_team", css_class="col"), Div("max_team", css_class="col"), css_class="row", id="team_number")),
            Field("sport"),
            HTML('''<label>When will this event start?</label>'''),
            Field(Div(Div("date", css_class="col"), Div("time", css_class="col"), css_class="row")),
            HTML('''<label>When will this event end?</label>'''),
            Field(Div(Div("end_date", css_class="col"), Div("end_time", css_class="col"), css_class="row")),
            Field("state"),
            Field("city"),
            Field("location"),
            Field("facebook"),
            #Field("banner"),
            Field("poster"),
            Field("price"),
            Field("payment_required"),
            Field("payment_methods"),
            Field("payment_gateway"),
            Field("payment_number"),
            Field("payment_instruction"),
            Field("registration_open"),
            Field("instruction"),
            Field(
                Div(Submit("submit", "Submit", css_class="btn btn-primary"), css_class="d-grid gap-2")
            )
        )
    def clean_title(self):
            return self.cleaned_data["title"].capitalize()

    def clean_city(self):
            return self.cleaned_data["city"].capitalize()

    def clean_country(self):
            return self.cleaned_data["country"].capitalize()

    