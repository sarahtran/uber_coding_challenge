from django.shortcuts import render, redirect
from bike_parkings.models import BikeParking
from bike_parkings.googlemaps import GeographicalCoordinates, Directions

"""
Renders a view where the client can submit an address
"""
def index(request):
  return render(request, 'bike_parkings/index.html')

"""
Renders a view with the 5 nearest bike parking locations to the address,
else redirects to index with error message

Object Fields:
* geographical_coordinates:
  - Address
  - Latitude
  - Longitude
* nearest_locations:
  - [Bike Parking Objects]
"""
def nearest_locations(request):
  address = request.GET['address']
  geographical_coordinates = GeographicalCoordinates(address)

  if geographical_coordinates.status != 'OK':
    return redirect('/bike_parkings')

  nearest_locations = sorted(BikeParking.objects.filter(status="COMPLETE"), key=lambda bike_parking: bike_parking.distance_to(geographical_coordinates.latitude, geographical_coordinates.longitude))[:5]

  return render(request, 'bike_parkings/nearest_locations.html', {
    'geographical_coordinates': geographical_coordinates,
    'nearest_locations'       : nearest_locations,
  })

"""
Renders a view with the directions from the address to the selected nearest
bike parking location, else renders index with error message

Object Fields:
* directions:
  - src_address
  - dst_address
  - distance
  - steps
  - status
"""
def directions(request):
  src_geo_coords = request.GET['src_geo_coords']
  dst_geo_coords = request.GET['dst_geo_coords']
  directions = Directions(src_geo_coords, dst_geo_coords)

  if directions.status != 'OK':
    return redirect('/bike_parkings')

  return render(request, 'bike_parkings/directions.html', {
    'directions'  : directions,
  })
