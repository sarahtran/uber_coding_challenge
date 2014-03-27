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
  _address   = ''
  _latitude  = 0.0
  _longitude = 0.0
  _status    = 'ERROR'

  def __init__(self, address):
    self._get_geographical_coordinates(address)

  @property
  def address(self):
    return self._address

  @property
  def latitude(self):
    return self._latitude

  @property
  def longitude(self):
    return self._longitude

  @property
  def status(self):
    return self._status

  def to_JSON(self):
    return self.__dict__

  def _get_geographical_coordinates(self, address):
    resp, content = self._request_geographical_coordinates_from_google(address)
    self._set_status(resp, content)
  
    if self._status == 'OK':
      self._set_geographical_coordinates(content)
  
  def _request_geographical_coordinates_from_google(self, address):
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

  def _set_status(self, response, content):
    self._status = 'OK' if response['status'] == '200' and loads(content)['status'] == 'OK' else 'ERROR'
  
  def _set_geographical_coordinates(self, content):
    result = loads(content)['results'][0]
    self._address = result['formatted_address']
    location = result['geometry']['location']
    self._latitude  = location['lat']
    self._longitude = location['lng']

"""
This class represents a step in the directions

Parameters/Fields:
* instruction - instruction for the step
* distance    - distance of the step in miles
"""
class Step:
  _instruction = ''
  _distance = ''

  def __init__(self, instruction, distance):
    self._instruction = instruction
    self._distance = distance

  @property
  def instruction(self):
    return self._instruction

  @property
  def distance(self):
    return self._distance

  def to_JSON(self):
    return self.__dict__

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
  _src_address = ''
  _dst_address = ''
  _distance = ''
  _steps = []
  _status = 'ERROR'

  def __init__(self, src_geo_coords, dst_geo_coords):
    self._get_directions(src_geo_coords, dst_geo_coords)

  @property
  def src_address(self):
    return self._src_address

  @property
  def dst_address(self):
    return self._dst_address

  @property
  def distance(self):
    return self._distance

  @property
  def steps(self):
    return self._steps

  @property
  def status(self):
    return self._status

  def to_JSON(self):
    return self.__dict__

  def _get_directions(self, src_geo_coords, dst_geo_coords):
    resp, content = self._request_directions_from_google(src_geo_coords, dst_geo_coords)
    self._set_status(resp, content)
  
    if self._status == 'OK':
      self._set_directions(content)

  def _request_directions_from_google(self, src_geo_coords, dst_geo_coords):
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
  
  def _set_status(self, response, content):
    self._status = 'OK' if response['status'] == '200' and loads(content)['status'] == 'OK' else 'ERROR'

  def _set_directions(self, content):
    route = loads(content)['routes'][0]['legs'][0]

    self._src_address = route['start_address']
    self._dst_address = route['end_address']
    self._distance = route['distance']['text']
    self._steps = [Step(step['html_instructions'], step['distance']['text']) for step in route['steps']]
