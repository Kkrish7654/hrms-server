
import pytest
from fastapi import status
from fastapi.testclient import TestClient
import uuid

class TestLeavePolicyAPI:
    @pytest.fixture
    def leave_policy_data(self):
        return {
            "policy_name": f"Standard Leave Policy {uuid.uuid4()}",
            "details": {"annual_days": 15, "sick_days": 7}
        }

    @pytest.fixture
    def created_leave_policy(self, client: TestClient, leave_policy_data):
        response = client.post("/api/v1/leave-policies/", json=leave_policy_data)
        return response.json()

    def test_create_leave_policy_success(self, client: TestClient, leave_policy_data):
        response = client.post("/api/v1/leave-policies/", json=leave_policy_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "LeavePolicy created successfully"
        leave_policy = response_data["data"]
        assert leave_policy["policy_name"] == leave_policy_data["policy_name"]
        assert "id" in leave_policy

    def test_create_leave_policy_invalid_data(self, client: TestClient):
        response = client.post("/api/v1/leave-policies/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_leave_policy_success(self, client: TestClient, leave_policy_data):
        create_response = client.post("/api/v1/leave-policies/", json=leave_policy_data)
        leave_policy_id = create_response.json()["data"]["id"]
        response = client.get(f"/api/v1/leave-policies/{leave_policy_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "LeavePolicy retrieved successfully"
        leave_policy = response_data["data"]
        assert leave_policy["id"] == leave_policy_id

    def test_get_leave_policy_not_found(self, client: TestClient):
        response = client.get("/api/v1/leave-policies/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_leave_policies_list(self, client: TestClient, leave_policy_data):
        for _ in range(3):
            client.post("/api/v1/leave-policies/", json={"policy_name": f"Policy {uuid.uuid4()}", "details": {}})
        response = client.get("/api/v1/leave-policies/")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "LeavePolicies retrieved successfully"
        leave_policies = response_data["data"]
        assert isinstance(leave_policies, list)
        assert len(leave_policies) >= 3

    def test_get_leave_policies_with_pagination(self, client: TestClient, leave_policy_data):
        for _ in range(5):
            client.post("/api/v1/leave-policies/", json={"policy_name": f"Policy {uuid.uuid4()}", "details": {}})
        response = client.get("/api/v1/leave-policies/?skip=1&limit=2")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        leave_policies = response_data["data"]
        assert isinstance(leave_policies, list)
        assert len(leave_policies) <= 2

    def test_update_leave_policy_success(self, client: TestClient, leave_policy_data):
        create_response = client.post("/api/v1/leave-policies/", json=leave_policy_data)
        leave_policy_id = create_response.json()["data"]["id"]
        update_data = {"policy_name": f"Updated Policy {uuid.uuid4()}", "details": {"annual_days": 20}}
        response = client.put(f"/api/v1/leave-policies/{leave_policy_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "LeavePolicy updated successfully"
        leave_policy = response_data["data"]
        assert leave_policy["id"] == leave_policy_id
        assert leave_policy["policy_name"] == update_data["policy_name"]

    def test_update_leave_policy_not_found(self, client: TestClient):
        response = client.put("/api/v1/leave-policies/999999", json={"policy_name": "Updated"})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_leave_policy_invalid_data(self, client: TestClient, leave_policy_data):
        create_response = client.post("/api/v1/leave-policies/", json=leave_policy_data)
        leave_policy_id = create_response.json()["data"]["id"]
        response = client.put(f"/api/v1/leave-policies/{leave_policy_id}", json={"policy_name": ""}) # Invalid empty name
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_leave_policy_success(self, client: TestClient, leave_policy_data):
        create_response = client.post("/api/v1/leave-policies/", json=leave_policy_data)
        leave_policy_id = create_response.json()["data"]["id"]
        response = client.delete(f"/api/v1/leave-policies/{leave_policy_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "LeavePolicy deleted successfully"
        get_response = client.get(f"/api/v1/leave-policies/{leave_policy_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_leave_policy_not_found(self, client: TestClient):
        response = client.delete("/api/v1/leave-policies/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_leave_policy_crud_workflow(self, client: TestClient, leave_policy_data):
        # Create
        create_data = leave_policy_data
        create_response = client.post("/api/v1/leave-policies/", json=create_data)
        assert create_response.status_code == status.HTTP_200_OK
        leave_policy_id = create_response.json()["data"]["id"]

        # Read
        read_response = client.get(f"/api/v1/leave-policies/{leave_policy_id}")
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["data"]["policy_name"] == create_data["policy_name"]

        # Update
        update_data = {"policy_name": f"Updated Workflow Policy {uuid.uuid4()}"}
        update_response = client.put(f"/api/v1/leave-policies/{leave_policy_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["policy_name"] == update_data["policy_name"]

        # Delete
        delete_response = client.delete(f"/api/v1/leave-policies/{leave_policy_id}")
        assert delete_response.status_code == status.HTTP_200_OK

        # Verify deletion
        final_read_response = client.get(f"/api/v1/leave-policies/{leave_policy_id}")
        assert final_read_response.status_code == status.HTTP_404_NOT_FOUND
