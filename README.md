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

## ⚙️ Setup & Installation

### 1️⃣ **Clone the Repository**
Run the following command to **clone the project** to your local system:
```sh
git clone https://github.com/RajVamsee/fetch-assessment.git
cd FETCH-ASSESSMENT
```

### 2️⃣ **Set Up Virtual Environment (Optional but Recommended)**

It is recommended to use a virtual environment to manage dependencies.

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

| Status Code | Description                        |
|------------|------------------------------------|
| **200 OK** | Successful request                |
| **400 Bad Request** | Invalid input or missing fields |
| **404 Not Found** | Receipt ID not found        |
| **500 Internal Server Error** | Server-side error |

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


