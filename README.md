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

- **Content Type:** application/json

```json
{
    "message": "User successfully registered"
}
```
Response Body(Error)

- **Content Type:** application/json

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

## 2. User Login / Token Endpoint

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

- **Content Type**: application/json


```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
Response Body (Error)

- **Content Type**: application/json


```json
{
    "detail": "Invalid login data"
}
```


## 3. Create Category

Creates a new category. Requires **admin** access/token. 

### Request

- **Method:** `POST`
- **Path:** `/categories`

#### Request Header
| Key       | Value  | Description                                  |
| --------- | ------ | -------------------------------------------- |
| x-token   | string | the token of the user, generated by the login|


#### Request Body

- **Content Type:** `application/json`

| Field     | Type   | Description                                  |
| --------- | ------ | -------------------------------------------- |
| name      | string | the name of the category we want to create   |
|description| string | optional; more info about the category       |
| status    | string | optional; either unlocked(default) or locked |
| privacy   | string | optional; either public(default) or private  |


#### Example Request Body

```json
{
    "name": "Medieval Times",
    "description": "All about the medieval time period in history"
}
```
### Responses

    201 Created: Category created successfully.
    401 Unauthorized: If the user has failed to login.
    403 Forbidden: If the user is not an admin. 

#### Response Body (Success)

- **Content Type:** `string`

```
Status: 201 Created

"Category 11 created successfuly!"
```
#### Response Body(Error)

- **Content Type:** `string`

```
Status: 401 Unauthorized

"Token header is missing! You must be logged in to gain access."
```
```
Status: 403 Forbidden

"You are not admin!"
```

## 4. Create Topic

Creates a new topic. Requires standard (user) authentication. 

### Request

- **Method:** `POST`
- **Path:** `/topics`

#### Request Body

- **Content Type:** `application/json`

| Field     | Type   | Description                                  |
| --------- | ------ | -------------------------------------------- |
| title     | string | the title of the topic we want to create     |
|category_id|   int  | the id of the category this topic will belong to|
|description| string | the topic content                            |
| status    | string | optional; either unlocked(default) or locked |


#### Example Request Body

```json
{
    "title": "How many hours did people sleep during the Medieval time period?",
    "category_id": 11,
    "description": "I saw this tv program on the History Channel once. It mentioned medieval people went to bed right after sundown. They would wake up sometime before sunrise. They would hire a 'knocker-upper' to wake them up. So in Europe, the nights could be as long as 16 hours in winter. The same tv show mentioned people would wake-up in the middle of the night & have a snack."

}
```
### Responses

    201 Created: Topic created successfully.
    401 Unauthorized: If the user has failed to login.
    403 Forbidden: If the category is locked or is private and the user does not have access. 
    404 Not Found: If the category id is not in the database.
    

#### Response Body (Success)

- **Content Type:** `text/plain`

```
Status: 201 Created

"Topic 44 created successfuly!"
```
#### Response Body(Error)

- **Content Type:** `text/plain`

```
Status: 401 Unauthorized

"Token header is missing! You must be logged in to create a topic."
```
```
Status: 403 Forbidden

"The category is locked and does not  accept any further topics!"
```
```
Status: 403 Forbidden

"You don't have writing access for the category of this topic!"
```
```
Status: 404 Forbidden

"This category does not exist!"
```

## 5. Create Reply

Creates a new reply. Requires standard (user) authentication. 

### Request

- **Method:** `POST`
- **Path:** `/topics/{topic_id}/replies`

#### Request Body

- **Content Type:** `text/plain`

Just put the string with the content of the reply in the Body. 


#### Example Request Body

```
    "More or less like us. What changed was how they slept.

    Sleeping was likely as seasonal as their food. In summer they would go to sleep late to better use the hours of sunlight."
```
### Responses

    201 Created: Reply created successfully.
    401 Unauthorized: If the user has failed to login.
    403 Forbidden: If the topic locked or if the category it belongs to is private and the user does not have access. 
    404 Not Found: If the topic id is not in the database.
    

#### Response Body (Success)

- **Content Type:** `text/plain`

```
Status: 201 Created

"Reply 101 created successfuly!"
```
#### Response Body(Error)

- **Content Type:** `text/plain`

```
Status: 401 Unauthorized

"Token header is missing! You must be logged in to post a topic."
```
```
Status: 403 Forbidden

"The topic is locked and does not  accept any further replies!"
```
```
Status: 403 Forbidden

"You don't have writing access for the category of this topic!"
```
```
Status: 404 Not Found

"This topic does not exist!"
```

## 6. View Category 

View a specific category and its topics. Requires standard (user) authentication. 

### Request

- **Method:** `GET`
- **Path:** `/categories/{category_id}`


### Responses

    200 OK: Displaying the category with its topics.
    401 Unauthorized: If the user has failed to login.
    403 Forbidden: If the category is private and the user does not have read or write access. 
    404 Not Found: If the category id is not in the database.
    

#### Response Body (Success) Example

- **Content Type:** `application/json`

```json
Status: 200 OK
{
    "category": {
        "id": 1,
        "name": "Art History",
        "description": "All about visual art",
        "status": "unlocked",
        "privacy": "public"
    },
    "topics": [
        {
            "id": 1,
            "title": "Was Van Gogh a better artist than Da Vinci?",
            "category_id": 1,
            "user_id": 1,
            "date": "2024-05-09T16:23:35",
            "description": "",
            "status": "unlocked",
            "best_reply": 3
        },
        {
            "id": 2,
            "title": "I just got rejected from the Academy of Fine Arts Vienna. What do I do now?",
            "category_id": 1,
            "user_id": 6,
            "date": "2024-05-10T09:24:47",
            "description": "I recently applied to the Academy of Fine Arts Vienna, but I just received a rejection letter. I'm feeling pretty down and unsure about my next steps. Has anyone else experienced this, and what did you do to stay motivated? I'd appreciate any advice on other art schools or alternative paths in the art world.",
            "status": "unlocked",
            "best_reply": 4
        }
    ]
}
```
#### Response Body(Error) 

- **Content Type:** `text/plain`

```
Status: 401 Unauthorized

"Token header is missing! You must be logged in to view category."
```
```
Status: 403 Forbidden

"You don't have access to this category!"
```
```
Status: 404 Not Found

"This category does not exist!"
```

## 7. View Topic 

View a specific topic and its replies. Requires standard (user) authentication. 

### Request

- **Method:** `GET`
- **Path:** `/topics/{topic_id}`


### Responses

    200 OK: Displaying the topic and its replies.
    401 Unauthorized: If the user has failed to login.
    403 Forbidden: If the category the topic belongs to is private and the user does not have read or write access. 
    404 Not Found: If the topic id is not in the database.
    

#### Response Body (Success) Example

- **Content Type:** `application/json`

```json
Status: 200 OK
{
"topic": {
        "id": 4,
        "title": "What are the best ways to think of ideas for a startup?",
        "category_id": 2,
        "user_id": 6,
        "date": "2024-05-10T10:22:46",
        "description": "",
        "status": "locked",
        "best_reply": 9
    },
    "replies": [
        {
            "id": 9,
            "user_id": 7,
            "date": "2024-05-10T10:23:32",
            "topic_id": 4,
            "content": "A startup idea is derived out of discomfort or a gap you see in the existing market. So don’t go looking here and there for that billion idea, just be more attentive and observant while looking around you, it is right there.",
            "upvotes": 2,
            "downvotes": 0
        },
        {
            "id": 10,
            "user_id": 8,
            "date": "2024-05-10T10:24:23",
            "topic_id": 4,
            "content": "Make sure your solution is unique, and you don't have a ton of competition. Use Google to search for competitors",
            "upvotes": 2,
            "downvotes": 2
        },
        {
            "id": 11,
            "user_id": 7,
            "date": "2024-05-10T10:24:59",
            "topic_id": 4,
            "content": "Validate demand (prove people will buy it). You can pre-sell with crowdfunding to prove this, or you can make a landing page that looks like your product is ready to go. Have your price on the landing page. When a user tries to buy capture their email, and inform them that they caught you right before launch",
            "upvotes": 0,
            "downvotes": 0
        }
    ]
}
```

#### Response Body(Error)

- **Content Type:** `text/plain`

```
Status: 401 Unauthorized

"Token header is missing! You must be logged in to view topic."
```
```
Status: 403 Forbidden

"You don't have access to the category this topic belongs to!"
```
```
Status: 404 Not Found

"There is no such topic!"
```

## 8. View Topics 

View all topics. Open access: no token necessary.  

### Request

- **Method:** `GET`
- **Path:** `/topics`

#### Request Params

| Key     | Value    | Description                                  |
| --------- | ------- | -------------------------------------------- |
| page      | integer | The page number to display results. |
| limit     | integer | The number of topics to display on the page. |


### Responses

    200 OK: Displaying the list of topics.

#### Response Body (Success) Example

- **Content Type**: application/json

```json
Status: 200 OK
[
    {
        "id": 1,
        "title": "Was Van Gogh a better artist than Da Vinci?",
        "category_id": 1,
        "user_id": 1,
        "date": "2024-05-09T16:23:35",
        "description": "",
        "status": "unlocked",
        "best_reply": 3
    }
]
```

## 9. View Categories 

View all categories. Open access: no token necessary.  

### Request

- **Method:** `GET`
- **Path:** `/categories`

#### Request Params

| Key     | Value    | Description                                  |
| --------- | ------- | -------------------------------------------- |
| page      | integer | The page number to display results. |
| limit     | integer | The number of categories to display on the page. |


### Responses

    200 OK: Displaying the list of topics.

#### Response Body (Success) Example

- **Content Type**:: application/json

```json
Status: 200 OK
[
    {
        "id": 1,
        "name": "Art History",
        "description": "All about visual art",
        "status": "unlocked",
        "privacy": "public"
    }
]
```

## 10. Give User Access to Category (Read and Write) 

Grants or revokes access to a category for a specific user. Requires **admin**  access/token.

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

```s

"read"

```


Responses
- **200 OK:** Access successfully granted or revoked.
- **400 Bad Request:**  If the request body or parameters are invalid.
- **401 Unauthorized:** If the user is not authenticated.
- **403 Forbidden:** If the authenticated user is not an admin.
- **404 Not Found:** If the category specified does not exist.


Response Body (Success)
- **Content Type**: text/plain

| Status Code | Message                                              |
|-------------|------------------------------------------------------|
| 200         | User {user_id} has been granted {write/read} access! |

Response Body (Error)
- **Content Type**: `text/plain`

| Status Code | Message                                                    |
|-------------| ---------------------------------------------------------- |
| 400         | Invalid access_type: please choose between read and write!.                          |
| 401         | Token header is missing! You must be logged in to gain access |
| 403         | You are not admin!                                        |
| 404         | This category does not exist!                             |
| 400         | The category is public! No need to give explicit access.                            |



## 11. Revoke User Access for Category

Revokes access to a category for a specific user. Requires **admin** access/token.

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


## 12. Lock Category

Changes the accessibility status of a category. Requires **admin** access/token.

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


## 13. Lock Topic

Changes the status of a topic. Requires **admin** access/token.

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



## 14. Create a Message 

A logged in user creates a message to another existing user in the database.

### Request

- **Method:** `POST`
- **Path:** `/messages`

#### Request Header
| Key       | Value  | Description                                  |
| --------- | ------ | -------------------------------------------- |
| x-token   | string | the token of the user, generated by the login|

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
No such recipient exists!
```



## 15. View Conversations 

Find a list of conversations a logged in user has with other users. 

### Request

- **Method:** `GET`
- **Path:** `/conversations`

#### Request Header

#### Request Header
| Key       | Value  | Description                                  |
| --------- | ------ | -------------------------------------------- |
| x-token   | string | the token of the user, generated by the login|

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



## 16. View Conversation

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



## 17. Upvote/Downvote a Reply

A logged in user can upvote or downvote on an existing reply in the system.

### Request

- **Method:** `PUT`
- **Path:** `/replies/{id}/vote`

#### Request Header
| Key       | Value  | Description                                  |
| --------- | ------ | -------------------------------------------- |
| x-token   | string | the token of the user, generated by the login|

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



## 18. Choose Best Reply 

An author to a topic can select a reply as the best reply.

### Request

- **Method:** `PUT`
- **Path:** `/topics/{id}/bestreply`

#### Request Header
| Key       | Value  | Description                                  |
| --------- | ------ | -------------------------------------------- |
| x-token   | string | the token of the user, generated by the login|

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



## 19. Make Category Private/Non-Private(Public) 

Changing the privacy to categories between *public* and *private*. Requires **admin** access/token.

### Request

- **Method:** `PUT`
- **Path:** `/categories/{id}/privacy`

#### Request Header
| Key       | Value  | Description                                  |
| --------- | ------ | -------------------------------------------- |
| x-token   | string | the token of the user, generated by the login|


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



## 20. View Priviliged Users

List of users who have *read* or *write* access for private categories.

### Request

- **Method:** `GET`
- **Path:** `/categories/{id}/priviliged`

Responses

- **200 OK** List of privileged users is provided.
- **401 Unauthorised** - Invalid token or user is not our database.
- **422 Unprocessable Entity** X-token is not provided

Response Body (Success)

- **Content Type:** `application/json`

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
