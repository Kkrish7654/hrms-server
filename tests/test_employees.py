import pytest
from fastapi import status
from fastapi.testclient import TestClient
import uuid
from datetime import date

class TestEmployeeAPI:
    @pytest.fixture
    def employee_data(self):
        def _employee_data():
            return {
                "first_name": "John",
                "last_name": "Doe",
                "email": f"john.doe.{uuid.uuid4()}@example.com",
                "phone": "123-456-7890",
                "employee_id": f"EMP-{uuid.uuid4()}",
                "department_id": 1,  # Assuming department with ID 1 exists or will be mocked
                "designation_id": 1, # Assuming designation with ID 1 exists or will be mocked
                "joining_date": str(date.today()),
                "profile_image_url": None,
                "manager_id": None,
                "probation_period": "6 months",
                "work_location_id": None,
                "job_type_id": None,
                "shift_timing": "Day",
                "weekly_hours": 40.0,
                "annual_leave_total": 20,
                "sick_leave_total": 10,
                "casual_leave_total": 5,
                "date_of_birth": str(date(1990, 1, 1)),
                "gender": "Male",
                "marital_status": "Single",
                "address": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zip_code": "12345",
                "emergency_contact_name": "Jane Doe",
                "emergency_contact_phone": "098-765-4321",
                "salary": 50000.0,
                "currency": "USD",
                "pay_frequency": "Monthly",
                "bank_account": "123456789",
                "bank_name": "Bank of America",
                "tax_id": "TAX123",
                "benefits": {"health": True, "dental": False},
                "is_active": True
            }
        return _employee_data

    @pytest.fixture
    def created_employee(self, client: TestClient, employee_data):
        response = client.post("/api/v1/employees/", json=employee_data())
        return response.json()

    def test_create_employee_success(self, client: TestClient, employee_data):
        data = employee_data()
        response = client.post("/api/v1/employees/", json=data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Employee created successfully"
        employee = response_data["data"]
        assert employee["employee_id"] == data["employee_id"]
        assert "id" in employee

    def test_create_employee_invalid_data(self, client: TestClient):
        response = client.post("/api/v1/employees/", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_employee_success(self, client: TestClient, employee_data):
        create_response = client.post("/api/v1/employees/", json=employee_data())
        employee_id = create_response.json()["data"]["id"]
        response = client.get(f"/api/v1/employees/{employee_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Employee retrieved successfully"
        employee = response_data["data"]
        assert employee["id"] == employee_id

    def test_get_employee_not_found(self, client: TestClient):
        response = client.get("/api/v1/employees/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_employees_list(self, client: TestClient, employee_data):
        for _ in range(3):
            client.post("/api/v1/employees/", json=employee_data())
        response = client.get("/api/v1/employees/")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Employees retrieved successfully"
        employees = response_data["data"]
        assert isinstance(employees, list)
        assert len(employees) >= 3

    def test_get_employees_with_pagination(self, client: TestClient, employee_data):
        for _ in range(5):
            client.post("/api/v1/employees/", json=employee_data())
        response = client.get("/api/v1/employees/?skip=1&limit=2")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        employees = response_data["data"]
        assert isinstance(employees, list)
        assert len(employees) <= 2

    def test_update_employee_success(self, client: TestClient, employee_data):
        create_response = client.post("/api/v1/employees/", json=employee_data())
        employee_id = create_response.json()["data"]["id"]
        update_data = {"first_name": "Jane", "email": f"jane.doe.{uuid.uuid4()}@example.com"}
        response = client.put(f"/api/v1/employees/{employee_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Employee updated successfully"
        employee = response_data["data"]
        assert employee["id"] == employee_id
        assert employee["first_name"] == update_data["first_name"]

    def test_update_employee_not_found(self, client: TestClient):
        response = client.put("/api/v1/employees/999999", json={})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_employee_invalid_data(self, client: TestClient, employee_data):
        create_response = client.post("/api/v1/employees/", json=employee_data())
        employee_id = create_response.json()["data"]["id"]
        response = client.put(f"/api/v1/employees/{employee_id}", json={"email": "invalid-email"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_employee_success(self, client: TestClient, employee_data):
        create_response = client.post("/api/v1/employees/", json=employee_data())
        employee_id = create_response.json()["data"]["id"]
        response = client.delete(f"/api/v1/employees/{employee_id}")
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Employee deleted successfully"
        get_response = client.get(f"/api/v1/employees/{employee_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_employee_not_found(self, client: TestClient):
        response = client.delete("/api/v1/employees/999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_employee_crud_workflow(self, client: TestClient, employee_data):
        # Create
        create_data = employee_data()
        create_response = client.post("/api/v1/employees/", json=create_data)
        assert create_response.status_code == status.HTTP_200_OK
        employee_id = create_response.json()["data"]["id"]

        # Read
        read_response = client.get(f"/api/v1/employees/{employee_id}")
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["data"]["employee_id"] == create_data["employee_id"]

        # Update
        update_data = {"first_name": "Jane", "email": f"jane.doe.updated.{uuid.uuid4()}@example.com"}
        update_response = client.put(f"/api/v1/employees/{employee_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["first_name"] == update_data["first_name"]

        # Delete
        delete_response = client.delete(f"/api/v1/employees/{employee_id}")
        assert delete_response.status_code == status.HTTP_200_OK

        # Verify deletion
        final_read_response = client.get(f"/api/v1/employees/{employee_id}")
        assert final_read_response.status_code == status.HTTP_404_NOT_FOUND