# HRMS Backend Application Requirements

## 1. Overview

This document outlines the technical requirements for the backend of a Human Resource Management System (HRMS). The application will be built using the **FastAPI** framework with a **PostgreSQL** relational database. It will provide a comprehensive set of APIs to manage employee data, organizational structure, leave, and attendance.

**Note on Authentication:** User authentication and role management are handled by a separate `auth-gateway` repository. This HRMS backend will operate as a downstream service. It will trust the incoming requests that have been vetted by the gateway. The gateway should pass necessary user context (like `employee_id` and `role`) in the request headers.

---

## 2. Technology Stack

* **Framework:** FastAPI
* **Database:** PostgreSQL
* **Language:** Python 3.9+
* **ORM:** SQLAlchemy (with Alembic for migrations)
* **Schema Validation:** Pydantic

---

## 3. Database Schema

The database will be relational and consist of the following tables. Foreign keys will be used to maintain data integrity.

### Table: `employees`

This is the central table for storing all employee information.

| Column Name                 | Data Type                  | Constraints & Notes                                                    |
| --------------------------- | -------------------------- | ---------------------------------------------------------------------- |
| `id`                        | `SERIAL`                   | **Primary Key** |
| `employee_id`               | `VARCHAR(50)`              | **Unique**, Not Null. E.g., "EMP-00123"                                  |
| `first_name`                | `VARCHAR(100)`             | Not Null                                                               |
| `last_name`                 | `VARCHAR(100)`             | Not Null                                                               |
| `email`                     | `VARCHAR(255)`             | **Unique**, Not Null                                                   |
| `phone`                     | `VARCHAR(20)`              |                                                                        |
| `profile_image_url`         | `VARCHAR(512)`             | URL to the stored image                                                |
| `department_id`             | `INTEGER`                  | **Foreign Key** -> `departments.id`                                    |
| `designation_id`            | `INTEGER`                  | **Foreign Key** -> `designations.id`                                   |
| `manager_id`                | `INTEGER`                  | **Foreign Key** -> `employees.id` (Self-referencing)                   |
| `joining_date`              | `DATE`                     | Not Null                                                               |
| `probation_period`          | `VARCHAR(50)`              | E.g., "90 days"                                                        |
| `work_location_id`          | `INTEGER`                  | **Foreign Key** -> `company_units.id`                                  |
| `job_type_id`               | `INTEGER`                  | **Foreign Key** -> `job_types.id`                                      |
| `shift_timing`              | `VARCHAR(100)`             | E.g., "9:00 AM - 6:00 PM"                                              |
| `weekly_hours`              | `NUMERIC(5, 2)`            | E.g., 40.00                                                            |
| `annual_leave_total`        | `INTEGER`                  | Total allocated annual leave days                                      |
| `sick_leave_total`          | `INTEGER`                  | Total allocated sick leave days                                        |
| `casual_leave_total`        | `INTEGER`                  | Total allocated casual leave days                                      |
| `date_of_birth`             | `DATE`                     |                                                                        |
| `gender`                    | `VARCHAR(20)`              | E.g., "Male", "Female", "Other"                                        |
| `marital_status`            | `VARCHAR(20)`              | E.g., "Single", "Married"                                              |
| `address`                   | `TEXT`                     |                                                                        |
| `city`                      | `VARCHAR(100)`             |                                                                        |
| `state`                     | `VARCHAR(100)`             |                                                                        |
| `zip_code`                  | `VARCHAR(20)`              |                                                                        |
| `emergency_contact_name`    | `VARCHAR(200)`             |                                                                        |
| `emergency_contact_phone`   | `VARCHAR(20)`              |                                                                        |
| `salary`                    | `NUMERIC(12, 2)`           |                                                                        |
| `currency`                  | `VARCHAR(10)`              | E.g., "USD", "INR"                                                     |
| `pay_frequency`             | `VARCHAR(50)`              | E.g., "Monthly", "Bi-Weekly"                                           |
| `bank_account`              | `VARCHAR(100)`             | Encrypted                                                              |
| `bank_name`                 | `VARCHAR(100)`             |                                                                        |
| `tax_id`                    | `VARCHAR(100)`             | Encrypted                                                              |
| `benefits`                  | `JSONB`                    | Store array of benefits as JSON, e.g., `["Health Insurance", "401k"]`  |
| `is_active`                 | `BOOLEAN`                  | Default `true`                                                         |
| `created_at`                | `TIMESTAMP WITH TIME ZONE` | Default `NOW()`                                                        |
| `updated_at`                | `TIMESTAMP WITH TIME ZONE` | Default `NOW()`                                                        |

### Table: `company_units` (for Work Locations)

| Column Name | Data Type                  | Constraints & Notes |
| ----------- | -------------------------- | ------------------- |
| `id`        | `SERIAL`                   | **Primary Key** |
| `unit_name` | `VARCHAR(255)`             | **Unique**, Not Null|
| `address`   | `TEXT`                     |                     |
| `created_at`| `TIMESTAMP WITH TIME ZONE` | Default `NOW()`     |

### Table: `departments`

| Column Name | Data Type                  | Constraints & Notes |
| ----------- | -------------------------- | ------------------- |
| `id`        | `SERIAL`                   | **Primary Key** |
| `name`      | `VARCHAR(255)`             | **Unique**, Not Null|
| `created_at`| `TIMESTAMP WITH TIME ZONE` | Default `NOW()`     |

### Table: `designations` (for Positions/Job Titles)

| Column Name | Data Type                  | Constraints & Notes |
| ----------- | -------------------------- | ------------------- |
| `id`        | `SERIAL`                   | **Primary Key** |
| `title`     | `VARCHAR(255)`             | **Unique**, Not Null|
| `created_at`| `TIMESTAMP WITH TIME ZONE` | Default `NOW()`     |

### Table: `job_types` (for Employment Type)

| Column Name | Data Type                  | Constraints & Notes                                              |
| ----------- | -------------------------- | ---------------------------------------------------------------- |
| `id`        | `SERIAL`                   | **Primary Key** |
| `type_name` | `VARCHAR(100)`             | **Unique**, Not Null. E.g., "Full-Time", "Part-Time", "Contract" |
| `created_at`| `TIMESTAMP WITH TIME ZONE` | Default `NOW()`                                                  |


### Table: `leave_types`

Defines the types of leave available in the organization.

| Column Name  | Data Type      | Constraints & Notes                            |
| ------------ | -------------- | ---------------------------------------------- |
| `id`         | `SERIAL`       | **Primary Key** |
| `name`       | `VARCHAR(100)` | **Unique**, Not Null. E.g., "Sick", "Annual"   |
| `created_at` | `TIMESTAMP`    | Default `NOW()`                                |

### Table: `leave_policies`

Defines different leave policies that can be assigned to employees.

| Column Name   | Data Type      | Constraints & Notes                               |
| ------------- | -------------- | ------------------------------------------------- |
| `id`          | `SERIAL`       | **Primary Key** |
| `policy_name` | `VARCHAR(150)` | **Unique**, Not Null. E.g., "Standard Full-Time"  |
| `details`     | `JSONB`        | Stores allocations, e.g., `[{"leave_type_id": 1, "days_allocated": 12}, {"leave_type_id": 2, "days_allocated": 15}]` |
| `created_at`  | `TIMESTAMP`    | Default `NOW()`   

### Table: `leaves`

| Column Name      | Data Type                  | Constraints & Notes                                        |
| ---------------- | -------------------------- | ---------------------------------------------------------- |
| `id`             | `SERIAL`                   | **Primary Key** |
| `employee_id`    | `INTEGER`                  | **Foreign Key** -> `employees.id`, Not Null                |
| `leave_type`     | `VARCHAR(50)`              | E.g., "Annual", "Sick", "Casual"                           |
| `start_date`     | `DATE`                     | Not Null                                                   |
| `end_date`       | `DATE`                     | Not Null                                                   |
| `reason`         | `TEXT`                     |                                                            |
| `status`         | `VARCHAR(50)`              | E.g., "Pending", "Approved", "Rejected". Default "Pending" |
| `approved_by_id` | `INTEGER`                  | **Foreign Key** -> `employees.id`                          |
| `created_at`     | `TIMESTAMP WITH TIME ZONE` | Default `NOW()`                                            |

### Table: `attendance`

| Column Name   | Data Type                  | Constraints & Notes                         |
| ------------- | -------------------------- | ------------------------------------------- |
| `id`          | `SERIAL`                   | **Primary Key** |
| `employee_id` | `INTEGER`                  | **Foreign Key** -> `employees.id`, Not Null |
| `date`        | `DATE`                     | Not Null                                    |
| `check_in`    | `TIMESTAMP WITH TIME ZONE` |                                             |
| `check_out`   | `TIMESTAMP WITH TIME ZONE` |                                             |
| `status`      | `VARCHAR(50)`              | E.g., "Present", "Absent", "On Leave"       |
| `notes`       | `TEXT`                     | For manual overrides or notes               |
| **Unique Constraint**: (`employee_id`, `date`) |                                            |

---

## 4. API Endpoints

All endpoints should be prefixed with `/api/v1`. All responses should be in JSON format. Proper HTTP status codes must be used (e.g., `200 OK`, `201 Created`, `404 Not Found`, `422 Unprocessable Entity`). Authorization logic (e.g., ensuring a manager can only approve leave for their own team) should be handled within the API endpoints by checking the user `role` and `employee_id` passed from the gateway.

### 4.1. Employee Management (`/employees`)

* **`POST /employees`**: Create a new employee.
* **`GET /employees`**: Get a list of all employees with pagination and filtering (by department, designation, etc.).
* **`GET /employees/{employee_id}`**: Get details for a specific employee.
* **`PUT /employees/{employee_id}`**: Update details for a specific employee.
* **`DELETE /employees/{employee_id}`**: Deactivate an employee (soft delete by setting `is_active` to `false`).

### 4.2. Department Management (`/departments`)

* **`POST /departments`**: Create a new department.
* **`GET /departments`**: Get a list of all departments.
* **`GET /departments/{department_id}`**: Get details for a specific department.
* **`PUT /departments/{department_id}`**: Update a department's name.
* **`DELETE /departments/{department_id}`**: Delete a department (only if no employees are assigned).

### 4.3. Designation Management (`/designations`)

* **`POST /designations`**: Create a new designation.
* **`GET /designations`**: Get a list of all designations.
* **`PUT /designations/{designation_id}`**: Update a designation's title.
* **`DELETE /designations/{designation_id}`**: Delete a designation (only if no employees are assigned).

### 4.4. Leave Management (`/leaves`)

* **`POST /leaves/apply`**: An employee applies for leave.
* **`GET /leaves/employee/{employee_id}`**: Get all leave requests for a specific employee.
* **`GET /leaves/pending`**: Get all pending leave requests (for managers/HR).
* **`POST /leaves/{leave_id}/approve`**: Approve a leave request.
* **`POST /leaves/{leave_id}/reject`**: Reject a leave request.

### 4.5. Attendance Management (`/attendance`)

* **`POST /attendance/check-in`**: Record an employee's check-in time.
* **`POST /attendance/check-out`**: Record an employee's check-out time.
* **`GET /attendance/employee/{employee_id}`**: Get attendance records for a specific employee for a given date range.
* **`POST /attendance/manual`**: Manually add or update an attendance record (for HR/admin).

---

## 5. Non-Functional Requirements

* **Security**: Sensitive data (bank info, tax id) must be encrypted in the database. Implement protection against common vulnerabilities like SQL Injection.
* **Error Handling**: Consistent error response format across the API.
* **Logging**: Implement comprehensive logging for requests, errors, and important application events.
* **Testing**: Unit and integration tests should be written to ensure code quality and reliability.