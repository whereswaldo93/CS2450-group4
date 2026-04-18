# To-Do List Application API Contract

## 1. Overview

This API provides CRUD operations for managing to-do tasks. It is built using Django REST Framework

* **Base URL:** `/api/`
* **Format:** JSON
* **App:** `Task_Manager_App`
* **Version:** v1

---

## 2. Resource: Task

Represents a single to-do item.

### Example

```json
{
  "task_id": 1,
  "title": "Buy groceries",
  "description": "Eggs, milk, cheese",
  "priority": "High",
  "due_date": "2026-03-25",
  "status": "Pending",
  "notes": "Remember to check for discounts."
}
```
---

### Field Definitions

| Field       | Type     | Required | Description              |
| ----------- | -------- | -------- | ------------------------ |
| id          | integer  | yes      | Auto-generated unique ID |
| title       | string   | yes      | Max 255 characters       |
| description | string   | no       | Optional task details    |
| priority    | string   | no       | Low, Medium or High      |
| due_date    | date     | no       | Due date for the task    |
| status      | string   | yes      | Pending or Completed     |
| notes       | string   | no       | Optional task notes      |

---

### 3. Endpoints

#### 🔹 List All Tasks

**GET** `/api/tasks/`
- Returns tasks belonging only to the authenticated user.

#### 🔹 Create Task

**POST** `/api/tasks/`
- **Validation**: Returns 400 if `title` is missing or `due_date` is in the past.
- **Logging**: Triggers an `INFO` log on successful DB creation.

#### 🔹 Retrieve / Update / Delete

- **GET** `/api/tasks/{task_id}/`
- **PUT/PATCH** `/api/tasks/{task_id}/`
- **DELETE** `/api/tasks/{task_id}/`
- **Auth**: Returns 404 if the task exists but belongs to a different user

---

### 4. Status Codes & Error Handling

| Code | Meaning     | Usage |
| ---- | ----------- | ----- |
| 200  | OK          | Successful retrieval or update |
| 201  | Created     | Successful task creation |
| 204  | No Content  | Successful deletion |
| 400  | Bad Request | Validation error |
| 401  | Unauthorized| User is not logged in |
| 404  | Not Found   | Task ID does not exist or is owned by another user |
| 500  | Server Error| Logged as Error with stack trace |
---

### 5. Implementation Standards

**Security & Ownership**
- **Authentication**: All endpoints require valid session or token
- **Isolation**: Users can only view, edit, or delete tasks where `task.user == request.user`

**Logging Policy**
All API interactions are logged under the taskproject namespace:
- **Audit Trail**: Every `POST`, `PATCH`, and `DELETE` records the `user_id` and `task_id` for traceability.
- **Visibility**: Environmnent-aware formatting, simple for development and JSON for production

---

### 6. Current Enhancements

* User authentication integration
* Task ownership enforcement
* Structured logging for all CRUD operations
* Validation for dates and required fields

---

### 7. Example Flow

- **POST**: `/api/tasks/` → User creates "Math homework"
- **GET**: `/api/tasks/` → User sees their list of active tasks
- **PATCH**: `/api/tasks/` → User marks "Math homework" as `Completed`
- **DELETE**: `/api/tasks/` → User removes the task
