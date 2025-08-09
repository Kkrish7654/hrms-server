"""
Unit tests for Department API CRUD operations
"""
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid


class TestDepartmentAPI:
    """Test cases for Department CRUD API endpoints."""

    @pytest.fixture
    def department_data(self):
        """Sample department data for testing with unique name."""
        return {
            "name": f"Human Resources {uuid.uuid4()}"
        }

    @pytest.fixture
    def created_department(self, client: TestClient, department_data):
        """Create a department for testing and return the response."""
        response = client.post("/api/v1/departments/", json=department_data)
        return response.json()

    def test_create_department_success(self, client: TestClient, department_data):
        """
        Test successful department creation.
        
        Verifies:
        - Returns 200 status code
        - Response contains correct structure
        - Department data matches input
        - Database assigns an ID
        """
        # Act
        response = client.post("/api/v1/departments/", json=department_data)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Department created successfully"
        
        department = response_data["data"]
        assert department["name"] == department_data["name"]
        assert "id" in department
        assert isinstance(department["id"], int)

    def test_create_department_duplicate_name(self, client: TestClient):
        """Test creating department with duplicate name fails (should return 500 or IntegrityError)."""
        import sqlalchemy
        name = f"Duplicate Department {uuid.uuid4()}"
        data = {"name": name}
        client.post("/api/v1/departments/", json=data)
        try:
            response = client.post("/api/v1/departments/", json=data)
            # Should return 500 error due to unique constraint
            assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        except sqlalchemy.exc.IntegrityError:
            # If IntegrityError is raised, this is also a pass for this test
            assert True

    def test_create_department_invalid_data(self, client: TestClient):
        """
        Test creating department with invalid data fails.
        """
        # Act
        response = client.post("/api/v1/departments/", json={})
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_department_success(self, client: TestClient):
        """
        Test successful retrieval of a department by ID.
        """
        # Arrange
        name = f"Get Department {uuid.uuid4()}"
        create_response = client.post("/api/v1/departments/", json={"name": name})
        department_id = create_response.json()["data"]["id"]
        
        # Act
        response = client.get(f"/api/v1/departments/{department_id}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Department retrieved successfully"
        
        department = response_data["data"]
        assert department["id"] == department_id
        assert department["name"] == name

    def test_get_department_not_found(self, client: TestClient):
        """
        Test retrieving non-existent department returns 404.
        """
        # Act
        response = client.get("/api/v1/departments/999999")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_departments_list(self, client: TestClient):
        """
        Test retrieving list of departments.
        """
        # Arrange - Create multiple departments
        departments_data = [
            {"name": f"Human Resources {uuid.uuid4()}"},
            {"name": f"Engineering {uuid.uuid4()}"},
            {"name": f"Marketing {uuid.uuid4()}"}
        ]
        
        for dept_data in departments_data:
            client.post("/api/v1/departments/", json=dept_data)
        
        # Act
        response = client.get("/api/v1/departments/")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Departments retrieved successfully"
        
        departments = response_data["data"]
        assert isinstance(departments, list)
        assert len(departments) >= 3

    def test_get_departments_with_pagination(self, client: TestClient):
        """
        Test retrieving departments with pagination parameters.
        """
        # Arrange - Create multiple departments
        for i in range(5):
            client.post("/api/v1/departments/", json={"name": f"Department {uuid.uuid4()}"})
        
        # Act
        response = client.get("/api/v1/departments/?skip=1&limit=2")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        response_data = response.json()
        departments = response_data["data"]
        assert isinstance(departments, list)
        assert len(departments) <= 2

    def test_update_department_success(self, client: TestClient):
        """
        Test successful department update.
        """
        # Arrange
        name = f"Update Department {uuid.uuid4()}"
        create_response = client.post("/api/v1/departments/", json={"name": name})
        department_id = create_response.json()["data"]["id"]
        update_data = {"name": f"Updated {uuid.uuid4()}"}
        
        # Act
        response = client.put(f"/api/v1/departments/{department_id}", json=update_data)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Department updated successfully"
        
        department = response_data["data"]
        assert department["id"] == department_id
        assert department["name"] == update_data["name"]

    def test_update_department_not_found(self, client: TestClient):
        """
        Test updating non-existent department returns 404.
        """
        # Act
        response = client.put("/api/v1/departments/999999", json={"name": "Updated"})
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_department_invalid_data(self, client: TestClient):
        """
        Test updating department with invalid data fails.
        """
        # Arrange
        name = f"Invalid Update Department {uuid.uuid4()}"
        create_response = client.post("/api/v1/departments/", json={"name": name})
        department_id = create_response.json()["data"]["id"]
        
        # Act
        response = client.put(f"/api/v1/departments/{department_id}", json={})
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_delete_department_success(self, client: TestClient):
        """
        Test successful department deletion.
        """
        # Arrange
        name = f"Delete Department {uuid.uuid4()}"
        create_response = client.post("/api/v1/departments/", json={"name": name})
        department_id = create_response.json()["data"]["id"]
        
        # Act
        response = client.delete(f"/api/v1/departments/{department_id}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Department deleted successfully"
        
        # Verify department is deleted
        get_response = client.get(f"/api/v1/departments/{department_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_department_not_found(self, client: TestClient):
        """
        Test deleting non-existent department returns 404.
        """
        # Act
        response = client.delete("/api/v1/departments/999999")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_department_crud_workflow(self, client: TestClient):
        """
        Test complete CRUD workflow for departments.
        """
        # Create
        create_data = {"name": f"Test Department {uuid.uuid4()}"}
        create_response = client.post("/api/v1/departments/", json=create_data)
        assert create_response.status_code == status.HTTP_200_OK
        
        department_id = create_response.json()["data"]["id"]
        
        # Read
        read_response = client.get(f"/api/v1/departments/{department_id}")
        assert read_response.status_code == status.HTTP_200_OK
        assert read_response.json()["data"]["name"] == create_data["name"]
        
        # Update
        update_data = {"name": f"Updated Test Department {uuid.uuid4()}"}
        update_response = client.put(f"/api/v1/departments/{department_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["data"]["name"] == update_data["name"]
        
        # Delete
        delete_response = client.delete(f"/api/v1/departments/{department_id}")
        assert delete_response.status_code == status.HTTP_200_OK
        
        # Verify deletion
        final_read_response = client.get(f"/api/v1/departments/{department_id}")
        assert final_read_response.status_code == status.HTTP_404_NOT_FOUND
