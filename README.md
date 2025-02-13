# 🧾 Receipt Processor - Fetch Assessment

## 📌 Author Information
- **Name:** Gopala Raj
- **Phone:** 3528882788
- **Email:** rajgopalavamsee01@gmail.com

---

## 📝 Introduction

This exercise is a **Receipt Processor API**, where users can submit receipts and earn points based on certain rules. The API processes receipts, assigns them a unique ID, calculates points, and returns them.

The application is built using **Python & Flask**, ensuring a robust, scalable, and lightweight RESTful API. Unit tests are included to verify all endpoints and validation checks.

---

## 🔥 Technologies Used

| Technology   | Purpose |
|-------------|---------|
| **Python** | Main programming language |
| **Flask** | Web framework for API development |
| **Pytest** | Used for writing unit tests |
| **Docker** | Containerization for deployment |
| **UUID** | Generating unique receipt IDs |
| **Regex** | Validating input formats |
| **Datetime** | Processing dates and timestamps |
| **Math** | Rounding and calculations |
| **Postman** | For API Testing |

---
## 🎯 Rules for Awarding Points

These rules collectively define how many points should be awarded to a receipt:

- **1️⃣ One point** for every alphanumeric character in the retailer name.  
- **2️⃣ 50 points** if the total is a round dollar amount with no cents.  
- **3️⃣ 25 points** if the total is a multiple of `0.25`.  
- **4️⃣ 5 points** for every two items on the receipt.  
- **5️⃣ If the trimmed length** of the item description is a multiple of 3, multiply the price by `0.2` and round up to the nearest integer.  
- **6️⃣ 6 points** if the day in the purchase date is odd.  
- **7️⃣ 10 points** if the time of purchase is after 2:00 PM and before 4:00 PM.  
---

## 📌 Explanation of Files

- **app.py** → Contains the Flask API logic, processing receipts, and calculating points.
- **test_app.py** → Includes unit tests to validate API functionality.
- **Dockerfile** → Defines the instructions to create a Docker container.
- **requirements.txt** → Lists the necessary dependencies for the project.
- **README.md** → Provides instructions on setup, installation, and running the project.
- **env/** → Virtual environment folder.

---

**💾 Data Persistence**  
This API **stores receipt data in-memory** and does **not persist data** after the application is stopped.  
- We use a Python dictionary to temporarily store receipt details.  
- Since this is an in-memory solution, restarting the server **removes all stored receipts**.
- This behavior aligns with Fetch's requirements that **data persistence is not mandatory**.

---

**📜 API Specification (api.yml)**  
This repository follows the API specifications outlined in the provided `api.yml` file in the link below. It defines all endpoints, expected request formats, and response structures. The API definitions can be tested using tools like **Postman**.

- link to the fetch receipt processor exercise : https://github.com/fetch-rewards/receipt-processor-challenge
- can access the exercise instuctions, api.yml and examples in the above link.

---

**🧪 Testing the API with Postman**
To test the API using Postman:
1. Open **Postman** and create a new request.
2. **For Processing Receipts**:
   - Set the method to `POST`
   - Use the endpoint: `http://localhost:5000/receipts/process`
   - Go to the **Body** tab, select **raw**, and choose **JSON format**.
   - Paste a sample receipt JSON and send the request.
3. **For Retrieving Points**:
   - Set the method to `GET`
   - Use the endpoint: `http://localhost:5000/receipts/{id}/points`
   - Replace `{id}` with a valid receipt ID returned from the previous request.

- Sample JSON for testing :
```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}
```

- Expected points : 28 

```text
Total Points: 28
Breakdown:
     6 points - retailer name has 6 characters
    10 points - 5 items (2 pairs @ 5 points each)
     3 Points - "Emils Cheese Pizza" is 18 characters (a multiple of 3)
                item price of 12.25 * 0.2 = 2.45, rounded up is 3 points
     3 Points - "Klarbrunn 12-PK 12 FL OZ" is 24 characters (a multiple of 3)
                item price of 12.00 * 0.2 = 2.4, rounded up is 3 points
     6 points - purchase day is odd
  + ---------
  = 28 points
```

---

## ⚙️ Setup & Installation

🔹 Prerequisites
Before proceeding, ensure that you have Python 3.9+ installed on your system.
To check if Python is installed, run: 
```Python
python --version
```
- If Python is not installed, download and install it from the official Python website: 
- 👉 Download : https://www.python.org/downloads/


### 1️⃣ **Clone the Repository**
Run the following command to **clone the project** to your local system:
```sh
git clone https://github.com/RajVamsee/fetch-assessment.git
cd FETCH-ASSESSMENT
```

### 2️⃣ **Set Up Virtual Environment (Mandatory for Dependency Management)**

A virtual environment (env) is required to isolate dependencies and run the application properly. Without this setup, the application may fail to execute correctly.

#### **For Windows:**
```sh
python -m venv env
env\Scripts\activate
```
#### **For Mac/Linux:**
```sh
python3 -m venv env
source env/bin/activate
```
To deactivate the virtual environment at any time, use:
```sh
deactivate
```
Note: You must activate the virtual environment (env) before running the application or executing any dependency installation commands.

---

### 3️⃣ **Install dependencies**

Ensure you have Python 3.9+ installed. Then, install the required dependencies using:
```sh
pip install -r requirements.txt
```
### 4️⃣ **Run the Application Locally**
To start the Flask application locally, run:
```sh
python app.py
```
The application will start on http://127.0.0.1:5000/ or http://localhost:5000/.

### 5️⃣ **Run Tests**
  
To verify the API and its functionalities, run the test suite using:
```sh
pytest test_app.py
```
If all test cases pass, you will see an output indicating 16 passed test cases.

### 6️⃣ **Run the Application using Docker**
To containerize and run the application using Docker, follow these steps:

Step 1 : Build the Docker Image
Run the following command to create a Docker image:
```sh
docker build -t fetch-receipt-processor .
```
Step 2 : Run the Docker Container
Once the image is built, start a container using:
```sh
docker run -p 5000:5000 fetch-receipt-processor
```
The application should now be accessible at:

- http://127.0.0.1:5000/
- http://localhost:5000/

### 🛑 Stopping Docker Container
To stop the running container, use:
```sh
docker ps  # List running containers
docker stop <container_id>  # Stop the container
```

### 7️⃣ **API Endpoints & Usage**
1️⃣ Process a Receipt
- Endpoint: POST /receipts/process
- Description: Submit a receipt in JSON format to process and store it.
- Sample Request:
```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "total": "35.35",
  "items": [
    { "shortDescription": "Mountain Dew 12PK", "price": "6.49" },
    { "shortDescription": "Emils Cheese Pizza", "price": "12.25" },
    { "shortDescription": "Knorr Creamy Chicken", "price": "1.26" }
  ]
}
```
- Sample Response:
```json
{
  "id": "b835c81b-8b58-4bc5-94c3-1a2dd99c1cf4"
}
```
2️⃣ Get Points for a Receipt
- Endpoint: GET /receipts/{id}/points
- Description: Retrieve the total points awarded for a processed receipt.
- Sample Response:
```json
{
  "points": 28
}
```
### 8️⃣ **Expected Responses & Errors** 

| Status Code | Description | Possible Causes | Fix |
|------------|------------------------------------|--------------------------------|------------------------|
| **200 OK** | Request was successful | ✅ Valid receipt data | No action needed |
| **400 Bad Request** | Invalid input or missing fields | ❌ Incorrect JSON format or missing required fields | Ensure all required fields are present |
| **404 Not Found** | Receipt ID not found | ❌ Invalid or non-existent receipt ID used | Check if the correct ID is used |

--- 

### 9️⃣ **Project Validation**
✔️ Fully implemented API endpoints  
✔️ Validations for input data & proper error handling  
✔️ Unit-tested API with 16 successful test cases  
✔️ Dockerized setup for easy deployment 

## 🔗 Conclusion
This project provides a fully functional **Receipt Processor API**, ensuring a smooth user experience with proper validation, testing, and containerization using Docker.

## 📌 Contact Information
For any questions or assistance, feel free to contact:

- 📧 **Email:** [rajgopalavamsee01@gmail.com](mailto:rajgopalavamsee01@gmail.com)
- 📞 **Phone:** 3528882788
- 🌐 **GitHub:** [RajVamsee](https://github.com/RajVamsee)


