# Full path and name to csv file
csv_filepathname = "/app/bike_parkings/scripts/Bicycle_Parking__Public_.csv"
# Full path to django project directory
djangoproject_home = "/app"

import sys, os
sys.path.append(djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'uber_coding_challenge.settings'

from bike_parkings.models import BikeParking

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

for row in dataReader:
  # Ignore the header row, and import everything else
  if row[0] != 'LOCATION':
    bike_parking = BikeParking()
    bike_parking.location           = row[0]
    bike_parking.address            = row[1] if row[1] == 'None' else row[1].lower().title() + ", San Francisco CA"
    bike_parking.bike_parking_type  = row[2]
    bike_parking.placement          = row[3]
    bike_parking.racks              = 0 if row[4] == '' else int(row[4])
    bike_parking.spaces             = 0 if row[5] == '' else int(row[5])
    bike_parking.status             = row[6]
    bike_parking.status_high_level  = row[7]
    bike_parking.status_detail      = row[8]
    bike_parking.status_description = row[9]
    bike_parking.acting_agent       = row[10]
    bike_parking.action             = row[11]
    bike_parking.installed_by       = row[12]
    bike_parking.year_installed     = row[13]

    geographical_coordinates = row[14].strip("()").split(",")
    bike_parking.latitude  = geographical_coordinates[0]
    bike_parking.longitude = geographical_coordinates[1]

    bike_parking.save()
