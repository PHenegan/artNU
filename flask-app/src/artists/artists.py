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

# Get artist detail for artist with particular artistID
@artists.route('/<artistID>', methods=['GET'])
def get_specific_artist(artistID):
    query = 'select firstName, lastName, email, link1, link2, link3, link4, bio '
    query += 'from Artists '
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

# Get all the tags an artist refuses to do
@artists.route('/<artistID>/denylist', methods=['GET'])
def get_artistDeny(artistID):
    cursor = db.get_db().cursor()
    cursor.execute('select distinct DL.tagName from Artists A join Deny_List DL on A.artistID = DL.artistID where A.artistID = {0}'.format(artistID))
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
    cursor.execute('Select a.lastName as artist_last_name, c.name as comm_types, description, minPrice, maxPrice, l.name as license_name' +
    ' from Artists as a join CommissionTypes as c using (artistID) join Licenses as l using (licenseID)' +
    ' where a.artistID = {0}'.format(artistID))
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

# Get all the specified artist's tags they will work with and the associated commissions
@artists.route('/<artistID>/comm_tag', methods=['GET'])
def get_artistTags(artistID):
    cursor = db.get_db().cursor()
    cursor.execute('select CT.tagName, C.name commName from Artists A join CommissionTypes C using (artistID) join Comm_Tag CT on C.typeID = CT.typeID where artistID = {0}'.format(artistID))
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

    artist_first = req_data['firstName']
    artist_last = req_data['lastName']
    artist_email = req_data['email']
    artist_bio = req_data['bio']
    artist_link1 = req_data['link1']
    artist_link2 = req_data['link2']
    artist_link3 = req_data['link3']
    artist_link4 = req_data['link4']
    artist_terms = req_data['termsOfService']

    # insert statement
    insert = 'INSERT INTO Artists(firstName, lastName, email, bio, link1, link2, link3, link4, termsOfService) Values(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\')'.format(artist_first, artist_last, artist_email, artist_bio, artist_link1, artist_link2, artist_link3, artist_link4, artist_terms);

    current_app.logger.info(insert) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(insert)
    db.get_db().commit()
    return "Success"

# Add a new commission_type to the database
@artists.route('/<artistID>/commission_types', methods=['POST'])
def add_commission_type(artistID):
    # access json data from request object
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    name = req_data['name']
    description = req_data['description']
    minPrice = req_data['minPrice']
    maxPrice = req_data['maxPrice']
    licenseID = req_data['licenseID']

    # insert statement
    insert = 'INSERT INTO CommissionTypes(name, description, minPrice, maxPrice, licenseID, artistID) Values(\'{0}\', \'{1}\', {2}, {3}, {4}, {5});'.format(name, description, minPrice, maxPrice, licenseID, artistID)

    current_app.logger.info(insert) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(insert)
    db.get_db().commit()
    return "Success"

# Add an order to an artist commission list
@artists.route('/<artistID>/orders', methods=['POST'])
def add_orders(artistID):
    # access json data from request object
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    description = req_data['description']
    quote = req_data['quote']
    paymentStatus = req_data['paymentStatus']
    typeName = req_data['typeName']
    clientID = req_data['clientID']

    # insert statement
    insert = 'INSERT INTO Orders(workStatus, description, quote, paymentStatus, typeID, clientID) Values(\'pending\', \'{0}\', \'{1}\', \'{2}\', (SELECT CT.typeID from CommissionTypes CT join Artists A using (artistID) where A.artistID = {3} and CT.name = \'{4}\'), {5});'.format(description, quote, paymentStatus, artistID, typeName, clientID)

    current_app.logger.info(insert) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(insert)
    db.get_db().commit()
    return "Success"

# Add a tag to a commission type
@artists.route('/<artistID>/comm_tag', methods=['POST'])
def add_comm_tag(artistID):
    # access json data from request object
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    typeID = req_data['typeID']
    tagName = req_data['tagName']
    tagType = req_data['type']

    # insert statement
    insert = 'INSERT IGNORE INTO Tags(tagName, type) Value(\'{0\'}, {1})'
    + 'INSERT INTO Comm_Tag(typeID, tagName) Values({2}, \'{0\'})'.format(tagName, tagType, typeID)

    current_app.logger.info(insert) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(insert)
    db.get_db().commit()
    return "Success"

# Add a tag to the deny list
@artists.route('/<artistID>/denylist', methods=['POST'])
def add_denylist(artistID):
    # access json data from request object
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    tagName = req_data['tagName']
    tagType = req_data['type']

    # insert statement
    insert = 'INSERT IGNORE INTO Tags(tagName, type) Value(\'{0\'}, {1})'
    + 'INSERT INTO Deny_List(artistID, tagName) Values({2}, \'{0\'})'.format(tagName, tagType, artistID)

    current_app.logger.info(insert) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(insert)
    db.get_db().commit()
    return "Success"

@artists.route('/<artistID>', methods=['PUT'])
def update_specific_artist(artistID):
    # access json data from request object
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

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
    query += 'bio = \'{0}\', link1 = \'{1}\', link2 = \'{2}\', link3 = \'{3}\', link4 = \'{4}\', '.format(bio, link1, link2, link3, link4)
    query += 'termsOfService = \'{0}\' '.format(terms)
    query += 'where artistID = {0};'.format(artistID)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))

    response = make_response(jsonify(json_data))
    response.status_code = 200
    return response

# Update an order in an artist commission list
@artists.route('/<artistID>/orders', methods=['PUT'])
def update_orders(artistID):
    # access json data from request object
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    workStatus = req_data['workStatus']
    startDate = req_data['startDate']
    finishDate = req_data['finishDate']
    quote = req_data['quote']
    paymentStatus = req_data['paymentStatus']
    orderFileLocation = req_data['orderFileLocation']
    orderID = req_data['orderID']

    # query statement
    query = 'UPDATE Orders SET workStatus = \'{0}\', startDate = Date(\'{1}\'), finishDate = Date(\'{2}\'), '.format(workStatus, startDate, finishDate)
    query += 'quote = {0}, paymentStatus = \'{1}\', orderFileLocation = \'{2}\' where orderID = {3};'.format(quote, paymentStatus, orderFileLocation, orderID)

    current_app.logger.info(query) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return "Success"

# Delete this artist profile
@artists.route('/<artistID>', methods=['DELETE'])
def delete_artist(artistID):

    # query statement
    query = 'DELETE from Artists where artistID = {}'.format(artistID)

    current_app.logger.info(query) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return "Success"

# Delete a certain commission type
@artists.route('/<artistID>/commission_type', methods=['DELETE'])
def delete_commission_type(artistID):
    # access json data from request object
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    typeID = req_data['typeID']

    # query statement
    query = 'DELETE from CommissionType where typeID = {}'.format(typeID)

    current_app.logger.info(query) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return "Success"

# Delete a tag from a certain commission
@artists.route('/<artistID>/comm_tag', methods=['DELETE'])
def delete_comm_tag(artistID):
    # access json data from request object
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    typeID = req_data['typeID']
    tagName = req_data['tagName']
    # query statement
    query = 'DELETE from Comm_Tag where typeID = {} and tagName = {}'.format(typeID, tagName)

    current_app.logger.info(query) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return "Success"

# Delete a tag from a denyList
@artists.route('/<artistID>/denylist', methods=['DELETE'])
def delete_denylist_tag(artistID):
    # access json data from request object
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    typeID = req_data['typeID']
    # query statement
    query = 'DELETE from Deny_List where typeID = {} and artistID = {}'.format(typeID, artistID)

    current_app.logger.info(query) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return "Success"

# Delete an order
@artists.route('/<artistID>/orders', methods=['DELETE'])
def delete_orders(artistID):
    # access json data from request object
    current_app.logger.info('Processing form data')
    req_data = request.get_json()
    current_app.logger.info(req_data)

    orderID = req_data['orderID']

    # query statement
    query = 'DELETE from Orders where orderID = {} and artistID = {}'.format(orderID, artistID)

    current_app.logger.info(query) 

    # execute query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return "Success"
