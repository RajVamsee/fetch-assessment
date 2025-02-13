import pytest
import json
from app import app 
import uuid

@pytest.fixture
def client():
  app.config["TESTING"] = True
  with app.test_client() as client:
    yield client

#test case for home page 
def test_home_page(client):
  response = client.get("/")
  assert response.status_code == 200
  assert response.data.decode("utf-8") == "Receipt Processor Application"

#sample test case 1
def test_1(client):
  receipt = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
      {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
      {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
      {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
      {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
      {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
    ],
    "total": "35.35"
  }
  
  #submit receipt
  process_response = client.post("/receipts/process", json=receipt)
  assert process_response.status_code == 200 #verify receipt is processed
  response_data = process_response.get_json()
  assert "id" in response_data #verify ID is returned
  
  receipt_id = response_data["id"]
  
  #get points for receipt
  points_response = client.get(f"/receipts/{receipt_id}/points")
  assert points_response.status_code == 200 #verify retrieval of receipt
  points = points_response.get_json()
  assert "points" in points #verify points are returned
  assert points["points"] == 28 #verify expected output points

#sample test case 2
def test_2(client):
  receipt = {
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
  } 
  
  #submit receipt
  process_response = client.post("/receipts/process", json=receipt)
  assert process_response.status_code == 200 #verify receipt is processed
  response_data = process_response.get_json()
  assert "id" in response_data #verify ID is returned
  
  receipt_id = response_data["id"]
  
  #get points for receipt
  points_response = client.get(f"/receipts/{receipt_id}/points")
  assert points_response.status_code == 200 #verify retrieval of receipt
  points = points_response.get_json()
  assert "points" in points #verify points are returned
  assert points["points"] == 109 #verify expected output points

#test case for morning-receipt.json example
def test_3(client):
  receipt = {
    "retailer": "Walgreens",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "08:13",
    "total": "2.65",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
        {"shortDescription": "Dasani", "price": "1.40"}
    ]
  } 
  
  #submit receipt
  process_response = client.post("/receipts/process", json=receipt)
  assert process_response.status_code == 200 #verify receipt is processed
  response_data = process_response.get_json()
  assert "id" in response_data #verify ID is returned
  
  receipt_id = response_data["id"]
  
  #get points for receipt
  points_response = client.get(f"/receipts/{receipt_id}/points")
  assert points_response.status_code == 200 #verify retrieval of receipt
  points = points_response.get_json()
  assert "points" in points #verify points are returned
  assert points["points"] == 15 #verify expected output points
  
#test case for simple-receipt.json example
def test_4(client):
  receipt = {
    "retailer": "Target",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "13:13",
    "total": "1.25",
    "items": [
        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
    ]
  }
  
  #submit receipt
  process_response = client.post("/receipts/process", json=receipt)
  assert process_response.status_code == 200 #verify receipt is processed
  response_data = process_response.get_json()
  assert "id" in response_data #verify ID is returned
  
  receipt_id = response_data["id"]
  
  #get points for receipt
  points_response = client.get(f"/receipts/{receipt_id}/points")
  assert points_response.status_code == 200 #verify retrieval of receipt
  points = points_response.get_json()
  assert "points" in points #verify points are returned
  assert points["points"] == 31 #verify expected output points

#test case for invalid date format
def test_5(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "01-02-2022",  # Wrong date format (MM-DD-YYYY)
        "purchaseTime": "13:01",
        "total": "10.00",
        "items": [{"shortDescription": "Item1", "price": "5.00"}]
    }

    #submit receipt
    process_response = client.post("/receipts/process", json=receipt)
    assert process_response.status_code == 400 #verify 400 Bad Request
    response_data = process_response.get_json()
    assert "error" in response_data #verify error is generated
    
#test case for invalid time format
def test_6(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "1:01 PM",  # Wrong format (should be 24-hour)
        "total": "10.00",
        "items": [{"shortDescription": "Item1", "price": "5.00"}]
    }

    #submit receipt
    process_response = client.post("/receipts/process", json=receipt)
    assert process_response.status_code == 400 #verify 400 Bad Request
    response_data = process_response.get_json()
    assert "error" in response_data #verify error is generated
    
#test case for empty items list
def test_7(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:01",
        "total": "10.00",
        "items": [] #items list is empty
    }

    #submit receipt
    process_response = client.post("/receipts/process", json=receipt)
    assert process_response.status_code == 400 #verify 400 Bad Request
    response_data = process_response.get_json()
    assert "error" in response_data #verify error is generated

#test case for missing short description
def test_8(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:01",
        "total": "10.00",
        "items": [{"price": "5.00"}] #short description is missing
    }

    #submit receipt
    process_response = client.post("/receipts/process", json=receipt)
    assert process_response.status_code == 400 #verify 400 Bad Request
    response_data = process_response.get_json()
    assert "error" in response_data #verify error is generated

#test case for missing price
def test_9(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:01",
        "total": "10.00",
        "items": [{"shortDescription": "Item1"}] #price is missing
    }

    #submit receipt
    process_response = client.post("/receipts/process", json=receipt)
    assert process_response.status_code == 400 #verify 400 Bad Request
    response_data = process_response.get_json()
    assert "error" in response_data #verify error is generated

#test case for invalid price format
def test_10(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:01",
        "total": "10.00",
        "items": [{"shortDescription": "Item1", "price": "5"}] #invalid price format
    }

    #submit receipt
    process_response = client.post("/receipts/process", json=receipt)
    assert process_response.status_code == 400 #verify 400 Bad Request
    response_data = process_response.get_json()
    assert "error" in response_data #verify error is generated

#test case for invalid total
def test_11(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:01",
        "total": "10", #invalid total format
        "items": [{"shortDescription": "Item1", "price": "5.00"}]
    }

    #submit receipt
    process_response = client.post("/receipts/process", json=receipt)
    assert process_response.status_code == 400 #verify 400 Bad Request
    response_data = process_response.get_json()
    assert "error" in response_data #verify error is generated

#test case for missing required fields
def test_12(client):
    receipt = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        #missing purchaseTime field
        "total": "10.00",
        "items": [{"shortDescription": "Item1", "price": "5.00"}]
    }

    #submit receipt
    process_response = client.post("/receipts/process", json=receipt)
    assert process_response.status_code == 400 #verify 400 Bad Request
    response_data = process_response.get_json()
    assert "error" in response_data #verify error is generated

#test case for invalid receipt id
def test_13(client):
  #get points for receipt
  points_response = client.get(f"/receipts/63452/points") #invalid id format
  assert points_response.status_code == 400 #verify 400 Bad request
  points = points_response.get_json()
  assert "error" in points #verify error is generated

#test case for receipt not found
def test_14(client):
  #get points for receipt
  invalid_id = "adb6b560-0eef-42bc-9d16-df48f30e89b2"  # Random valid UUID
  points_response = client.get(f"/receipts/{invalid_id}/points") #invalid id 
  assert points_response.status_code == 404 #verify 404 not found error
  points = points_response.get_json()
  assert "error" in points #verify error is generated

#test case for huge input
def test_15(client):
  my_items = [{"shortDescription": f"Item{i}", "price": "1.00"} for i in range(200)]  # 200 items
  receipt = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": my_items,
    "total": "35.35"
  }
  
  #submit receipt
  process_response = client.post("/receipts/process", json=receipt)
  assert process_response.status_code == 200 #verify receipt is processed
  response_data = process_response.get_json()
  assert "id" in response_data #verify ID is returned
  
  receipt_id = response_data["id"]
  
  #get points for receipt
  points_response = client.get(f"/receipts/{receipt_id}/points")
  assert points_response.status_code == 200 #verify retrieval of receipt
  points = points_response.get_json()
  assert "points" in points #verify points are returned




    




    
    



  

  
  
  
  
  
  
  
  
  
  
  

  


