
import pytest
from fastapi import status
from fastapi.testclient import TestClient
import uuid

class TestDesignationAPI:
    @pytest.fixture
    def designation_data(self):
        return {
            "title": f"Software Engineer {uuid.uuid4()}"
        }

    @pytest.fixture
    def created_designation(self, client: TestClient, designation_data):
        response = client.post("/api/v1/designations/", json=designation_data)
        return response.json()

    def test_create_designation_success(self, client: TestClient, designation_data):
        response = client.post("/api/v1/designations/", json=designation_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Designation created successfully"
        designation = response_data["data"]
        assert designation["title"] == designation_data["title"]
        assert "id" in designation

    def test_create_designation_invalid_data(self, client: TestClient):
        response = client.post("/api/v1/designations/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_designation_success(self, client: TestClient, designation_data):
        create_response = client.post("/api/v1/designations/", json=designation_data)
        designation_id = create_response.json()["data"]["id"]
        response = client.get(f"/api/v1/designations/{designation_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Designation retrieved successfully"
        designation = response_data["data"]
        assert designation["id"] == designation_id

    def test_get_designation_not_found(self, client: TestClient):
        response = client.get("/api/v1/designations/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_designations_list(self, client: TestClient, designation_data):
        for _ in range(3):
            client.post("/api/v1/designations/", json={"title": f"Manager {uuid.uuid4()}"})
        response = client.get("/api/v1/designations/")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Designations retrieved successfully"
        designations = response_data["data"]
        assert isinstance(designations, list)
        assert len(designations) >= 3

    def test_get_designations_with_pagination(self, client: TestClient, designation_data):
        for _ in range(5):
            client.post("/api/v1/designations/", json={"title": f"Analyst {uuid.uuid4()}"})
        response = client.get("/api/v1/designations/?skip=1&limit=2")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        designations = response_data["data"]
        assert isinstance(designations, list)
        assert len(designations) <= 2

    def test_update_designation_success(self, client: TestClient, designation_data):
        create_response = client.post("/api/v1/designations/", json=designation_data)
        designation_id = create_response.json()["data"]["id"]
        update_data = {"title": f"Updated Designation {uuid.uuid4()}"}
        response = client.put(f"/api/v1/designations/{designation_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Designation updated successfully"
        designation = response_data["data"]
        assert designation["id"] == designation_id
        assert designation["title"] == update_data["title"]

    def test_update_designation_not_found(self, client: TestClient):
        response = client.put("/api/v1/designations/999999", json={"title": "Updated"})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_designation_invalid_data(self, client: TestClient, designation_data):
        create_response = client.post("/api/v1/designations/", json=designation_data)
        designation_id = create_response.json()["data"]["id"]
        response = client.put(f"/api/v1/designations/{designation_id}", json={"title": ""}) # Invalid empty title
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_designation_success(self, client: TestClient, designation_data):
        create_response = client.post("/api/v1/designations/", json=designation_data)
        designation_id = create_response.json()["data"]["id"]
        response = client.delete(f"/api/v1/designations/{designation_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Designation deleted successfully"
        get_response = client.get(f"/api/v1/designations/{designation_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_designation_not_found(self, client: TestClient):
        response = client.delete("/api/v1/designations/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_designation_crud_workflow(self, client: TestClient, designation_data):
        # Create
        create_data = designation_data
        create_response = client.post("/api/v1/designations/", json=create_data)
        assert create_response.status_code == status.HTTP_200_OK
        designation_id = create_response.json()["data"]["id"]

        # Read
        read_response = client.get(f"/api/v1/designations/{designation_id}")
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["data"]["title"] == create_data["title"]

        # Update
        update_data = {"title": f"Updated Workflow Designation {uuid.uuid4()}"}
        update_response = client.put(f"/api/v1/designations/{designation_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["title"] == update_data["title"]

        # Delete
        delete_response = client.delete(f"/api/v1/designations/{designation_id}")
        assert delete_response.status_code == status.HTTP_200_OK

        # Verify deletion
        final_read_response = client.get(f"/api/v1/designations/{designation_id}")
        assert final_read_response.status_code == status.HTTP_404_NOT_FOUND
