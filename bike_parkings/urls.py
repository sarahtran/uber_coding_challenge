from django.conf.urls import patterns, url

from bike_parkings import views

urlpatterns = patterns('',
  # ex: /bike_parkings/
  url(r'^$', views.index, name='index'),
  # ex: /bike_parkings/nearest_locations
  url(r'^nearest_locations$', views.nearest_locations, name='nearest_locations'),
  # ex: /bike_parkings/directions
  url(r'^directions$', views.directions, name='directions'),
)
