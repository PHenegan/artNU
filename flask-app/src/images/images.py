from flask import Blueprint, request, jsonify, make_response
import json
from src import db


images = Blueprint('images', __name__)

# Get all the images in the database
@images.route('/images', methods=['GET'])
def get_images():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT imageID, description, typeID, isExplicit FROM DigitalImages')
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

# Get a portfolio of the specified artist's uploaded images
@images.route('/images/artist/<artistID>', methods=['GET'])
def get_images_artist(artistID):
    cursor = db.get_db().cursor()
    # this line needs to be changed, not sure what exactly we want from the database based on the rest api matrix description
    cursor.execute('select * from Artists join CommissionTypes using (artistID) join DigitalImages using (typeID) where id = {0}'.format(artistID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all examples of a specified commission tag
@images.route('/images/tags/<tagID>', methods=['GET'])
def get_images_tag(tagID):
    cursor = db.get_db().cursor()
    # this line needs to be changed, not sure what exactly we want from the database based on the rest api matrix description
    cursor.execute('select imageID, description from DigitalImages join CommissionTypes using (typeID) join Comm_Tag using (typeID)' 
                   + ' join Tags using (tagID) where id = {0}'.format(tagID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
