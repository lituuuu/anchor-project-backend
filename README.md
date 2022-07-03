# anchor-project-backend

This project is a code challenge.

How to start the API:
``make run``

How start the tests:
``make test``

Actually, this project connect in mongodb cloud (connection string in config.py), then don't use any docker-compose file.

# -> API Methods
## ---> Utils
    [GET] /ping
    Description: It's a health check for application
    Returns: [200]
    Example: { "pong!" }
    
## ---> User
    [POST] /register
    Description: Register a new user in application, the new user isn't admin.
    Returns: [200, 500]
    Example: 
    {
        "_id": {
            "$oid": "62c10c886397abeed3dd67fb"
        },
        "admin": false,
        "created_at": {
            "$date": "2022-07-03T00:27:04.645Z"
        },
        "email": "my_test",
        "username": "my_test"
    }

    [POST] /login
    Description: Check if user exists in database and returns JWT token.
    Returns: [200, 404]
    Example: 
    {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJhZG1pbiJ9.ZkqrFqhjDnjNxefAMEuJEOENZc4BYrnX46mI7RaTZw0"
    }

## ---> Gallery

## ---> Like

## ---> Comments