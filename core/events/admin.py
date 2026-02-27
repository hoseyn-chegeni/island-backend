from django.contrib import admin
from .models import Event,EventType,Ticket
# Register your models here.


class EventAdmin(admin.ModelAdmin):
    # Define methods for properties to show them in the admin list
    def total_capacity(self, obj):
        return obj.total_capacity
    
    def duration(self, obj):
        return obj.duration

    # Optionally, you can make these methods read-only in the admin
    readonly_fields = ('total_capacity', 'duration')

admin.site.register(Event, EventAdmin)
admin.site.register(EventType)
admin.site.register(Ticket)