from flask import Blueprint, request, jsonify, make_response
import json
from src import db


commission_types = Blueprint('commission_types', __name__)

# Get all the commission_types in the database
@commission_types.route('/', methods=['GET'])
def get_commission_types():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT C.name as commission_type, C.description as commission_desc, minPrice, maxPrice, L.name as license_name, I.title as image_title, I.location as image_location' + ' FROM CommissionTypes C join Licenses L using (licenseID) join DigitalImages DI on C.typeID = DI.typeID join ImageFiles I on DI.imageID = I.imageID')
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# Get a portfolio of the specified artist's commission types
@commission_types.route('/artist/<artistID>', methods=['GET'])
def get_artist_commission_images(artistID):
    cursor = db.get_db().cursor()
    # this line needs to be changed, not sure what exactly we want from the database based on the rest api matrix description
    cursor.execute('Select a.firstName as artist_first_name, a.lastName as artist_last_name, c.name as comm_types, description, minPrice, maxPrice, l.name as license_name' +
    ' from Artists as a join CommissionTypes as c using (artistID) join Licenses as l using (licenseID) '
    '+ where a.artistID = {0};'.format(artistID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response