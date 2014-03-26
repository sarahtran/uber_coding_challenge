from django.contrib import admin
from bike_parkings.models import BikeParking

class BikeParkingAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Location',                 {'fields': ['location', 'address']}),
    ('Geographical Coordinates', {'fields': ['latitude', 'longitude']}),
    ('Bike Parking Information', {'fields': ['bike_parking_type', 'placement', 'racks', 'spaces']}),
    ('Statuses',                 {'fields': ['status', 'status_high_level', 'status_detail', 'status_description']}),
    ('Additional Information',   {'fields': ['acting_agent', 'action', 'installed_by', 'year_installed']}),
  ]

  list_display = ('location', 'address', 'latitude', 'longitude',
                  'bike_parking_type', 'placement', 'racks', 'spaces',
                  'status', 'status_high_level', 'status_detail', 'status_description',
                  'acting_agent', 'action', 'installed_by', 'year_installed')

admin.site.register(BikeParking, BikeParkingAdmin)
