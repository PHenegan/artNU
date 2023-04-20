from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


artists = Blueprint('artists', __name__)


# Get all artists from the db
@artists.route('/', methods=['GET'])
def get_artists():
    cursor = db.get_db().cursor()
    cursor.execute('select firstName, lastName, email, bio from Artists')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get a portfolio of the specified artist's commission types
@artists.route('/<artistID>/commission_types', methods=['GET'])
def get_artist_commission_types(artistID):
    cursor = db.get_db().cursor()
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
    first = req_data['firstName']
    last = req_data['lastName']
    email = req_data['email']
    bio = req_data['bio']
    link1 = req_data['link1']
    link2 = req_data['link2']
    link3 = req_data['link3']
    link4 = req_data['link4']
    terms = req_data['termsofService']

    query = 'update Artists '
    query += 'set firstName = \'{0}\', lastName = \'{1}\', email = \'{2}\', '.format(first, last, email)
    query += 'bio = \'{0}\', link1 = \'{1}\', link2 = \'{2}\', link3 = \'{3}\', link4 = \'{4}\''.format(bio, link1, link2, link3, link4)
    query += 'termsOfService = \'{0}\', '.format(terms)
    query += 'where artistID = {0}'.format(artistID)

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
    cursor.execute('select name from Deny_List join Tags using (tagName) where artistID = {0}'.format(artistID))
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
    cursor.execute('select name, description from Artists join CommissionTypes using (tagName) where artistID = {0}'.format(artistID))
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
    cursor.execute('select name, CT.description, workStatus from Artists A join CommissionTypes CT on A.artistID = CT.artistID join Orders O on CT.typeID = O.typeID where A.artistID = {0} AND workStatus = \'in-progress\''.format(artistID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all the specified artist's tags they will work with and the associated commission
@artists.route('/<artistID>/comm_tag', methods=['GET'])
def get_artistTags(artistID):
    cursor = db.get_db().cursor()
    cursor.execute('select T.name tag_name, C.name comm_name, C.description from Artists join CommissionTypes C using (artistID) join Comm_Tag CT on C.typeID = CT.typeID join Tags T on CT.tagName = T.tagName where artistID = {0}'.format(artistID))
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
@artists.route('/<artistID>/comm_tag', methods=['POST'])
def add_comm_tag(tagName):
    req_data = request.get_json

    #commission type ID
    typeID = req_data['typeID']
    tagName = req_data['tagName']

    # insert statement
    insert = 'INSERT INTO Comm_Tag ({0}, {1})'.format(typeID, tagName) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(insert)
    db.get_db().commit()
    return "Success"