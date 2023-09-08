from django.contrib import admin
from .models import *


admin.site.site_header = 'Event Meetup'

# Register your models here.

class MeetupAdmin(admin.ModelAdmin):
    list_display = ('title','slug')
    list_filter = ('title',)
    prepopulated_fields = {'slug':('title',)}

admin.site.register(myUser)
admin.site.register(Meetup)
admin.site.register(Speaker)
admin.site.register(Participant)
admin.site.register(Location)
