#import statements
from flask import Flask 
from flask import request, jsonify 
import uuid #this is for generating unique ids for receipts
import re #for regex patterns
import math #for rounding up
from datetime import datetime
from uuid import UUID

#Create a Flask application instance which will act as our server 
app = Flask(__name__)

#Our in-memory storage for receipts (python dictionary for key value pairs)
receipts_details = dict()

#function to validate our unique id
def validate_id(token):
    try:
        UUID(token, version=4)
        return True
    except ValueError:
        return False

#Defining the routes for our receipt processor
#our home page on opening on any browser
@app.route('/')
def home():
    return "Receipt Processor Application"

#API to submit and process the receipt (POST)
@app.route('/receipts/process', methods=['POST'])
def receipt_processor():
    """ accepts a json receipt, 
    generates a unique receipt id, 
    stores receipt details, 
    returns id  """

    receipt = request.get_json() #receive json receipt data
    
    if not receipt:
        return jsonify({"error":"The receipt is invalid."}), 400
    
    #validation for all required fields
    required = ["retailer","purchaseDate","purchaseTime","items","total"]
    missing = [item for item in required if item not in receipt]
    if missing:
        return jsonify({"error":"The receipt is invalid."}), 400
    
    #validation for purchaseDate: YYYY-MM-DD
    try:
        datetime.strptime(receipt["purchaseDate"], "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "The receipt is invalid."}), 400
    
    #validation for purchaseTime: HH:MM (24hr format)
    try:
        datetime.strptime(receipt["purchaseTime"], "%H:%M")
    except ValueError:
        return jsonify({"error": "The receipt is invalid."}), 400
    
    #validation for total amount: 
    if not re.match(r"^\d+\.\d{2}$", receipt["total"]):
        return jsonify({"error": "The receipt is invalid."}), 400
    
    #validation for items:
    if not isinstance(receipt["items"], list) or len(receipt["items"]) == 0:
        return jsonify({"error": "The receipt is invalid."}), 400
    
    # Validation for every item in the item list:
    for item in receipt["items"]:
        if "shortDescription" not in item or "price" not in item:
            return jsonify({"error": "The receipt is invalid."}), 400
        if not isinstance(item["shortDescription"], str) or not item["shortDescription"].strip():
            return jsonify({"error": "The receipt is invalid."}), 400
        if not re.match(r"^\d+\.\d{2}$", item["price"]):
            return jsonify({"error": "The receipt is invalid."}), 400
    
    receipt_id = str(uuid.uuid4()) #Generate a unique id
    receipts_details[receipt_id] = receipt #Store the receipt in memory
    return jsonify({"id": receipt_id}), 200

#function to write the logic to follow rules for awarding points for a particular receipt
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
    
    #Rule 3 : 25 points if the total is a multiple of 0.25.
    if amount % 0.25 == 0:
        points +=25
    
    #Rule 4 : 5 points for every two items on the receipt.
    items = receipt.get("items", [])
    two_item_count = (len(items) // 2)
    points += (two_item_count * 5)

    """Rule 5 : If the trimmed length of the item description is a multiple of 3, 
    multiply the price by 0.2 and round up to the nearest integer. 
    The result is the number of points earned."""
    for item in items:
        trimmed = item.get("shortDescription","").strip() #trimming the whitespaces
        price = float(item.get("price","0"))
        if len(trimmed) % 3 == 0:
            points += math.ceil(price * 0.2) #used ceil since we are asked to round "up"
    
    #Rule 6 : 6 points if the day in the purchase date is odd.
    date = receipt.get("purchaseDate","")
    if date: 
        day = int(date.split("-")[-1]) #extract the day from YYYY-MM-DD format 
        if day % 2 == 1: #checking the odd day condition
            points += 6 
    
    #Rule 7 : 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    time = receipt.get("purchaseTime", "")
    if time:
        hr, min = map(int, time.split(":")) #we extract the hour and minute
        if 14 <= hr <=15:   #allows 2:00pm to 3:59pm
            if not (hr==14 and min==0): #excluding 2:00pm and only consider if it is 2:01pm
                points += 10
    
    return points

#API to return points for a receipt (GET)
@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    """ Accepts receipt ID, 
    returns points earned for that receipt """

    if not validate_id(id):  # Ensure valid UUID format
        return jsonify({"error": "The receipt is invalid."}), 400

    if id in receipts_details:
        #temporarily returning 20 points till I come up with logic for all the rules
        #return jsonify({"points": 20}), 200 

        points = points_calculator(receipts_details[id]) #awarding points based on rules
        return jsonify({"points": points}), 200
    
    return jsonify({"error":"No receipt found for that ID."}), 404

#This is to run our receipt processor App
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    