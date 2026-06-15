from django.contrib import admin
import travelmate.models as models

# Register your models here.

admin.site.register(models.Destination)
admin.site.register(models.TouristPlace)
admin.site.register(models.Restaurant)
admin.site.register(models.Hotel)
admin.site.register(models.Contact)
admin.site.register(models.Package)
admin.site.register(models.Booking)
