from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


clients = Blueprint('clients', __name__)

# Get the client information given their email address
@clients.route('/email/<email>', methods=['GET'])
def getClientFromEmail(email):
    cursor = db.get_db().cursor()

    query = "select firstName, lastName, email, clientID "
    query += " from Clients where email = \'{0}\'".format(email)

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

# Update information for the client with the given ID
@clients.route('/<clientID>', methods=['PUT'])
def updateClientInfo(clientID):
    cursor = db.get_db().cursor()

    req_data = request.get_json()
    firstName = req_data["firstName"]
    lastName = req_data["lastName"]
    email = req_data["email"]

    update = "update Clients "
    update += "set firstName=\'{0}\', lastName=\'{1}\', email=\'{2}\' ".format(firstName, lastName, email)
    update += "where clientID = {0}".format(clientID)

    cursor = db.get_db().cursor()
    cursor.execute(update)
    db.get_db().commit()
    return "Success"

@clients.route('/<clientID>/orders', methods=['GET'])
def getClientOrders(clientID):
    cursor = db.get_db().cursor()

    query = "select orderID, Artists.firstName as artistFirstName, Artists.lastName as artistLastName, "
    query += "Artists.email as artistEmail,workStatus, startDate, finishDate, quote, paymentStatus, "
    query += "orderFileLocation, name as commissionName from Orders join CommissionTypes using (typeID) join Artists using (artistID) "
    query += "where clientID = {0}".format(clientID)

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

@clients.route('/orders/<orderID>', methods=['DELETE'])
def cancelOrder(orderID):
    cursor = db.get_db().cursor()
    cursor.execute("delete from Orders where orderID = {0}".format(orderID))
    db.get_db().commit()
    return "Success"

@clients.route('/orders', methods=['POST'])
def makeOrder():
    req_data = request.get_json()
    current_app.logger.info("Request data: ")
    current_app.logger.info(req_data)

    clientId = req_data['clientID']
    quote = req_data['quote']
    description = req_data['description']
    typeID = req_data['typeID']
    finishDate = req_data['finishDate']
    
    cursor = db.get_db().cursor()

    orderInsert = "insert into Orders(clientID, quote, description, typeID, finishDate) "
    orderInsert += "values('{0}',{1}, '{2}', {3}, '{4}')".format(clientId, quote, description, typeID, finishDate)
    cursor.execute(orderInsert)

    streetAddr = req_data['streetAddr']
    city = req_data['city']
    state = req_data['state']
    country = req_data['country']
    zipCode = req_data['zipCode']

    detailsInsert = "insert into OrderDetails(streetAddr, city, state, country, zipCode, orderID)"
    detailsInsert += "values('{0}', '{1}', '{2}', '{3}', '{4}', LAST_INSERT_ID())".format(streetAddr, city, state, country, zipCode)
    cursor.execute(detailsInsert)
    
    db.get_db().commit()
    return "Success"

# Given the ID of an image, get the artist information from the image's creator
# NOTE: DOESN'T WORK YET
@clients.route('/images/<imageID>', methods=['GET'])
def getImageCreator(imageID):
    cursor = db.get_db().cursor()

    query = "select firstName, lastName, email, bio, artistID from Artists"
    query += "join CommissionTypes using (artistID) join DigitalImages using (typeID)"
    query += "where imageID = {0}".format(imageID)

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

@clients.route('/commissions/<tag>/<minPrice>/<maxPrice>', methods = ['GET'])
def getSearchImages(tag, minPrice, maxPrice):
    cursor = db.get_db().cursor()
    query = "select distinct imageID, location, title, minPrice, maxPrice, firstName, lastName, artistID, email "
    query += "from Artists join CommissionTypes using (artistID) join DigitalImages using (typeID) " 
    query += "join ImageFiles using (imageID) join Comm_Tag using (typeID) "
    query += "where tagName = '{0}' and minPrice > {1} and maxPrice < {2}".format(tag)

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

