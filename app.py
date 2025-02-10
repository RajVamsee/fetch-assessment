#importing Flask
from flask import Flask 

#Create a Flask application instance 
app = Flask(__name__)

#Defining the route for our receipt processor homepage "/"
@app.route('/')
def home():
    return "Receipt Processor Application"

#run our receipt processor App only if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)