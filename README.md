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

    200 OK: User successfully registered.
    400 Bad Request: If the username is already taken or the email is already associated with an existing user.

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