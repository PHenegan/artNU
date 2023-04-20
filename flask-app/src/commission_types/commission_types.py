from flask import Blueprint, request, jsonify, make_response, current_app
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

# Get a portfolio of the specified artist's images
@commission_types.route('/artist/<artistID>', methods=['GET'])
def get_artist_commission_images(artistID):
    cursor = db.get_db().cursor()
    cursor.execute('Select I.location'
 + ' from Artists as a join CommissionTypes as c using (artistID) join DigitalImages DI on c.typeID = DI.typeID join ImageFiles I on DI.imageID = I.imageID'
 + ' where a.artistID = {};'.format(artistID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all commission types of a specified commission tag
@commission_types.route('/tags/<tagName>', methods=['GET'])
def get_commission_tags(tagName):
    cursor = db.get_db().cursor
    cursor.execute('Select T.tagName, A.firstName as artist_first_name, A.lastName as artist_last_name, C.name as commission_type, minPrice' 
                   + ' From CommissionTypes C join Comm_Tag CT on C.typeID = CT.typeID join Tags T on CT.tagName = T.tagName join Artists A on C.artistID = A.artistID'
                   + ' where T.tagName = {0}'.format(tagName))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add a new commission type to a tag
@commission_types.route('/tag/<tagName>', methods=['POST'])
def add_image(tagName):
    req_data = request.get_json

    #commission type ID
    typeID = req_data['typeID']

    # insert statement
    insert = 'INSERT INTO Comm_Tag ({0}, {1})'.format(typeID, tagName) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(insert)
    db.get_db().commit()
    return "Success"

# Remove a tag from a commission type
@commission_types.route('/tag/<tagName>', methods=['DELETE'])
def delete_image(tagName):
    req_data = request.get_json

    #commission type ID
    typeID = req_data['typeID']

    cursor = db.get_db().cursor()
    cursor.execute('DELETE from Comm_Tag where typeID={0} and tagName={1}'.format(typeID, tagName))
    db.get_db().commit()
    return "Success"