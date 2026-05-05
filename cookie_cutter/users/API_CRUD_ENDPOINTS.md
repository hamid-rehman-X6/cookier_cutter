# User CRUD API Documentation

This document describes the complete CRUD (Create, Read, Update, Delete) API endpoints for the User model in the cookie_cutter application.

## Base URL
```
/api/users/
```

## Endpoints

### 1. CREATE - Create a New User
**Endpoint:** `POST /api/users/`

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "name": "New User",
  "password": "securepassword123!"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "newuser@example.com",
  "name": "New User",
  "is_active": true,
  "is_staff": false,
  "date_joined": "2026-05-05T12:00:00Z",
  "url": "http://localhost:8000/api/users/1/"
}
```

**Status Codes:**
- `201 Created` - User successfully created
- `400 Bad Request` - Invalid data or missing required fields
- `400 Bad Request` - Email already exists

---

### 2. READ - List All Users
**Endpoint:** `GET /api/users/`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "email": "user1@example.com",
    "name": "User One",
    "is_active": true,
    "is_staff": false,
    "date_joined": "2026-05-05T12:00:00Z",
    "url": "http://localhost:8000/api/users/1/"
  },
  {
    "id": 2,
    "email": "user2@example.com",
    "name": "User Two",
    "is_active": true,
    "is_staff": false,
    "date_joined": "2026-05-05T12:00:00Z",
    "url": "http://localhost:8000/api/users/2/"
  }
]
```

**Status Codes:**
- `200 OK` - List retrieved successfully

---

### 3. READ - Retrieve a Specific User
**Endpoint:** `GET /api/users/{id}/`

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user1@example.com",
  "name": "User One",
  "is_active": true,
  "is_staff": false,
  "date_joined": "2026-05-05T12:00:00Z",
  "url": "http://localhost:8000/api/users/1/"
}
```

**Status Codes:**
- `200 OK` - User retrieved successfully
- `404 Not Found` - User does not exist

---

### 4. READ - Get Current User Profile
**Endpoint:** `GET /api/users/me/`

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "currentuser@example.com",
  "name": "Current User",
  "is_active": true,
  "is_staff": false,
  "date_joined": "2026-05-05T12:00:00Z",
  "url": "http://localhost:8000/api/users/1/"
}
```

**Status Codes:**
- `200 OK` - Current user profile retrieved
- `401 Unauthorized` - Not authenticated

---

### 5. UPDATE - Full Update (PUT)
**Endpoint:** `PUT /api/users/{id}/`

**Request Body:**
```json
{
  "email": "updated@example.com",
  "name": "Updated Name",
  "is_active": true
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "updated@example.com",
  "name": "Updated Name",
  "is_active": true,
  "is_staff": false,
  "date_joined": "2026-05-05T12:00:00Z",
  "url": "http://localhost:8000/api/users/1/"
}
```

**Status Codes:**
- `200 OK` - User updated successfully
- `400 Bad Request` - Invalid data
- `404 Not Found` - User does not exist

---

### 6. UPDATE - Partial Update (PATCH)
**Endpoint:** `PATCH /api/users/{id}/`

**Request Body (only update specific fields):**
```json
{
  "name": "New Name"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "New Name",
  "is_active": true,
  "is_staff": false,
  "date_joined": "2026-05-05T12:00:00Z",
  "url": "http://localhost:8000/api/users/1/"
}
```

**Update Password:**
```json
{
  "password": "newpassword123!"
}
```

**Status Codes:**
- `200 OK` - User partially updated successfully
- `400 Bad Request` - Invalid data
- `404 Not Found` - User does not exist

---

### 7. DELETE - Delete a User
**Endpoint:** `DELETE /api/users/{id}/`

**Response (204 No Content):**
```
(empty response body)
```

**Status Codes:**
- `204 No Content` - User successfully deleted
- `404 Not Found` - User does not exist

---

## Field Reference

### User Fields

| Field | Type | Required | Read-Only | Description |
|-------|------|----------|-----------|-------------|
| id | integer | No | Yes | Unique user identifier |
| email | email | Yes | No | User's email address (must be unique) |
| name | string | Yes | No | User's full name |
| password | string | Yes* | No | User's password (*only on create) |
| is_active | boolean | No | No | Whether user account is active |
| is_staff | boolean | No | No | Whether user has admin privileges |
| date_joined | datetime | No | Yes | When user account was created |
| url | URL | No | Yes | API endpoint URL for this user |

---

## Example Usage

### Using cURL

**Create a user:**
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "name": "John Doe",
    "password": "securepass123!"
  }'
```

**List all users:**
```bash
curl -X GET http://localhost:8000/api/users/
```

**Get a specific user:**
```bash
curl -X GET http://localhost:8000/api/users/1/
```

**Update a user:**
```bash
curl -X PATCH http://localhost:8000/api/users/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith"
  }'
```

**Delete a user:**
```bash
curl -X DELETE http://localhost:8000/api/users/1/
```

---

## Authentication

The API supports token-based authentication. Include the token in the Authorization header:

```
Authorization: Token {your-token-here}
```

---

## Testing

Run the CRUD tests using:

```bash
pytest cookie_cutter/users/tests/test_api_crud.py
```

Or run all user tests:

```bash
pytest cookie_cutter/users/tests/
```

---

## Implementation Details

The CRUD API is implemented using Django REST Framework with the following components:

- **ViewSet:** `UserViewSet` in `cookie_cutter/users/api/views.py`
  - Includes: Create, Retrieve, Update, Destroy, List mixins
  - Custom action: `me` endpoint for current user

- **Serializer:** `UserSerializer` in `cookie_cutter/users/api/serializers.py`
  - Handles validation
  - Custom `create()` method for secure password handling
  - Custom `update()` method for password updates

- **URLs:** Automatically generated via DRF router in `config/api_router.py`

---

## Error Handling

All endpoints return appropriate HTTP status codes and error messages:

```json
{
  "email": [
    "This field may not be blank."
  ],
  "name": [
    "This field may not be blank."
  ]
}
```

---

## Security Considerations

1. **Passwords:** Always sent over HTTPS in production
2. **Token Authentication:** Use token-based auth for API access
3. **Permissions:** Restrict user modifications to authorized users only
4. **CORS:** Configure CORS headers for cross-origin requests
5. **Rate Limiting:** Consider implementing rate limiting for production

