
import pytest
from fastapi import status
from fastapi.testclient import TestClient

class TestHealthAPI:
    def test_health_check(self, client: TestClient):
        response = client.get("/api/v1/health")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Application is running smoothly"
        assert response_data["data"] == {"status": "healthy"}
