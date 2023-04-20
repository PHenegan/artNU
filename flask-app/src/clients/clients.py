from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


clients = Blueprint('clients', __name__)

# Get the client information given their email address
@clients.route('/<email>', methods=['GET'])
def getClientFromEmail(email):
    cursor = db.get_db().cursor()

    query = "select firstName, lastName, email, clientID "
    query += " from Clients where email = {0}".format(email)

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

    query = "select orderID, Artists.firstName as artistFirstName, Artists.lastName as artistLastName, Artists.email as artistEmail, "
    query += "workStatus, startDate, finishDate, quote, paymentStatus, fileLocation name as commissionName, "
    query += "from Orders join CommissionTypes using (typeID) join Artists using (artistID)"


# Given the ID of an image, get the artest information from the image's creator
# NOTE: DOESN'T WORK YET
@clients.route('/images/<imageID>', methods=['GET'])
def getImageCreator(imageID):
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
