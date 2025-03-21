import pytest
from fastapi.testclient import TestClient
from service import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_execute_test():
    test_plan = {
        "test_plan": {
            "steps": [
                {"action": "navigate", "value": "https://example.com"},
                {"action": "click", "selector": "button#submit"}
            ]
        },
        "url": "https://example.com",
        "record_video": False
    }
    response = client.post("/execute", json=test_plan)
    assert response.status_code == 200
    assert "steps" in response.json()
    assert "success" in response.json()

def test_navigate_to_url():
    request_data = {"url": "https://example.com"}
    response = client.post("/navigate", json=request_data)
    assert response.status_code == 200
    assert "url" in response.json()
    assert "elements" in response.json()

def test_process_step():
    test_plan = {
        "url": "https://ale-sanchez-g.github.io/featureflags/",
        "test_plan": {
          "description": "Validate Classic Calculator Functionality with Various Calculations",
          "steps": [
            {
              "action": "navigate", "value": "https://ale-sanchez-g.github.io/featureflags/"
            },
            {
              "action": "hover", "selector": "button:has-text('1')"
            },
            {
              "action": "click", "selector": "button:has-text('1')"
            },
            {
              "action": "click", "selector": "button:has-text('+')"
            },
            {
              "action": "click", "selector": "button:has-text('1')"
            },
            {
              "action": "click", "selector": "button:has-text('=')"
            },
            {
              "action": "check", "selector": ".display", "value": "2"
            }
          ]
        }
      }
    response = client.post("/execute", json=test_plan)
    assert response.status_code == 200
    assert "steps" in response.json()
    assert response.json().get("success") == true
    assert response.json().get("error") is null

