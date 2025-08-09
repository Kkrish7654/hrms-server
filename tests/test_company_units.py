
import pytest
from fastapi import status
from fastapi.testclient import TestClient
import uuid

class TestCompanyUnitAPI:
    @pytest.fixture
    def company_unit_data(self):
        return {
            "unit_name": f"Headquarters {uuid.uuid4()}",
            "address": "123 Main St"
        }

    @pytest.fixture
    def created_company_unit(self, client: TestClient, company_unit_data):
        response = client.post("/api/v1/company-units/", json=company_unit_data)
        return response.json()

    def test_create_company_unit_success(self, client: TestClient, company_unit_data):
        response = client.post("/api/v1/company-units/", json=company_unit_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "CompanyUnit created successfully"
        company_unit = response_data["data"]
        assert company_unit["unit_name"] == company_unit_data["unit_name"]
        assert "id" in company_unit

    def test_create_company_unit_invalid_data(self, client: TestClient):
        response = client.post("/api/v1/company-units/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_company_unit_success(self, client: TestClient, company_unit_data):
        create_response = client.post("/api/v1/company-units/", json=company_unit_data)
        company_unit_id = create_response.json()["data"]["id"]
        response = client.get(f"/api/v1/company-units/{company_unit_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "CompanyUnit retrieved successfully"
        company_unit = response_data["data"]
        assert company_unit["id"] == company_unit_id

    def test_get_company_unit_not_found(self, client: TestClient):
        response = client.get("/api/v1/company-units/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_company_units_list(self, client: TestClient, company_unit_data):
        for _ in range(3):
            client.post("/api/v1/company-units/", json={"unit_name": f"Branch {uuid.uuid4()}", "address": "456 Oak Ave"})
        response = client.get("/api/v1/company-units/")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "CompanyUnits retrieved successfully"
        company_units = response_data["data"]
        assert isinstance(company_units, list)
        assert len(company_units) >= 3

    def test_get_company_units_with_pagination(self, client: TestClient, company_unit_data):
        for _ in range(5):
            client.post("/api/v1/company-units/", json={"unit_name": f"Warehouse {uuid.uuid4()}", "address": "789 Pine Ln"})
        response = client.get("/api/v1/company-units/?skip=1&limit=2")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        company_units = response_data["data"]
        assert isinstance(company_units, list)
        assert len(company_units) <= 2

    def test_update_company_unit_success(self, client: TestClient, company_unit_data):
        create_response = client.post("/api/v1/company-units/", json=company_unit_data)
        company_unit_id = create_response.json()["data"]["id"]
        update_data = {"unit_name": f"Updated Unit {uuid.uuid4()}", "address": "321 New St"}
        response = client.put(f"/api/v1/company-units/{company_unit_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "CompanyUnit updated successfully"
        company_unit = response_data["data"]
        assert company_unit["id"] == company_unit_id
        assert company_unit["unit_name"] == update_data["unit_name"]

    def test_update_company_unit_not_found(self, client: TestClient):
        response = client.put("/api/v1/company-units/999999", json={"unit_name": "Updated"})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_company_unit_invalid_data(self, client: TestClient, company_unit_data):
        create_response = client.post("/api/v1/company-units/", json=company_unit_data)
        company_unit_id = create_response.json()["data"]["id"]
        response = client.put(f"/api/v1/company-units/{company_unit_id}", json={"unit_name": ""}) # Invalid empty name
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_company_unit_success(self, client: TestClient, company_unit_data):
        create_response = client.post("/api/v1/company-units/", json=company_unit_data)
        company_unit_id = create_response.json()["data"]["id"]
        response = client.delete(f"/api/v1/company-units/{company_unit_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "CompanyUnit deleted successfully"
        get_response = client.get(f"/api/v1/company-units/{company_unit_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_company_unit_not_found(self, client: TestClient):
        response = client.delete("/api/v1/company-units/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_company_unit_crud_workflow(self, client: TestClient, company_unit_data):
        # Create
        create_data = company_unit_data
        create_response = client.post("/api/v1/company-units/", json=create_data)
        assert create_response.status_code == status.HTTP_200_OK
        company_unit_id = create_response.json()["data"]["id"]

        # Read
        read_response = client.get(f"/api/v1/company-units/{company_unit_id}")
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["data"]["unit_name"] == create_data["unit_name"]

        # Update
        update_data = {"unit_name": f"Updated Workflow Unit {uuid.uuid4()}"}
        update_response = client.put(f"/api/v1/company-units/{company_unit_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["unit_name"] == update_data["unit_name"]

        # Delete
        delete_response = client.delete(f"/api/v1/company-units/{company_unit_id}")
        assert delete_response.status_code == status.HTTP_200_OK

        # Verify deletion
        final_read_response = client.get(f"/api/v1/company-units/{company_unit_id}")
        assert final_read_response.status_code == status.HTTP_404_NOT_FOUND
