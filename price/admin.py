from django.contrib import admin
from .models import Location

# Register your models here.

class LocationAdmin(admin.ModelAdmin):
    fields = ['name', 'code']

admin.site.register(Location, LocationAdmin)