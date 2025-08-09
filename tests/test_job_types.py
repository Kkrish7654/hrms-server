
import pytest
from fastapi import status
from fastapi.testclient import TestClient
import uuid

class TestJobTypeAPI:
    @pytest.fixture
    def job_type_data(self):
        return {
            "type_name": f"Full-time {uuid.uuid4()}"
        }

    @pytest.fixture
    def created_job_type(self, client: TestClient, job_type_data):
        response = client.post("/api/v1/job-types/", json=job_type_data)
        return response.json()

    def test_create_job_type_success(self, client: TestClient, job_type_data):
        response = client.post("/api/v1/job-types/", json=job_type_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "JobType created successfully"
        job_type = response_data["data"]
        assert job_type["type_name"] == job_type_data["type_name"]
        assert "id" in job_type

    def test_create_job_type_invalid_data(self, client: TestClient):
        response = client.post("/api/v1/job-types/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_job_type_success(self, client: TestClient, job_type_data):
        create_response = client.post("/api/v1/job-types/", json=job_type_data)
        job_type_id = create_response.json()["data"]["id"]
        response = client.get(f"/api/v1/job-types/{job_type_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "JobType retrieved successfully"
        job_type = response_data["data"]
        assert job_type["id"] == job_type_id

    def test_get_job_type_not_found(self, client: TestClient):
        response = client.get("/api/v1/job-types/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_job_types_list(self, client: TestClient, job_type_data):
        for _ in range(3):
            client.post("/api/v1/job-types/", json={"type_name": f"Part-time {uuid.uuid4()}"})
        response = client.get("/api/v1/job-types/")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "JobTypes retrieved successfully"
        job_types = response_data["data"]
        assert isinstance(job_types, list)
        assert len(job_types) >= 3

    def test_get_job_types_with_pagination(self, client: TestClient, job_type_data):
        for _ in range(5):
            client.post("/api/v1/job-types/", json={"type_name": f"Contract {uuid.uuid4()}"})
        response = client.get("/api/v1/job-types/?skip=1&limit=2")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        job_types = response_data["data"]
        assert isinstance(job_types, list)
        assert len(job_types) <= 2

    def test_update_job_type_success(self, client: TestClient, job_type_data):
        create_response = client.post("/api/v1/job-types/", json=job_type_data)
        job_type_id = create_response.json()["data"]["id"]
        update_data = {"type_name": f"Updated Job Type {uuid.uuid4()}"}
        response = client.put(f"/api/v1/job-types/{job_type_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "JobType updated successfully"
        job_type = response_data["data"]
        assert job_type["id"] == job_type_id
        assert job_type["type_name"] == update_data["type_name"]

    def test_update_job_type_not_found(self, client: TestClient):
        response = client.put("/api/v1/job-types/999999", json={"type_name": "Updated"})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_job_type_invalid_data(self, client: TestClient, job_type_data):
        create_response = client.post("/api/v1/job-types/", json=job_type_data)
        job_type_id = create_response.json()["data"]["id"]
        response = client.put(f"/api/v1/job-types/{job_type_id}", json={"type_name": ""}) # Invalid empty name
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_job_type_success(self, client: TestClient, job_type_data):
        create_response = client.post("/api/v1/job-types/", json=job_type_data)
        job_type_id = create_response.json()["data"]["id"]
        response = client.delete(f"/api/v1/job-types/{job_type_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "JobType deleted successfully"
        get_response = client.get(f"/api/v1/job-types/{job_type_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_job_type_not_found(self, client: TestClient):
        response = client.delete("/api/v1/job-types/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_job_type_crud_workflow(self, client: TestClient, job_type_data):
        # Create
        create_data = job_type_data
        create_response = client.post("/api/v1/job-types/", json=create_data)
        assert create_response.status_code == status.HTTP_200_OK
        job_type_id = create_response.json()["data"]["id"]

        # Read
        read_response = client.get(f"/api/v1/job-types/{job_type_id}")
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["data"]["type_name"] == create_data["type_name"]

        # Update
        update_data = {"type_name": f"Updated Workflow Job Type {uuid.uuid4()}"}
        update_response = client.put(f"/api/v1/job-types/{job_type_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["type_name"] == update_data["type_name"]

        # Delete
        delete_response = client.delete(f"/api/v1/job-types/{job_type_id}")
        assert delete_response.status_code == status.HTTP_200_OK

        # Verify deletion
        final_read_response = client.get(f"/api/v1/job-types/{job_type_id}")
        assert final_read_response.status_code == status.HTTP_404_NOT_FOUND
