# Database Table Relationships for HRMS Frontend

This document outlines the relationships between the database tables (models) in the HRMS backend. Understanding these relationships is crucial for designing and developing the frontend, especially when dealing with data fetching, displaying related information, and managing forms for linked entities.

---

## Table: `attendance`

Represents employee attendance records.

| Column Name   | Type      | Constraints / Notes                               |
| :------------ | :-------- | :------------------------------------------------ |
| `id`          | `Integer` | Primary Key, Auto-increment                       |
| `employee_id` | `Integer` | Foreign Key to `employees.id`, Not Null           |
| `date`        | `Date`    | Not Null                                          |
| `check_in`    | `DateTime`| Optional (with timezone)                          |
| `check_out`   | `DateTime`| Optional (with timezone)                          |
| `status`      | `String`  | Max length 50                                     |
| `notes`       | `Text`    | Optional                                          |

**Relationships:**

*   **Many-to-One with `employees`**: An attendance record belongs to one employee.
    *   `employee_id` (FK) -> `employees.id` (PK)
    *   Python relationship: `employee = relationship("Employee", back_populates="attendance_records")`

**Unique Constraints:**

*   `uq_employee_date`: Ensures that an employee can only have one attendance record per day.
    *   (`employee_id`, `date`)

---

## Table: `company_units`

Represents different company locations or units.

| Column Name | Type      | Constraints / Notes                               |
| :---------- | :-------- | :------------------------------------------------ |
| `id`        | `Integer` | Primary Key, Auto-increment                       |
| `unit_name` | `String`  | Max length 255, Unique, Not Null                  |
| `address`   | `Text`    | Optional                                          |
| `created_at`| `DateTime`| Auto-generated timestamp (server default)         |

**Relationships:**

*   **One-to-Many with `employees`**: A company unit can have multiple employees associated with it.
    *   Python relationship: `employees = relationship("Employee", back_populates="work_location")`

---

## Table: `departments`

Represents different departments within the company.

| Column Name | Type      | Constraints / Notes                               |
| :---------- | :-------- | :------------------------------------------------ |
| `id`        | `Integer` | Primary Key, Auto-increment                       |
| `name`      | `String`  | Max length 255, Unique, Not Null                  |
| `created_at`| `DateTime`| Auto-generated timestamp (server default)         |

**Relationships:**

*   **One-to-Many with `employees`**: A department can have multiple employees associated with it.
    *   Python relationship: `employees = relationship("Employee", back_populates="department", foreign_keys="Employee.department_id")`

---

## Table: `designations`

Represents different job designations within the company.

| Column Name | Type      | Constraints / Notes                               |
| :---------- | :-------- | :------------------------------------------------ |
| `id`        | `Integer` | Primary Key, Auto-increment                       |
| `title`     | `String`  | Max length 255, Unique, Not Null                  |
| `created_at`| `DateTime`| Auto-generated timestamp (server default)         |

**Relationships:**

*   **One-to-Many with `employees`**: A designation can be held by multiple employees.
    *   Python relationship: `employees = relationship("Employee", back_populates="designation")`

---

## Table: `employees`

Represents employee records, including personal and employment details.

| Column Name             | Type      | Constraints / Notes                               |
| :---------------------- | :-------- | :------------------------------------------------ |
| `id`                    | `Integer` | Primary Key, Auto-increment                       |
| `employee_id`           | `String`  | Max length 50, Unique, Not Null                   |
| `first_name`            | `String`  | Max length 100, Not Null                          |
| `last_name`             | `String`  | Max length 100, Not Null                          |
| `email`                 | `String`  | Max length 255, Unique, Not Null                  |
| `phone`                 | `String`  | Max length 20                                     |
| `profile_image_url`     | `String`  | Max length 512                                    |
| `department_id`         | `Integer` | Foreign Key to `departments.id`                   |
| `designation_id`        | `Integer` | Foreign Key to `designations.id`                  |
| `manager_id`            | `Integer` | Foreign Key to `employees.id` (Self-referencing)  |
| `joining_date`          | `Date`    | Not Null                                          |
| `probation_period`      | `String`  | Max length 50                                     |
| `work_location_id`      | `Integer` | Foreign Key to `company_units.id`                 |
| `job_type_id`           | `Integer` | Foreign Key to `job_types.id`                     |
| `shift_timing`          | `String`  | Max length 100                                    |
| `weekly_hours`          | `Numeric` | Precision 5, Scale 2                              |
| `annual_leave_total`    | `Integer` |                                                   |
| `sick_leave_total`      | `Integer` |                                                   |
| `casual_leave_total`    | `Integer` |                                                   |
| `date_of_birth`         | `Date`    |                                                   |
| `gender`                | `String`  | Max length 20                                     |
| `marital_status`        | `String`  | Max length 20                                     |
| `address`               | `Text`    |                                                   |
| `city`                  | `String`  | Max length 100                                    |
| `state`                 | `String`  | Max length 100                                    |
| `zip_code`              | `String`  | Max length 20                                     |
| `emergency_contact_name`| `String`  | Max length 200                                    |
| `emergency_contact_phone`| `String`  | Max length 20                                     |
| `salary`                | `Numeric` | Precision 12, Scale 2                             |
| `currency`              | `String`  | Max length 10                                     |
| `pay_frequency`         | `String`  | Max length 50                                     |
| `bank_account`          | `String`  | Max length 100 (should be encrypted)              |
| `bank_name`             | `String`  | Max length 100                                    |
| `tax_id`                | `String`  | Max length 100 (should be encrypted)              |
| `benefits`              | `JSONB`   | Stores JSON data for employee benefits            |
| `is_active`             | `Boolean` | Default True                                      |
| `created_at`            | `DateTime`| Auto-generated timestamp (server default)         |
| `updated_at`            | `DateTime`| Auto-generated timestamp (server default, on update)|

**Relationships:**

*   **Many-to-One with `departments`**: An employee belongs to one department.
    *   `employees.department_id` (FK) -> `departments.id` (PK)
    *   Python relationship: `department = relationship("Department", back_populates="employees")`
*   **Many-to-One with `designations`**: An employee has one designation.
    *   `employees.designation_id` (FK) -> `designations.id` (PK)
    *   Python relationship: `designation = relationship("Designation", back_populates="employees")`
*   **Self-referencing Many-to-One with `employees` (Manager)**: An employee can have one manager (who is also an employee).
    *   `employees.manager_id` (FK) -> `employees.id` (PK)
    *   Python relationship: `manager = relationship("Employee", remote_side=[id], back_populates="subordinates")`
*   **Self-referencing One-to-Many with `employees` (Subordinates)**: An employee (manager) can have many subordinates (employees).
    *   `employees.id` (PK) -> `employees.manager_id` (FK)
    *   Python relationship: `subordinates = relationship("Employee", back_populates="manager", foreign_keys=[manager_id])`
*   **Many-to-One with `company_units`**: An employee works at one company unit.
    *   `employees.work_location_id` (FK) -> `company_units.id` (PK)
    *   Python relationship: `work_location = relationship("CompanyUnit", back_populates="employees")`
*   **Many-to-One with `job_types`**: An employee has one job type.
    *   `employees.job_type_id` (FK) -> `job_types.id` (PK)
    *   Python relationship: `job_type = relationship("JobType", back_populates="employees")`
*   **One-to-Many with `leaves`**: An employee can have multiple leave records.
    *   `employees.id` (PK) -> `leaves.employee_id` (FK)
    *   Python relationship: `leaves = relationship("Leave", back_populates="employee", foreign_keys=[Leave.employee_id])`
*   **One-to-Many with `leaves` (Approved Leaves)**: An employee can approve multiple leave records.
    *   `employees.id` (PK) -> `leaves.approved_by_id` (FK)
    *   Python relationship: `approved_leaves = relationship("Leave", foreign_keys=[Leave.approved_by_id], back_populates="approver")`
*   **One-to-Many with `attendance`**: An employee can have multiple attendance records.
    *   `employees.id` (PK) -> `attendance.employee_id` (FK)
    *   Python relationship: `attendance_records = relationship("Attendance", back_populates="employee")`

---

## Table: `job_types`

Represents different types of jobs or employment (e.g., Full-time, Part-time, Contract).

| Column Name | Type      | Constraints / Notes                               |
| :---------- | :-------- | :------------------------------------------------ |
| `id`        | `Integer` | Primary Key, Auto-increment                       |
| `type_name` | `String`  | Max length 100, Unique, Not Null                  |
| `created_at`| `DateTime`| Auto-generated timestamp (server default)         |

**Relationships:**

*   **One-to-Many with `employees`**: A job type can be associated with multiple employees.
    *   Python relationship: `employees = relationship("Employee", back_populates="job_type")`

---

## Table: `leaves`

Represents employee leave requests and their status.

| Column Name    | Type      | Constraints / Notes                               |
| :------------- | :-------- | :------------------------------------------------ |
| `id`           | `Integer` | Primary Key, Auto-increment                       |
| `employee_id`  | `Integer` | Foreign Key to `employees.id`, Not Null           |
| `leave_type`   | `String`  | Max length 50                                     |
| `start_date`   | `Date`    | Not Null                                          |
| `end_date`     | `Date`    | Not Null                                          |
| `reason`       | `Text`    | Optional                                          |
| `status`       | `String`  | Max length 50, Default "Pending"                  |
| `approved_by_id`| `Integer` | Foreign Key to `employees.id` (Self-referencing)  |
| `created_at`   | `DateTime`| Auto-generated timestamp (server default)         |

**Relationships:**

*   **Many-to-One with `employees` (Employee)**: A leave record belongs to one employee.
    *   `leaves.employee_id` (FK) -> `employees.id` (PK)
    *   Python relationship: `employee = relationship("Employee", back_populates="leaves", foreign_keys=[employee_id])`
*   **Many-to-One with `employees` (Approver)**: The approver of a leave record is an employee.
    *   `leaves.approved_by_id` (FK) -> `employees.id` (PK)
    *   Python relationship: `approver = relationship("Employee", foreign_keys=[approved_by_id], back_populates="approved_leaves")`

---

## Table: `leave_policies`

Represents different leave policies (e.g., Annual Leave Policy, Sick Leave Policy).

| Column Name   | Type      | Constraints / Notes                               |
| :------------ | :-------- | :------------------------------------------------ |
| `id`          | `Integer` | Primary Key, Auto-increment                       |
| `policy_name` | `String`  | Max length 150, Unique, Not Null                  |
| `details`     | `JSONB`   | Stores JSON data for policy details (e.g., number of days) |
| `created_at`  | `DateTime`| Auto-generated timestamp (server default)         |

**Relationships:**

*   No direct relationships defined in this model.

---

## Table: `leave_types`

Represents different categories of leave (e.g., Annual, Sick, Casual).

| Column Name | Type      | Constraints / Notes                               |
| :---------- | :-------- | :------------------------------------------------ |
| `id`        | `Integer` | Primary Key, Auto-increment                       |
| `name`      | `String`  | Max length 100, Unique, Not Null                  |
| `created_at`| `DateTime`| Auto-generated timestamp (server default)         |

**Relationships:**

*   No direct relationships defined in this model. (Likely referenced by `leaves.leave_type` but not explicitly defined as a relationship in this model).
