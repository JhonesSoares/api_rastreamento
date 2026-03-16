from django.contrib import admin

from .models import Location, User, Vehicle

admin.site.register(User)
admin.site.register(Vehicle)
admin.site.register(Location)
