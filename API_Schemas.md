# API Schemas for HRMS Frontend

This document outlines the data structures (schemas) used by the HRMS backend API, providing TypeScript equivalents for frontend development.

---

## Attendance API

### `AttendanceBase`

Base schema for attendance records.

| Field          | Python Type      | TypeScript Type | Description                               |
| :------------- | :--------------- | :-------------- | :---------------------------------------- |
| `employee_id`  | `int`            | `number`        | The ID of the employee.                   |
| `date`         | `date`           | `string`        | The date of the attendance record (ISO 8601 format: YYYY-MM-DD). |
| `check_in`     | `Optional[date]` | `string | null`  | The check-in time (ISO 8601 format: YYYY-MM-DDTHH:MM:SS.sssZ). |
| `check_out`    | `Optional[date]` | `string | null`  | The check-out time (ISO 8601 format: YYYY-MM-DDTHH:MM:SS.sssZ). |
| `status`       | `str`            | `string`        | The attendance status (e.g., "Present", "Absent", "Leave"). |
| `notes`        | `Optional[str]`  | `string | null`  | Additional notes for the attendance record. |

```typescript
interface AttendanceBase {
  employee_id: number;
  date: string; // YYYY-MM-DD
  check_in: string | null; // YYYY-MM-DDTHH:MM:SS.sssZ
  check_out: string | null; // YYYY-MM-DDTHH:MM:SS.sssZ
  status: string;
  notes: string | null;
}
```

### `AttendanceCreate`

Schema for creating a new attendance record. Inherits from `AttendanceBase`.

```typescript
interface AttendanceCreate extends AttendanceBase {}
```

### `AttendanceUpdate`

Schema for updating an existing attendance record. All fields are optional.

| Field          | Python Type      | TypeScript Type | Description                               |
| :------------- | :--------------- | :-------------- | :---------------------------------------- |
| `employee_id`  | `Optional[int]`  | `number | null`  | The ID of the employee.                   |
| `date`         | `Optional[date]` | `string | null`  | The date of the attendance record (ISO 8601 format: YYYY-MM-DD). |
| `check_in`     | `Optional[date]` | `string | null`  | The check-in time (ISO 8601 format: YYYY-MM-DDTHH:MM:SS.sssZ). |
| `check_out`    | `Optional[date]` | `string | null`  | The check-out time (ISO 8601 format: YYYY-MM-DDTHH:MM:SS.sssZ). |
| `status`       | `Optional[str]`  | `string | null`  | The attendance status (e.g., "Present", "Absent", "Leave"). |
| `notes`        | `Optional[str]`  | `string | null`  | Additional notes for the attendance record. |

```typescript
interface AttendanceUpdate {
  employee_id?: number | null;
  date?: string | null; // YYYY-MM-DD
  check_in?: string | null; // YYYY-MM-DDTHH:MM:SS.sssZ
  check_out?: string | null; // YYYY-MM-DDTHH:MM:SS.sssZ
  status?: string | null;
  notes?: string | null;
}
```

### `Attendance`

Full schema for an attendance record, including the `id` assigned by the database. Inherits from `AttendanceBase`.

| Field | Python Type | TypeScript Type | Description      |
| :---- | :---------- | :-------------- | :--------------- |
| `id`  | `int`       | `number`        | The unique ID of the attendance record. |

```typescript
interface Attendance extends AttendanceBase {
  id: number;
}
```

---

## Company Unit API

### `CompanyUnitBase`

Base schema for company units.

| Field       | Python Type      | TypeScript Type | Description             |
| :---------- | :--------------- | :-------------- | :---------------------- |
| `unit_name` | `str`            | `string`        | The name of the company unit. |
| `address`   | `Optional[str]`  | `string | null`  | The address of the company unit. |

```typescript
interface CompanyUnitBase {
  unit_name: string;
  address: string | null;
}
```

### `CompanyUnitCreate`

Schema for creating a new company unit. Inherits from `CompanyUnitBase`.

```typescript
interface CompanyUnitCreate extends CompanyUnitBase {}
```

### `CompanyUnit`

Full schema for a company unit, including the `id` assigned by the database. Inherits from `CompanyUnitBase`.

| Field | Python Type | TypeScript Type | Description      |
| :---- | :---------- | :-------------- | :--------------- |
| `id`  | `int`       | `number`        | The unique ID of the company unit. |

```typescript
interface CompanyUnit extends CompanyUnitBase {
  id: number;
}
```

---

## Department API

### `DepartmentBase`

Base schema for departments.

| Field | Python Type | TypeScript Type | Description      |
| :---- | :---------- | :-------------- | :--------------- |
| `name`| `str`       | `string`        | The name of the department. |

```typescript
interface DepartmentBase {
  name: string;
}
```

### `DepartmentCreate`

Schema for creating a new department. Inherits from `DepartmentBase`.

```typescript
interface DepartmentCreate extends DepartmentBase {}
```

### `Department`

Full schema for a department, including the `id` assigned by the database. Inherits from `DepartmentBase`.

| Field | Python Type | TypeScript Type | Description      |
| :---- | :---------- | :--------------- | :--------------- |
| `id`  | `int`       | `number`        | The unique ID of the department. |

```typescript
interface Department extends DepartmentBase {
  id: number;
}
```

---

## Designation API

### `DesignationBase`

Base schema for designations.

| Field | Python Type | TypeScript Type | Description      |
| :---- | :---------- | :-------------- | :--------------- |
| `title`| `str`       | `string`        | The title of the designation. |

```typescript
interface DesignationBase {
  title: string;
}
```

### `DesignationCreate`

Schema for creating a new designation. Inherits from `DesignationBase`.

```typescript
interface DesignationCreate extends DesignationBase {}
```

### `Designation`

Full schema for a designation, including the `id` assigned by the database. Inherits from `DesignationBase`.

| Field | Python Type | TypeScript Type | Description      |
| :---- | :---------- | :--------------- | :--------------- |
| `id`  | `int`       | `number`        | The unique ID of the designation. |

```typescript
interface Designation extends DesignationBase {
  id: number;
}
```

---

## Employee API

### `EmployeeBase`

Base schema for employee records.

| Field                    | Python Type      | TypeScript Type        | Description                               |
| :----------------------- | :--------------- | :--------------------- | :---------------------------------------- |
| `first_name`             | `str`            | `string`               | Employee's first name.                    |
| `last_name`              | `str`            | `string`               | Employee's last name.                     |
| `email`                  | `EmailStr`       | `string`               | Employee's email address.                 |
| `phone`                  | `str`            | `string`               | Employee's phone number.                  |
| `employee_id`            | `str`            | `string`               | Unique employee identifier.               |
| `department_id`          | `int`            | `number`               | ID of the department the employee belongs to. |
| `designation_id`         | `int`            | `number`               | ID of the employee's designation.         |
| `joining_date`           | `date`           | `string`               | Date when the employee joined (ISO 8601 format: YYYY-MM-DD). |
| `profile_image_url`      | `Optional[str]`  | `string \| null`       | URL to the employee's profile image.      |
| `manager_id`             | `Optional[int]`  | `number \| null`       | ID of the employee's manager.             |
| `probation_period`       | `Optional[str]`  | `string \| null`       | Duration of the probation period.         |
| `work_location_id`       | `Optional[int]`  | `number \| null``       | ID of the employee's work location.       |
| `job_type_id`            | `Optional[int]`  | `number \| null`       | ID of the employee's job type.            |
| `shift_timing`           | `Optional[str]`  | `string \| null`       | Employee's shift timing.                  |
| `weekly_hours`           | `Optional[float]`| `number \| null`       | Number of weekly working hours.           |
| `annual_leave_total`     | `Optional[int]`  | `number \| null`       | Total annual leave days.                  |
| `sick_leave_total`       | `Optional[int]`  | `number \| null`       | Total sick leave days.                    |
| `casual_leave_total`     | `Optional[int]`  | `number \| null`       | Total casual leave days.                  |
| `date_of_birth`          | `Optional[date]` | `string \| null`       | Employee's date of birth (ISO 8601 format: YYYY-MM-DD). |
| `gender`                 | `Optional[str]`  | `string \| null`       | Employee's gender.                        |
| `marital_status`         | `Optional[str]`  | `string \| null`       | Employee's marital status.                |
| `address`                | `Optional[str]`  | `string \| null`       | Employee's address.                       |
| `city`                   | `Optional[str]`  | `string \| null`       | Employee's city.                          |
| `state`                  | `Optional[str]`  | `string \| null`       | Employee's state.                         |
| `zip_code`               | `Optional[str]`  | `string \| null`       | Employee's zip code.                      |
| `emergency_contact_name` | `Optional[str]`  | `string \| null`       | Name of emergency contact.                |
| `emergency_contact_phone`| `Optional[str]`  | `string \| null`       | Phone number of emergency contact.        |
| `salary`                 | `Optional[float]`| `number \| null`       | Employee's salary.                        |
| `currency`               | `Optional[str]`  | `string \| null`       | Currency of the salary.                   |
| `pay_frequency`          | `Optional[str]`  | `string \| null`       | Frequency of salary payment.              |
| `bank_account`           | `Optional[str]`  | `string \| null`       | Employee's bank account number.           |
| `bank_name`              | `Optional[str]`  | `string \| null`       | Name of the bank.                         |
| `tax_id`                 | `Optional[str]`  | `string \| null`       | Employee's tax identifier.                |
| `benefits`               | `Optional[dict]` | `Record<string, any> \| null` | Employee's benefits information.          |
| `is_active`              | `bool`           | `boolean`              | Indicates if the employee is active.      |

```typescript
interface EmployeeBase {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  employee_id: string;
  department_id: number;
  designation_id: number;
  joining_date: string; // YYYY-MM-DD
  profile_image_url: string | null;
  manager_id: number | null;
  probation_period: string | null;
  work_location_id: number | null;
  job_type_id: number | null;
  shift_timing: string | null;
  weekly_hours: number | null;
  annual_leave_total: number | null;
  sick_leave_total: number | null;
  casual_leave_total: number | null;
  date_of_birth: string | null; // YYYY-MM-DD
  gender: string | null;
  marital_status: string | null;
  address: string | null;
  city: string | null;
  state: string | null;
  zip_code: string | null;
  emergency_contact_name: string | null;
  emergency_contact_phone: string | null;
  salary: number | null;
  currency: string | null;
  pay_frequency: string | null;
  bank_account: string | null;
  bank_name: string | null;
  tax_id: string | null;
  benefits: Record<string, any> | null;
  is_active: boolean;
}
```

### `EmployeeCreate`

Schema for creating a new employee record. Inherits from `EmployeeBase`.

```typescript
interface EmployeeCreate extends EmployeeBase {}
```

### `EmployeeUpdate`

Schema for updating an existing employee record. All fields are optional.

| Field                    | Python Type      | TypeScript Type        | Description                               |
| :----------------------- | :--------------- | :--------------------- | :---------------------------------------- |
| `first_name`             | `Optional[str]`  | `string \| null`       | Employee's first name.                    |
| `last_name`              | `Optional[str]`  | `string \| null`       | Employee's last name.                     |
| `email`                  | `Optional[EmailStr]`| `string \| null`       | Employee's email address.                 |
| `phone`                  | `Optional[str]`  | `string \| null`       | Employee's phone number.                  |
| `employee_id`            | `Optional[str]`  | `string \| null`       | Unique employee identifier.               |
| `department_id`          | `Optional[int]`  | `number \| null`       | ID of the department the employee belongs to. |
| `designation_id`         | `Optional[int]`  | `number \| null`       | ID of the employee's designation.         |
| `joining_date`           | `Optional[date]` | `string \| null`       | Date when the employee joined (ISO 8601 format: YYYY-MM-DD). |
| `profile_image_url`      | `Optional[str]`  | `string \| null`       | URL to the employee's profile image.      |
| `manager_id`             | `Optional[int]`  | `number \| null`       | ID of the employee's manager.             |
| `probation_period`       | `Optional[str]`  | `string \| null`       | Duration of the probation period.         |
| `work_location_id`       | `Optional[int]`  | `number \| null`       | ID of the employee's work location.       |
| `job_type_id`            | `Optional[int]`  | `number \| null`       | ID of the employee's job type.            |
| `shift_timing`           | `Optional[str]`  | `string \| null`       | Employee's shift timing.                  |
| `weekly_hours`           | `Optional[float]`| `number \| null`       | Number of weekly working hours.           |
| `annual_leave_total`     | `Optional[int]`  | `number \| null`       | Total annual leave days.                  |
| `sick_leave_total`       | `Optional[int]`  | `number \| null`       | Total sick leave days.                    |
| `casual_leave_total`     | `Optional[int]`  | `number \| null`       | Total casual leave days.                  |
| `date_of_birth`          | `Optional[date]` | `string \| null`       | Employee's date of birth (ISO 8601 format: YYYY-MM-DD). |
| `gender`                 | `Optional[str]`  | `string \| null`       | Employee's gender.                        |
| `marital_status`         | `Optional[str]`  | `string \| null`       | Employee's marital status.                |
| `address`                | `Optional[str]`  | `string \| null`       | Employee's address.                       |
| `city`                   | `Optional[str]`  | `string \| null`       | Employee's city.                          |
| `state`                  | `Optional[str]`  | `string \| null`       | Employee's state.                         |
| `zip_code`               | `Optional[str]`  | `string \| null`       | Employee's zip code.                      |
| `emergency_contact_name` | `Optional[str]`  | `string \| null`       | Name of emergency contact.                |
| `emergency_contact_phone`| `Optional[str]`  | `string \| null`       | Phone number of emergency contact.        |
| `salary`                 | `Optional[float]`| `number \| null`       | Employee's salary.                        |
| `currency`               | `Optional[str]`  | `string \| null`       | Currency of the salary.                   |
| `pay_frequency`          | `Optional[str]`  | `string \| null`       | Frequency of salary payment.              |
| `bank_account`           | `Optional[str]`  | `string \| null`       | Employee's bank account number.           |
| `bank_name`              | `Optional[str]`  | `string \| null`       | Name of the bank.                         |
| `tax_id`                 | `Optional[str]`  | `string \| null`       | Employee's tax identifier.                |
| `benefits`               | `Optional[dict]` | `Record<string, any> \| null` | Employee's benefits information.          |
| `is_active`              | `Optional[bool]` | `boolean \| null`      | Indicates if the employee is active.      |

```typescript
interface EmployeeUpdate {
  first_name?: string | null;
  last_name?: string | null;
  email?: string | null;
  phone?: string | null;
  employee_id?: string | null;
  department_id?: number | null;
  designation_id?: number | null;
  joining_date?: string | null; // YYYY-MM-DD
  profile_image_url?: string | null;
  manager_id?: number | null;
  probation_period?: string | null;
  work_location_id?: number | null;
  job_type_id?: number | null;
  shift_timing?: string | null;
  weekly_hours?: number | null;
  annual_leave_total?: number | null;
  sick_leave_total?: number | null;
  casual_leave_total?: number | null;
  date_of_birth?: string | null; // YYYY-MM-DD
  gender?: string | null;
  marital_status?: string | null;
  address?: string | null;
  city?: string | null;
  state?: string | null;
  zip_code?: string | null;
  emergency_contact_name?: string | null;
  emergency_contact_phone?: string | null;
  salary?: number | null;
  currency?: string | null;
  pay_frequency?: string | null;
  bank_account?: string | null;
  bank_name?: string | null;
  tax_id?: string | null;
  benefits?: Record<string, any> | null;
  is_active?: boolean | null;
}
```

### `Employee`

Full schema for an employee record, including the `id` assigned by the database. Inherits from `EmployeeBase`.

| Field | Python Type | TypeScript Type | Description      |
| :---- | :---------- | :-------------- | :--------------- |
| `id`  | `int`       | `number`        | The unique ID of the employee. |

```typescript
interface Employee extends EmployeeBase {
  id: number;
}
```

---

## Job Type API

### `JobTypeBase`

Base schema for job types.

| Field       | Python Type | TypeScript Type | Description      |
| :---------- | :---------- | :-------------- | :--------------- |
| `type_name` | `str`       | `string`        | The name of the job type. |

```typescript
interface JobTypeBase {
  type_name: string;
}
```

### `JobTypeCreate`

Schema for creating a new job type. Inherits from `JobTypeBase`.

```typescript
interface JobTypeCreate extends JobTypeBase {}
```

### `JobType`

Full schema for a job type, including the `id` assigned by the database. Inherits from `JobTypeBase`.

| Field | Python Type | TypeScript Type | Description      |
| :---- | :---------- | :-------------- | :--------------- |
| `id`  | `int`       | `number`        | The unique ID of the job type. |

```typescript
interface JobType extends JobTypeBase {
  id: number;
}
```

---

## Leave API

### `LeaveBase`

Base schema for leave records.

| Field          | Python Type      | TypeScript Type | Description                               |
| :------------- | :--------------- | :-------------- | :---------------------------------------- |
| `employee_id`  | `int`            | `number`        | The ID of the employee.                   |
| `leave_type`   | `str`            | `string`        | The type of leave (e.g., "Annual Leave", "Sick Leave"). |
| `start_date`   | `date`           | `string`        | The start date of the leave (ISO 8601 format: YYYY-MM-DD). |
| `end_date`     | `date`           | `string`        | The end date of the leave (ISO 8601 format: YYYY-MM-DD). |
| `reason`       | `Optional[str]`  | `string | null`  | The reason for the leave.                 |
| `status`       | `str`            | `string`        | The status of the leave (e.g., "Pending", "Approved", "Rejected"). |
| `approved_by_id`| `Optional[int]`  | `number | null`  | The ID of the person who approved the leave. |

```typescript
interface LeaveBase {
  employee_id: number;
  leave_type: string;
  start_date: string; // YYYY-MM-DD
  end_date: string; // YYYY-MM-DD
  reason: string | null;
  status: string;
  approved_by_id: number | null;
}
```

### `LeaveCreate`

Schema for creating a new leave record. Inherits from `LeaveBase`.

```typescript
interface LeaveCreate extends LeaveBase {}
```

### `LeaveUpdate`

Schema for updating an existing leave record. All fields are optional.

| Field          | Python Type      | TypeScript Type | Description                               |
| :------------- | :--------------- | :-------------- | :---------------------------------------- |
| `employee_id`  | `Optional[int]`  | `number | null`  | The ID of the employee.                   |
| `leave_type`   | `Optional[str]`  | `string | null`  | The type of leave (e.g., "Annual Leave", "Sick Leave"). |
| `start_date`   | `Optional[date]` | `string | null`  | The start date of the leave (ISO 8601 format: YYYY-MM-DD). |
| `end_date`     | `Optional[date]` | `string | null`  | The end date of the leave (ISO 8601 format: YYYY-MM-DD). |
| `reason`       | `Optional[str]`  | `string | null`  | The reason for the leave.                 |
| `status`       | `Optional[str]`  | `string | null`  | The status of the leave (e.g., "Pending", "Approved", "Rejected"). |
| `approved_by_id`| `Optional[int]`  | `number | null`  | The ID of the person who approved the leave. |

```typescript
interface LeaveUpdate {
  employee_id?: number | null;
  leave_type?: string | null;
  start_date?: string | null; // YYYY-MM-DD
  end_date?: string | null; // YYYY-MM-DD
  reason?: string | null;
  status?: string | null;
  approved_by_id?: number | null;
}
```

### `Leave`

Full schema for a leave record, including the `id` assigned by the database. Inherits from `LeaveBase`.

| Field | Python Type | TypeScript Type | Description      |
| :---- | :---------- | :-------------- | :--------------- |
| `id`  | `int`       | `number`        | The unique ID of the leave record. |

```typescript
interface Leave extends LeaveBase {
  id: number;
}
```

---

## Leave Policy API

### `LeavePolicyBase`

Base schema for leave policies.

| Field         | Python Type | TypeScript Type        | Description             |
| :------------ | :---------- | :--------------------- | :---------------------- |
| `policy_name` | `str`       | `string`               | The name of the leave policy. |
| `details`     | `dict`      | `Record<string, any>`  | Details of the leave policy (e.g., annual leave days, sick leave days). |

```typescript
interface LeavePolicyBase {
  policy_name: string;
  details: Record<string, any>;
}
```

### `LeavePolicyCreate`

Schema for creating a new leave policy. Inherits from `LeavePolicyBase`.

```typescript
interface LeavePolicyCreate extends LeavePolicyBase {}
```

### `LeavePolicyUpdate`

Schema for updating an existing leave policy. All fields are optional.

| Field         | Python Type      | TypeScript Type        | Description             |
| :------------ | :--------------- | :--------------------- | :---------------------- |
| `policy_name` | `Optional[str]`  | `string \| null`       | The name of the leave policy. |
| `details`     | `Optional[dict]` | `Record<string, any> \| null` | Details of the leave policy. |

```typescript
interface LeavePolicyUpdate {
  policy_name?: string | null;
  details?: Record<string, any> | null;
}
```

### `LeavePolicy`

Full schema for a leave policy, including the `id` assigned by the database. Inherits from `LeavePolicyBase`.

| Field | Python Type | TypeScript Type | Description      |
| :---- | :---------- | :-------------- | :--------------- |
| `id`  | `int`       | `number`        | The unique ID of the leave policy. |

```typescript
interface LeavePolicy extends LeavePolicyBase {
  id: number;
}
```

---

## Leave Type API

### `LeaveTypeBase`

Base schema for leave types.

| Field | Python Type | TypeScript Type | Description      |
| :---- | :---------- | :-------------- | :--------------- |
| `name`| `str`       | `string`        | The name of the leave type. |

```typescript
interface LeaveTypeBase {
  name: string;
}
```

### `LeaveTypeCreate`

Schema for creating a new leave type. Inherits from `LeaveTypeBase`.

```typescript
interface LeaveTypeCreate extends LeaveTypeBase {}
```

### `LeaveType`

Full schema for a leave type, including the `id` assigned by the database. Inherits from `LeaveTypeBase`.

| Field | Python Type | TypeScript Type | Description      |
| :---- | :---------- | :--------------- | :--------------- |
| `id`  | `int`       | `number`        | The unique ID of the leave type. |

```typescript
interface LeaveType extends LeaveTypeBase {
  id: number;
}
```

---

## Health API

The Health API provides a simple endpoint to check the application's status.

### `/api/v1/health`

*   **Method:** `GET`
*   **Description:** Checks if the application is running smoothly.
*   **Response:**
    ```json
    {
      "status": "success",
      "message": "Application is running smoothly",
      "data": {
        "status": "healthy"
      }
    }
    ```

```typescript
interface HealthCheckResponse {
  status: string;
  message: string;
  data: {
    status: string;
  };
}
```