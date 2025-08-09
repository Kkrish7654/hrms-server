import pytest
from fastapi import status
from fastapi.testclient import TestClient
import uuid

class TestLeaveTypeAPI:
    @pytest.fixture
    def leave_type_data(self):
        return {
            "name": f"Annual Leave {uuid.uuid4()}"
        }

    @pytest.fixture
    def created_leave_type(self, client: TestClient, leave_type_data):
        response = client.post("/api/v1/leave-types/", json=leave_type_data)
        return response.json()

    def test_create_leave_type_success(self, client: TestClient, leave_type_data):
        response = client.post("/api/v1/leave-types/", json=leave_type_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "LeaveType created successfully"
        leave_type = response_data["data"]
        assert leave_type["name"] == leave_type_data["name"]
        assert "id" in leave_type

    def test_create_leave_type_invalid_data(self, client: TestClient):
        response = client.post("/api/v1/leave-types/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_leave_type_success(self, client: TestClient, leave_type_data):
        create_response = client.post("/api/v1/leave-types/", json=leave_type_data)
        leave_type_id = create_response.json()["data"]["id"]
        response = client.get(f"/api/v1/leave-types/{leave_type_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "LeaveType retrieved successfully"
        leave_type = response_data["data"]
        assert leave_type["id"] == leave_type_id

    def test_get_leave_type_not_found(self, client: TestClient):
        response = client.get("/api/v1/leave-types/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_leave_types_list(self, client: TestClient, leave_type_data):
        for _ in range(3):
            client.post("/api/v1/leave-types/", json={"name": f"Sick Leave {uuid.uuid4()}"})
        response = client.get("/api/v1/leave-types/")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "LeaveTypes retrieved successfully"
        leave_types = response_data["data"]
        assert isinstance(leave_types, list)
        assert len(leave_types) >= 3

    def test_get_leave_types_with_pagination(self, client: TestClient, leave_type_data):
        for _ in range(5):
            client.post("/api/v1/leave-types/", json={"name": f"Casual Leave {uuid.uuid4()}"})
        response = client.get("/api/v1/leave-types/?skip=1&limit=2")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        leave_types = response_data["data"]
        assert isinstance(leave_types, list)
        assert len(leave_types) <= 2

    def test_update_leave_type_success(self, client: TestClient, leave_type_data):
        create_response = client.post("/api/v1/leave-types/", json=leave_type_data)
        leave_type_id = create_response.json()["data"]["id"]
        update_data = {"name": f"Updated Leave {uuid.uuid4()}"}
        response = client.put(f"/api/v1/leave-types/{leave_type_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "LeaveType updated successfully"
        leave_type = response_data["data"]
        assert leave_type["id"] == leave_type_id
        assert leave_type["name"] == update_data["name"]

    def test_update_leave_type_not_found(self, client: TestClient):
        response = client.put("/api/v1/leave-types/999999", json={"name": "Updated"})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_leave_type_invalid_data(self, client: TestClient, leave_type_data):
        create_response = client.post("/api/v1/leave-types/", json=leave_type_data)
        leave_type_id = create_response.json()["data"]["id"]
        response = client.put(f"/api/v1/leave-types/{leave_type_id}", json={"name": ""}) # Invalid empty name
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_leave_type_success(self, client: TestClient, leave_type_data):
        create_response = client.post("/api/v1/leave-types/", json=leave_type_data)
        leave_type_id = create_response.json()["data"]["id"]
        response = client.delete(f"/api/v1/leave-types/{leave_type_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "LeaveType deleted successfully"
        get_response = client.get(f"/api/v1/leave-types/{leave_type_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_leave_type_not_found(self, client: TestClient):
        response = client.delete("/api/v1/leave-types/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_leave_type_crud_workflow(self, client: TestClient, leave_type_data):
        # Create
        create_data = leave_type_data
        create_response = client.post("/api/v1/leave-types/", json=create_data)
        assert create_response.status_code == status.HTTP_200_OK
        leave_type_id = create_response.json()["data"]["id"]

        # Read
        read_response = client.get(f"/api/v1/leave-types/{leave_type_id}")
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["data"]["name"] == create_data["name"]

        # Update
        update_data = {"name": f"Updated Workflow Leave {uuid.uuid4()}"}
        update_response = client.put(f"/api/v1/leave-types/{leave_type_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["name"] == update_data["name"]

        # Delete
        delete_response = client.delete(f"/api/v1/leave-types/{leave_type_id}")
        assert delete_response.status_code == status.HTTP_200_OK

        # Verify deletion
        final_read_response = client.get(f"/api/v1/leave-types/{leave_type_id}")
        assert final_read_response.status_code == status.HTTP_404_NOT_FOUND