## Register User endpoint

Registers a new user with the system.

### Request

- **Method:** `POST`
- **Path:** `/users/register`

#### Request Body

- **Content Type:** `application/json`

| Field     | Type   | Description                                  |
| --------- | ------ | -------------------------------------------- |
| username  | string | The username of the user (unique identifier).|
| email     | string | The email address of the user (unique identifier). |
| password  | string | The password for the user's account.         |
| firstname | string | The first name of the user.                  |
| lastname  | string | The last name of the user.                   |

#### Example Request Body

```json
{
    "username": "john_doe",
    "password": "P@ssw0rd",
    "firstname": "John",
    "lastname": "Doe",
    "email": "john@example.com"
}
```
Responses

- **200 OK:** User successfully registered.
- **400 Bad Request:** If the username is already taken or the email is already associated with an existing user.

Response Body (Success)

Content Type: application/json

```json

{
    "message": "User successfully registered"
}
```
Response Body(Error)

Content Type: application/json

```json
{
    "detail": "Username is taken"
}
```
```json

{
    "detail": "User with this email already exists"
}
```


## User Login

Logs in a user to the system and generates an authentication token.

### Request

- **Method:** `POST`
- **Path:** `/users/login`

#### Request Body

- **Content Type:** `application/json`

| Field     | Type   | Description                                  |
| --------- | ------ | -------------------------------------------- |
| username  | string | The username of the user.                    |
| password  | string | The password for the user's account.         |

#### Example Request Body

```json
{
    "username": "john_doe",
    "password": "P@ssw0rd"
}
```
Responses

    200 OK: User successfully logged in and authentication token generated.
    400 Bad Request: If the login data provided is invalid.

Response Body (Success)

Content Type: application/json


```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
Response Body (Error)

Content Type: application/json


```json
{
    "detail": "Invalid login data"
}
```

## Give User Access to Category

Grants or revokes access to a category for a specific user.

### Request

- **Method:** `PUT`
- **Path:** `/categories/{category_id}/users/{user_id}`

#### Path Parameters

| Parameter   | Type   | Description                                 |
| ----------- | ------ | ------------------------------------------- |
| category_id | int    | The ID of the category.                     |
| user_id     | int    | The ID of the user to grant access.|

#### Request Body

- **Content Type:** `text/plain`

| Type   | Description                                  |
| ------ | -------------------------------------------- |
| string | The type of access to grant("read", "write").|

#### Example Request Body

```json

"read"

```


Responses
- **200 OK:** Access successfully granted or revoked.
- **400 Bad Request:**  If the request body or parameters are invalid.
- **401 Unauthorized:** If the user is not authenticated.
- **403 Forbidden:** If the authenticated user is not an admin.
- **404 Not Found:** If the category specified does not exist.


Response Body (Success)
Content Type: text/plain

| Status Code | Message                                              |
|-------------|------------------------------------------------------|
| 200         | User {user_id} has been granted {write/read} access! |

Response Body (Error)
- **Content Type:** `text/plain`

| Status Code | Message                                                    |
|-------------| ---------------------------------------------------------- |
| 400         | Invalid access_type: please choose between read and write!.                          |
| 401         | Token header is missing! You must be logged in to gain access |
| 403         | You are not admin!                                        |
| 404         | This category does not exist!                             |
| 400         | The category is public! No need to give explicit access.                            |



## Revoke User Access from Category

Revokes access to a category for a specific user.

### Request

- **Method:** `DELETE`
- **Path:** `/categories/{category_id}/users/{user_id}`

#### Path Parameters

| Parameter   | Type   | Description                                  |
| ----------- | ------ | -------------------------------------------- |
| category_id | int    | The ID of the category.                      |
| user_id     | int    | The ID of the user to revoke access.         |

### Responses

- **200 OK:** Access successfully revoked.
- **401 Unauthorized:** If the user is not authenticated.
- **403 Forbidden:** If the authenticated user is not an admin.
- **404 Not Found:** If the category specified does not exist.

#### Response Body (Error)

- **Content Type:** `text/plain`

| Status Code | Message                                                    |
| ----------- | ---------------------------------------------------------- |
| 401         | Token header is missing! You must be logged in to gain access |
| 403         | You are not admin!                                        |
| 404         | This category does not exist!                             |


## Change Accessibility Status of Category

Changes the accessibility status of a category.

### Request

- **Method:** `PUT`
- **Path:** `/categories/{id}/status`

#### Path Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| id        | int  | The ID of the category. |

### Responses

- **200 OK:** Accessibility status successfully changed.
- **401 Unauthorized:** If the user is not authenticated.
- **403 Forbidden:** If the authenticated user is not an admin.
- **404 Not Found:** If the category specified does not exist.

#### Response Body (Error)

- **Content Type:** `text/plain`

| Status Code | Message                                                    |
| ----------- | ---------------------------------------------------------- |
| 401         | Token header is missing! You must be logged in to gain access |
| 403         | You are not admin!                                        |
| 404         | This category does not exist!                             |


## Change Accessibility Status of Topic

Changes the status of a topic.

### Request

- **Method:** `PUT`
- **Path:** `/topics/{id}/status`

#### Path Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| id        | int  | The ID of the topic. |

### Responses

- **200 OK:** Status successfully changed.
- **401 Unauthorized:** If the user is not authenticated.
- **403 Forbidden:** If the authenticated user is not an admin.
- **404 Not Found:** If the topic specified does not exist.

#### Response Body (Error)

- **Content Type:** `text/plain`

| Status Code | Message                                                    |
| ----------- | ---------------------------------------------------------- |
| 401         | Token header is missing! You must be logged in to gain access |
| 403         | You are not admin!                                        |
| 404         | This topic does not exist!                                |