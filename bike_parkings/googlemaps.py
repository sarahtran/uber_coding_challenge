from httplib2 import Http
from urllib import urlencode
from json import loads

"""
An instance of this class takes in an address and requests the geographical
coordinates from the Google Maps Geocoding API.

Parameters:
* address - address string

Fields:
* address   - address that is updated with Google's formatted version
* latitude  - latitude in degrees from Google
* longitude - longitude in degrees from Google
* status    - 'OK' if geographical coordinates are available, else 'ERROR'
"""
class GeographicalCoordinates:
  def __init__(self, address):
    self.address   = address
    self.latitude  = 0.0
    self.longitude = 0.0
    self.status    = 'ERROR'
    self.get_geographical_coordinates(address)

  def get_geographical_coordinates(self, address):
    resp, content = self.request_geographical_coordinates_from_google(address)
    self.set_status(resp, content)
  
    if self.status == 'OK':
      self.set_geographical_coordinates(content)
  
  def request_geographical_coordinates_from_google(self, address):
    http = Http()
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    san_francisco_bounds = "37.6933354,-123.1077733|37.9297707,-122.3279149"
    data = urlencode({
      'address': address,
      'sensor' : 'false',
      'key'    : 'AIzaSyA5sGb_UnDFDOuIH6ohqpTs9QDW_nH7XAs',
      'bounds' : san_francisco_bounds,
    })
    resp, content = http.request(url + data, "GET")
    return resp, content

  def set_status(self, response, content):
    self.status = 'OK' if response['status'] == '200' and loads(content)['status'] == 'OK' else 'ERROR'
  
  def set_geographical_coordinates(self, content):
    result = loads(content)['results'][0]
    self.address = result['formatted_address']
    location = result['geometry']['location']
    self.latitude  = location['lat']
    self.longitude = location['lng']

"""
This class represents a step in the directions

Parameters/Fields:
* instruction - instruction for the step
* distance    - distance of the step in miles
"""
class Step:
  def __init__(self, instruction, distance):
    self.instruction = instruction
    self.distance = distance

"""
An instance of this class takes in source geographical coordinates and
destinatation geographical coordinates and requests the directions to
get from source to destination from the Google Maps Directions API.

Parameters:
* src_geo_coords - string of geographical coordinates ('latitude,longitude')
* dst_geo_coords - string of geographical coordinates ('latitude,longitude')

Fields:
* src_address - Google's directions start address
* dst_address - Google's directions end address
* distance    - miles between src_address and dst_address
* steps       - steps to get from src_address to dst_address
* status      - 'OK' if geographical coordinates are available, else 'ERROR'
"""
class Directions:
  def __init__(self, src_geo_coords, dst_geo_coords):
    self.src_address = ''
    self.dst_address = ''
    self.distance = ''
    self.steps = []
    self.status = 'ERROR'
    self.get_directions(src_geo_coords, dst_geo_coords)

  def get_directions(self, src_geo_coords, dst_geo_coords):
    resp, content = self.request_directions_from_google(src_geo_coords, dst_geo_coords)
    self.set_status(resp, content)
  
    if self.status == 'OK':
      self.set_directions(content)

  def request_directions_from_google(self, src_geo_coords, dst_geo_coords):
    http = Http()
    url = 'https://maps.googleapis.com/maps/api/directions/json?'
    data = urlencode({
      'origin'     : src_geo_coords,
      'destination': dst_geo_coords,
      'sensor'     : 'false',
      'key'        : 'AIzaSyA5sGb_UnDFDOuIH6ohqpTs9QDW_nH7XAs',
      'mode'       : 'bicycling',
    })
    resp, content = http.request(url + data, "GET")
    return resp, content
  
  def set_status(self, response, content):
    self.status = 'OK' if response['status'] == '200' and loads(content)['status'] == 'OK' else 'ERROR'

  def set_directions(self, content):
    route = loads(content)['routes'][0]['legs'][0]

    self.src_address = route['start_address']
    self.dst_address = route['end_address']
    self.distance = route['distance']['text']

    for step in route['steps']:
      self.steps.append(Step(step['html_instructions'], step['distance']['text']))
