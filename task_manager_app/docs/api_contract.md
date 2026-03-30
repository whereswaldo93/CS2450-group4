# To-Do List Application API Contract

## 1. Overview

This API provides CRUD operations for managing to-do tasks.

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

## 3. Endpoints

### 🔹 List All Tasks

**GET** `/api/tasks/`

#### Response

```json
[
  {
    "task_id": 1,
    "title": "Buy groceries",
    "description": "Eggs, milk, cheese",
    "priority": "High",
    "due_date": "2026-03-25",
    "status": "Pending",
  }
]
```

---

### 🔹 Create Task

**POST** `/api/tasks/`

#### Request

```json
{
  "title": "Finish homework",
  "description": "Math exercises",
  "priority": "High",
  "due_date": "2026-12-31"
}
```

#### Response (201 Created)

```json
{
  "task_id": 2,
  "title": "Finish homework",
  "description": "Math exercises",
  "priority": "High",
  "due_date": "2026-12-31",
  "status": "Pending",
}
```

---

### 🔹 Retrieve Single Task

**GET** `/api/tasks/{task_id}/`

#### Response

```json
{
  "task_id": 1,
  "title": "Buy groceries",
  "description": "Eggs, milk, cheese",
  "priority": "High",
  "due_date": "2026-03-25",
  "status": "Pending",
}
```

---

### 🔹 Update Task (Full)

**PUT** `/api/tasks/{task_id}/`

#### Request

```json
{
  "title": "Buy groceries and fruit",
  "description": "Eggs, milk, apples",
  "priority": "High",
  "due_date": "2026-03-30",
  "status": "Completed",
}
```

#### Response

```json
{
  "task_id": 1,
  "title": "Buy groceries and fruit",
  "description": "Eggs, milk, apples",
  "priority": "High",
  "due_date": "2026-03-30",
  "status": "Completed",
}
```

---

### 🔹 Partial Update

**PATCH** `/api/tasks/{task_id}/`

#### Request

```json
{
  "status": "Completed"
}
```

#### Response

```json
{
  "task_id": 1,
  "status": "Completed",
}
```

---

### 🔹 Delete Task

**DELETE** `/api/tasks/{task_id}/`

#### Response (204 No Content)

```json
{
  "message": "Task deleted successfully"
}
```

---

## 4. Status Codes

| Code | Meaning     |
| ---- | ----------- |
| 200  | OK          |
| 201  | Created     |
| 204  | No Content  |
| 400  | Bad Request |
| 404  | Not Found   |

---

## 5. Validation Rules

* `title` is required
* `title` must not exceed 255 characters
* `description` is optional
* `priority` must be one of the defined levels (e.g., Low, Medium, High).
* `due_date` is optional but must be a valid date.

---

## 6. URL Structure

```
/api/tasks/
/api/tasks/{task_id}/
```

---

## 7. Future Enhancements

* User authentication
* Task ownership per user
* Filtering
* Editing tasks
* Due dates and priorities

---

## 8. Implementation Notes

This contract will be implemented in:

* `todos/views.py` → API logic
* `todos/urls.py` → route definitions
* `core/urls.py` → API entry point
* Task model definition in models/task.py

---

## 9. Example Flow

```
Client → GET /api/tasks/ → Retrieve all tasks
Client → POST /api/tasks/ → Create a task
Client → PATCH /api/tasks/1/ → Mark task complete
```
