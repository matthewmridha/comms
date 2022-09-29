from django.contrib import admin

# Register your models here.
from .models import Manager, Event, PaymentMethod, EventType


admin.site.register(Manager)
admin.site.register(Event)
admin.site.register(PaymentMethod)
admin.site.register(EventType)
