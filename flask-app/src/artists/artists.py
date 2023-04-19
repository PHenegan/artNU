from flask import Blueprint, request, jsonify, make_response
import json
from src import db


artists = Blueprint('artists', __name__)


# Get all artists from the db
@artists.route('/artists', methods=['GET'])
def get_artists():
    cursor = db.get_db().cursor()
    cursor.execute('select firstName, lastName, email from Artists')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add a new artist to the database
@artists.route('/', methods=['POST'])
def add_artist():
    # access json data from request object
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    artist_ID = req_data['artistID']
    artist_first = req_data['firstName']
    artist_last = req_data['lastName']
    artist_email = req_data['email']
    artist_bio = req_data['bio']
    artist_link1 = req_data['link1']
    artist_link2 = req_data['link2']
    artist_link3 = req_data['link3']
    artist_link4 = req_data['link4']
    artist_terms = req_data['termsofService']

    # insert statement
    insert = 'INSERT INTO Artists ("'
    insert += str(artist_ID) + ', "' + artist_first + '", "' + artist_last + '",' 
    + artist_email + '",' + artist_bio + '",' + artist_link1 + '",' + artist_link2 + '",' + artist_link3 + '",' 
    + artist_link4 + '",' + artist_terms + ')'

    current_app.logger.info(insert) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(insert)
    db.get_db().commit()
    return "Success"


# Get artist detail for artist with particular artistID
@artists.route('/<artistID>', methods=['GET'])
def get_specific_artist(artistID):
    query = 'select firstName, lastName, email, link1, link2, link3, link4, bio, CommissionTypes.name as commissionType, artistID '
    query += 'from Artists join CommissionTypes using (artistID) '
    query += 'where artistID = {0}'.format(artistID)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

def update_specific_artist(artistID):
    json_data = []

    cursor = db.get_db().cursor()
    cursor.execute(query)
    
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    response = make_response(jsonify(json_data))
    response.status_code = 200
    return response

# Get all the tags an artist refuses to do
@artists.route('/<artistID>/denylist', methods=['GET'])
def get_artistDeny(artistID):
    cursor = db.get_db().cursor()
    cursor.execute('select name from Deny_List join Tags using (tagID) where id = {0}'.format(artistID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all the commission types offered by a specific artist
@artists.route('/<artistID>/commission_types', methods=['GET'])
def get_artistCommissions(artistID):
    cursor = db.get_db().cursor()
    cursor.execute('select name, description from Artists join CommissionTypes using (tagID) where id = {0}'.format(artistID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all the specified artist's ongoing orders
@artists.route('/<artistID>/orders', methods=['GET'])
def get_artistOrders(artistID):
    cursor = db.get_db().cursor()
    cursor.execute('select name, description from Artists join CommissionTypes using (tagID) where id = {0}'.format(artistID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response