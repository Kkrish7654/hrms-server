
import pytest
from fastapi import status
from fastapi.testclient import TestClient
import uuid
from datetime import date

class TestLeaveAPI:
    @pytest.fixture
    def leave_data(self):
        return {
            "employee_id": 1,  # Assuming employee with ID 1 exists or will be mocked
            "leave_type": "Annual Leave",
            "start_date": str(date.today()),
            "end_date": str(date.today()),
            "reason": "Vacation",
            "status": "Pending",
            "approved_by_id": None
        }

    @pytest.fixture
    def created_leave(self, client: TestClient, leave_data):
        response = client.post("/api/v1/leaves/", json=leave_data)
        return response.json()

    def test_create_leave_success(self, client: TestClient, leave_data):
        response = client.post("/api/v1/leaves/", json=leave_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Leave created successfully"
        leave = response_data["data"]
        assert leave["employee_id"] == leave_data["employee_id"]
        assert "id" in leave

    def test_create_leave_invalid_data(self, client: TestClient):
        response = client.post("/api/v1/leaves/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_leave_success(self, client: TestClient, leave_data):
        create_response = client.post("/api/v1/leaves/", json=leave_data)
        leave_id = create_response.json()["data"]["id"]
        response = client.get(f"/api/v1/leaves/{leave_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Leave retrieved successfully"
        leave = response_data["data"]
        assert leave["id"] == leave_id

    def test_get_leave_not_found(self, client: TestClient):
        response = client.get("/api/v1/leaves/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_leaves_list(self, client: TestClient, leave_data):
        for _ in range(3):
            client.post("/api/v1/leaves/", json=leave_data)
        response = client.get("/api/v1/leaves/")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Leaves retrieved successfully"
        leaves = response_data["data"]
        assert isinstance(leaves, list)
        assert len(leaves) >= 3

    def test_get_leaves_with_pagination(self, client: TestClient, leave_data):
        for _ in range(5):
            client.post("/api/v1/leaves/", json=leave_data)
        response = client.get("/api/v1/leaves/?skip=1&limit=2")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        leaves = response_data["data"]
        assert isinstance(leaves, list)
        assert len(leaves) <= 2

    def test_update_leave_success(self, client: TestClient, leave_data):
        create_response = client.post("/api/v1/leaves/", json=leave_data)
        leave_id = create_response.json()["data"]["id"]
        update_data = {"status": "Approved"}
        response = client.put(f"/api/v1/leaves/{leave_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Leave updated successfully"
        leave = response_data["data"]
        assert leave["id"] == leave_id
        assert leave["status"] == update_data["status"]

    def test_update_leave_not_found(self, client: TestClient):
        response = client.put("/api/v1/leaves/999999", json={"status": "Approved"})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_leave_invalid_data(self, client: TestClient, leave_data):
        create_response = client.post("/api/v1/leaves/", json=leave_data)
        leave_id = create_response.json()["data"]["id"]
        response = client.put(f"/api/v1/leaves/{leave_id}", json={"employee_id": "invalid"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_leave_success(self, client: TestClient, leave_data):
        create_response = client.post("/api/v1/leaves/", json=leave_data)
        leave_id = create_response.json()["data"]["id"]
        response = client.delete(f"/api/v1/leaves/{leave_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Leave deleted successfully"
        get_response = client.get(f"/api/v1/leaves/{leave_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_leave_not_found(self, client: TestClient):
        response = client.delete("/api/v1/leaves/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_leave_crud_workflow(self, client: TestClient, leave_data):
        # Create
        create_data = leave_data
        create_response = client.post("/api/v1/leaves/", json=create_data)
        assert create_response.status_code == status.HTTP_200_OK
        leave_id = create_response.json()["data"]["id"]

        # Read
        read_response = client.get(f"/api/v1/leaves/{leave_id}")
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["data"]["employee_id"] == create_data["employee_id"]

        # Update
        update_data = {"status": "Rejected"}
        update_response = client.put(f"/api/v1/leaves/{leave_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["status"] == update_data["status"]

        # Delete
        delete_response = client.delete(f"/api/v1/leaves/{leave_id}")
        assert delete_response.status_code == status.HTTP_200_OK

        # Verify deletion
        final_read_response = client.get(f"/api/v1/leaves/{leave_id}")
        assert final_read_response.status_code == status.HTTP_404_NOT_FOUND
