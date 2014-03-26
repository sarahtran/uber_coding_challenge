from django.test import TestCase
from django.core.urlresolvers import reverse

from bike_parkings.models import BikeParking
from bike_parkings.googlemaps import GeographicalCoordinates, Directions

class BikeParkingMethodTests(TestCase):

  def test_distance_to(self):
    """
    distance_to() should return the correct distance value
    """
    latitude  = 37.739009
    longitude = -122.467365
    bike_parking = BikeParking(latitude=37.77040275, longitude=-122.44512989)
    self.assertEqual(round(bike_parking.distance_to(latitude, longitude), 2), 2.49)

class BikeParkingIndexViewTests(TestCase):

  def test_index_view(self):
    """
    Index view should render index.html
    """
    response = self.client.get(reverse('bike_parkings:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Find the Nearest Bike Parking Locations in SF")

class BikeParkingNearestLocationsViewTests(TestCase):

  def test_nearest_locations_view_with_invalid_address(self):
    """
    Invalid address should cause a redirect back to the index view
    """
    response = self.client.get(reverse('bike_parkings:nearest_locations'), {
      'address': 'asdfjklllj'
    })
    self.assertEqual(response.status_code, 302)

  def test_nearest_locations_view_with_valid_address(self):
    """
    Valid address should render nearest_locations.html
    """
    response = self.client.get(reverse('bike_parkings:nearest_locations'), {
      'address': '576 Natoma St., San Francisco CA'
    })
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Nearest Bike Parking Locations in SF")
    self.assertQuerysetEqual(response.context['nearest_locations'], [])

  def test_nearest_locations_view_with_valid_address_and_nearest_locations(self):
    """
    Valid address should return the nearest five locations with the closest
    one first (source address is approximately at (37.8,-122.4))
    """
    bike_parking_1 = BikeParking.objects.create(location='Location 1', status='COMPLETE', latitude=37.8, longitude=-122.4)
    bike_parking_2 = BikeParking.objects.create(location='Location 2', status='COMPLETE', latitude=38.0, longitude=-122.0)
    bike_parking_3 = BikeParking.objects.create(location='Location 3', status='COMPLETE', latitude=39.0, longitude=-122.0)
    bike_parking_4 = BikeParking.objects.create(location='Location 4', status='COMPLETE', latitude=40.0, longitude=-122.0)
    bike_parking_5 = BikeParking.objects.create(location='Location 5', status='COMPLETE', latitude=41.0, longitude=-122.0)
    bike_parking_6 = BikeParking.objects.create(location='Location 6', status='COMPLETE', latitude=42.0, longitude=-122.0)
    response = self.client.get(reverse('bike_parkings:nearest_locations'), {
      'address': '576 Natoma St., San Francisco CA'
    })
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Nearest Bike Parking Locations in SF")
    self.assertQuerysetEqual(response.context['nearest_locations'], [
      '<BikeParking: Location 1>',
      '<BikeParking: Location 2>',
      '<BikeParking: Location 3>',
      '<BikeParking: Location 4>',
      '<BikeParking: Location 5>',
    ])

class BikeParkingDirectionsViewTests(TestCase):

  def test_directions_view_with_invalid_src_geo_coords(self):
    """
    Invalid src_geo_coords should cause a redirect back to the index view
    """
    response = self.client.get(reverse('bike_parkings:directions'), {
      'src_geo_coords': 'invalid_input',
      'dst_geo_coords': '37.7,-122.4'
    })
    self.assertEqual(response.status_code, 302)

  def test_directions_view_with_invalid_dst_geo_coords(self):
    """
    Invalid dst_geo_coords should cause a redirect back to the index view
    """
    response = self.client.get(reverse('bike_parkings:directions'), {
      'src_geo_coords': '37.7,-122.4',
      'dst_geo_coords': 'invalid_input'
    })
    self.assertEqual(response.status_code, 302)

  def test_directions_view_with_src_and_dst_geo_coords(self):
    """
    Valid src_geo_coords and dst_geo_coords should show directions
    """
    response = self.client.get(reverse('bike_parkings:directions'), {
      'src_geo_coords': '37.75,-122.4',
      'dst_geo_coords': '37.76,-122.4'
    })
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Start Address")
    self.assertContains(response, "Directions")
    self.assertContains(response, "End Address")
    self.assertContains(response, "Total Distance")

class GeographicalCoordinatesTests(TestCase):

  def test_geographical_coordinates_with_invalid_address(self):
    """
    GeographicalCoordinates that is passed an invalid address should not
    convert the address to geo coordinates and have an 'ERROR' status
    """
    invalid_address = "asdlfjladjkfld"
    geo_coords = GeographicalCoordinates(invalid_address)

    self.assertEqual(geo_coords.latitude, 0.0)
    self.assertEqual(geo_coords.longitude, 0.0)
    self.assertEqual(geo_coords.status, 'ERROR')

  def test_geographical_coordinates_with_valid_address(self):
    """
    GeographicalCoordinates that is passed a valid address should convert
    the address to corresponding geo coordinates and have an 'OK' status
    """
    valid_address = "576 Natoma St., San Francisco CA"
    geo_coords = GeographicalCoordinates(valid_address)

    self.assertNotEqual(geo_coords.latitude, 0.0)
    self.assertNotEqual(geo_coords.longitude, 0.0)
    self.assertEqual(geo_coords.status, 'OK')

class DirectionsTests(TestCase):

  def test_directions_with_invalid_src_geo_coords(self):
    """
    Directions that is passed an invalid src_geo_coords should not
    get the directions and have an 'ERROR' status
    """
    invalid_src_geo_coords = 'invalid_input'
    valid_dst_geo_coords = '37.76,-122.4'
    directions = Directions(invalid_src_geo_coords, valid_dst_geo_coords)

    self.assertEqual(directions.src_address, '')
    self.assertEqual(directions.dst_address, '')
    self.assertEqual(directions.distance, '')
    self.assertEqual(directions.steps, [])
    self.assertEqual(directions.status, 'ERROR')

  def test_directions_with_invalid_dst_geo_coords(self):
    """
    Directions that is passed an invalid dst_geo_coords should not
    get the directions and have an 'ERROR' status
    """
    valid_src_geo_coords = '37.75,-122.4'
    invalid_dst_geo_coords = 'invalid_input'
    directions = Directions(valid_src_geo_coords, invalid_dst_geo_coords)

    self.assertEqual(directions.src_address, '')
    self.assertEqual(directions.dst_address, '')
    self.assertEqual(directions.distance, '')
    self.assertEqual(directions.steps, [])
    self.assertEqual(directions.status, 'ERROR')

  def test_directions_with_valid_src_and_dst_geo_coords(self):
    """
    Directions that is passed valid src_geo_coords and valid dst_geo_coords
    should get the directions and have an 'OK' status
    """
    valid_src_geo_coords = '37.75,-122.4'
    valid_dst_geo_coords = '37.76,-122.4'
    directions = Directions(valid_src_geo_coords, valid_dst_geo_coords)

    self.assertNotEqual(directions.src_address, '')
    self.assertNotEqual(directions.dst_address, '')
    self.assertNotEqual(directions.distance, '')
    self.assertNotEqual(directions.steps, [])
    self.assertEqual(directions.status, 'OK')
