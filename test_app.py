import pytest
import json
from app import app 

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Receipt Processor Application"


