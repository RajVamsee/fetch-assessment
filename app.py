#import statements
from flask import Flask 
from flask import request, jsonify
import uuid

#Create a Flask application instance 
app = Flask(__name__)

#Our in-memory storage for receipts
receipts_details = {}

#Defining the routes for our receipt processor
@app.route('/')
def home():
    return "Receipt Processor Application"

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

@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    """ Accepts receipt ID, 
    returns points earned for that receipt """

    if id in receipts_details:
        return jsonify({"points": 20}), 200 
    return jsonify({"error":"Receipt not found"}), 404

#run our receipt processor App only if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)