import math
from django.db import models

class BikeParking(models.Model):
  location           = models.CharField(max_length=255)
  address            = models.CharField(max_length=255)
  bike_parking_type  = models.CharField(max_length=50)
  placement          = models.CharField(max_length=50)
  racks              = models.IntegerField(default=0)
  spaces             = models.IntegerField(default=0)
  status             = models.CharField(max_length=50)
  status_high_level  = models.CharField(max_length=50)
  status_detail      = models.CharField(max_length=50)
  status_description = models.CharField(max_length=255)
  acting_agent       = models.CharField(max_length=50)
  action             = models.CharField(max_length=50)
  installed_by       = models.CharField(max_length=50)
  year_installed     = models.CharField(max_length=50)
  latitude           = models.DecimalField(max_digits=15, decimal_places=10)
  longitude          = models.DecimalField(max_digits=15, decimal_places=10)

  def __unicode__(self):
    return self.location

  """
  Returns the distance in miles between the geographical coordinates of the
  bike parking and the geographical coordinates of the given parameters
  """
  def distance_to(self, latitude, longitude):
    # conversion of geographical coordinates into radian values
    lat1 = math.radians(self.latitude)
    long1 = math.radians(self.longitude)
    lat2 = math.radians(latitude)
    long2 = math.radians(longitude)

    # radius of the equator in miles
    radius_of_equator = 3963.191

    # distance calculation in miles
    distance = math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(long2 - long1)) * radius_of_equator

    return distance
