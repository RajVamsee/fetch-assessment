#import statements
from flask import Flask 
from flask import request, jsonify
import uuid #this is for generating unique ids for receipts
import re

#Create a Flask application instance which will act as our server 
app = Flask(__name__)

#Our in-memory storage for receipts
receipts_details = dict()

#Defining the routes for our receipt processor
#our home page on opening on any browser
@app.route('/')
def home():
    return "Receipt Processor Application"

#API to submit the receipt (POST)
@app.route('/receipts/process', methods=['POST'])
def receipt_processor():
    """ accepts a json receipt, 
    generates a unique receipt id, 
    stores receipt details, 
    returns id  """

    receipt = request.get_json() #receive json receipt data
    
    if not receipt:
        return jsonify({"error":"Invalid Receipt JSON"}), 400
    
    receipt_id = str(uuid.uuid4()) #Generate a unique id
    receipts_details[receipt_id] = receipt #Store the receipt in memory
    return jsonify({"id": receipt_id}), 200

#function/method to write the logic to follow rules for awarding points for a particular receipt
def points_calculator(receipt):
    points = 0

    #Rule 1 : One point for every alphanumeric character in the retailer name.
    retailerName = receipt.get("retailer","")
    pattern = re.sub(r'[^a-zA-Z0-9]', '', retailerName)
    points += len(pattern)

    #Rule 2 : 50 points if the total is a round dollar amount with no cents.
    amount = float(receipt.get("total","0"))
    if amount.is_integer():
        points += 50
    
    return points


#API to return points for a receipt (GET)
@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    """ Accepts receipt ID, 
    returns points earned for that receipt """

    if id in receipts_details:
        #temporarily returning 20 points till I come up with logic for all the rules
        #return jsonify({"points": 20}), 200 

        points = points_calculator(receipts_details[id]) #awarding points based on rules
        return jsonify({"points": points}), 200
    
    return jsonify({"error":"Receipt not found"}), 404

#This is to run our receipt processor App
if __name__ == '__main__':
    app.run(debug=True)