from fastapi.testclient import TestClient
import sys
import os
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from leak_lock_ai.main import app
client = TestClient(app)

def test_read_main():
    """
    Tests the root ("/") endpoint to check if the API is up and running.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World, testing"}
