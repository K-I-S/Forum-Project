## 1. Register User 

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


## 2. User Login

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

## 3. Give User Access to Category (Read and Write) 

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



## 4. Revoke User Access for Category

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


## 5. Lock Category

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


## 6. Lock Topic

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



## 7. Create a Message 

A logged in user creates a message to another existing user in the database.

### Request

- **Method:** `POST`
- **Path:** `/messages`

#### Request Header

- **x-token** - The token provided during login.

#### Request Body

- **Content Type:** `application/json`

| Field        | Type   | Description                                  |
| ------------ | ------ | -------------------------------------------- |
| text         | string | Content of the message|
| receiver_id  | string | Recipient of the message|

#### Example Request Body

```json
{
    "text": "Hi.",
    "receiver_id": 5
}
```
Responses

- **201 Created:** Message has been sucessfully created.
- **401 Unauthorised** - Invalid token or user is not our database.
- **404 Not Found** Username is not found.
- **422 Unprocessable Entity:** X-token is not provided.

Response Body (Success)

- **Content Type:** `text/plain`

```s

Message to User 5 successfully sent (ID 29)!

```
Response Body(Error)

- **Content Type:** `json/application`
```json
{
    "detail": "Invalid token"
}
```

- **Content Type:** `text/plain`
```s
Token header is missing! You need to log in first!
```

- **Content Type:** `text/plain`
```s

    "No such recipient exists!"

```



## 8. View Conversations 

Find a list of conversations a logged in user has with other users.

### Request

- **Method:** `GET`
- **Path:** `/conversations`

#### Request Header

- **x-token:** - The token provided during login.

Responses

- **200 OK** - List of conversations is provided.
- **401 Unauthorised** - Invalid token or user is not our database.
- **422 Unprocessable Entity** X-token is not provided

Response Body (Success)

- **Content Type:**: `application/json`

```json
[
    "User 4(you) has conversations with the following users:",
    [
        {
            "receiver_id": 5,
            "username": "geomilev"
        },
    ]
]
```
Response Body(Error)
- **Content Type:** `text/plain`
```s
Token header is missing! You need to log in first!
```
- **Content Type:**: `application/json`
```json
{
    "detail": "Invalid token"
}
```



## 9. View Conversation

View the conversation between a logged in user and another registered user in the database.

### Request

- **Method:** `GET`
- **Path:** `/conversation/{id}`

Responses

- **200 OK** The sought conversation is provided.
- **401 Unauthorised** - Invalid token or user is not our database.
- **422 Unprocessable Entity** X-token is not provided

Response Body (Success)

- **Content Type:**: `application/json`

```json

[
    {
        "id": 9,
        "sender_id": 5,
        "text": "Anyway. Nashledanou.",
        "date": "2024-05-10T12:23:01",
        "receiver_id": 4
    },
    {
        "id": 8,
        "sender_id": 4,
        "text": "Bad day?",
        "date": "2024-05-10T12:21:31",
        "receiver_id": 5
    },
]
```
Response Body(Error)

- **Content Type:** `text/plain`
```s
Token header is missing! You need to log in first!
```
- **Content Type:**: `application/json`
```json
{
    "detail": "Invalid token"
}
```



## 10. Upvote/Downvote a Reply

A logged in user can upvote or downvote on an existing reply in the system.

### Request

- **Method:** `PUT`
- **Path:** `/replies/{id}/vote`

#### Request Header

- **x-token** - The token provided during login.

#### Request Body

- **Content Type:** `text/plain`

"up" for *upvote* or any other string for *downvote*

#### Example Request Body

```s
"up"
```
#### Responses

- **200 OK** - Vote is casted.
- **401 Unauthorised** - Invalid token.
- **404 Not Found** - Username is not found.
- **422 Unprocessable Entity:** - X-token is not provided.


#### Response Body (Success)

No written response.

#### Response Body(Error)
- **Content Type:** `json/application`
```json
{
    "detail": "Invalid token"
}
```
- **Content Type:** `text/plain`
```s
Token header is missing! You need to log in first!
```
- **Content Type:** `json/application`
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": [
                "body"
            ],
            "msg": "Field required",
            "input": null
        }
    ]
}
```

- **Content Type:** `json/application`
```json
{
    "detail": [
        {
            "type": "string_type",
            "loc": [
                "body"
            ],
            "msg": "Input should be a valid string",
            "input": 1
        }
    ]
}
```



## 11. Choose Best Reply 

An author to a topic can select a reply as the best reply.

### Request

- **Method:** `PUT`
- **Path:** `/topics/{id}/bestreply`

#### Request Header

- **x-token** - The token provided during login of the author of the topic.

#### Request Body

- **Content Type:** `text/plain`

ID number of the reply.

#### Example Request Body

```s
5
```
#### Responses

- **200 OK** - Best Reply is selected.
- **401 Unauthorised** - Invalid token or user is not our database.
- **404 Not Found** - Username is not found.
- **422 Unprocessable Entity:** - X-token is not provided.


#### Response Body (Success)

- **Content Type:** `text/plain`
```s
You have successfully chosen the reply ID5 as the best!
```

#### Response Body(Error)
- **Content Type:** `json/application`
```json
{
    "detail": "Invalid token"
}
```
- **Content Type:** `json/application`
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": [
                "body"
            ],
            "msg": "Field required",
            "input": null
        }
    ]
}
```
- **Content Type:** `text/plain`
```s
Token header is missing! You must be logged in to gain access
```



## 12. Make Category Private/Non-Private(Public) 

Changing the privacy to categories between *public* and *private*.

### Request

- **Method:** `PUT`
- **Path:** `/categories/{id}/privacy`

#### Request Header

- **x-token** - The token provided during login.


#### Responses

- **200 OK** - Category Privacy is amended.
- **401 Unauthorised** - Invalid token or user is not our database.
- **404 Not Found** - Username is not found.
- **422 Unprocessable Entity:** - X-token is not provided.

#### Response Body (Success)

- **Content Type:** `text/plain`
```s
Privacy status changed to public for category Art History!
```
- **Content Type:** `text/plain`
```s
Privacy status changed to private for category Art History!
```

#### Response Body(Error)
- **Content Type:** `json/application`
```json
{
    "detail": "Invalid token"
}
```
- **Content Type:** `text/plain`
```s
Token header is missing! You must be logged in to gain access
```
- **Content Type:** `text/plain`
```s
This category does not exist!
```



## 13. View Priviliged Users

List of users who have *read* or *write* access for private categories.

### Request

- **Method:** `GET`
- **Path:** `/categories/{id}/priviliged`

Responses

- **200 OK** List of privileged users is provided.
- **401 Unauthorised** - Invalid token or user is not our database.
- **422 Unprocessable Entity** X-token is not provided

Response Body (Success)

- **Content Type:**: `application/json`

```json
{
    "category": {
        "id": 2,
        "name": "Startups",
        "description": "Why we make one and how to succeed..",
        "status": "unlocked",
        "privacy": "private"
    },
    "users": [
        {
            "id": 4,
            "access_type": "read"
        },
        {
            "id": 6,
            "access_type": "write"
        }
    ]
}
```
Response Body(Error)
- **Content Type:** `text/plain`
```s
Token header is missing! You must be logged in to gain access
```
- **Content Type:** `text/plain`
```s
You are not admin!
```

- **Content Type:**: `application/json`
```json
{
    "detail": "Invalid token"
}
```
