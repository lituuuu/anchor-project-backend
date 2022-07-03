# anchor-project-backend

This project is a code challenge.
Before start, needs execute:
``pip install -r requirements.txt``

Python version 3.10.

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
    Returns: [201, 500]
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
        "token": "HASH_JWT_TOKEN"
    }

## ---> Gallery
    [GET] /gallery?limit={x}&skip={y}
    Description: Get images based in limit with an offset based in skip. In this path. In this path if the user is admin
    the application get all photos, else get only the user photos.
    Returns: [200, 404, 500]
    Example: 
    [{
        "_id": {
            "$oid": "62c0634858ffd07aecc4178c"
        },
        "created_at": {
            "$date": "2022-07-02T12:24:56.909Z"
        },
        "pendent": false,
        "photo_bucket": "https://s3.amazonaws.com/anchorproject/62c0634858ffd07aecc4178b-62bf6b94fe2a2aef06195113-1516850398825%20(1).jpg",
        "user_id": {
            "$oid": "62c05c17a10c56097d006979"
        }
    }]

    [GET] /gallery/pendent
    Description: Needs a admin permission. Get images based in limit with an offset based in skip. In this path, get ONLY pendent
    images.
    Returns: [200, 404]
    Example: 
    [{
        "_id": {
            "$oid": "62c0634858ffd07aecc4178c"
        },
        "created_at": {
            "$date": "2022-07-02T12:24:56.909Z"
        },
        "pendent": true,
        "photo_bucket": "https://s3.amazonaws.com/anchorproject/62c0634858ffd07aecc4178b-62bf6b94fe2a2aef06195113-1516850398825%20(1).jpg",
        "user_id": {
            "$oid": "62c05c17a10c56097d006979"
        }
    }]

    [GET] /gallery/confirmed
    Description: Get images based in limit with an offset based in skip. In this path, NEVER get pendent images. All images before
    needs to be approved by admin.
    Returns: [200, 404]
    Example: 
    [{
        "_id": {
            "$oid": "62c0634858ffd07aecc4178c"
        },
        "created_at": {
            "$date": "2022-07-02T12:24:56.909Z"
        },
        "pendent": false,
        "photo_bucket": "https://s3.amazonaws.com/anchorproject/62c0634858ffd07aecc4178b-62bf6b94fe2a2aef06195113-1516850398825%20(1).jpg",
        "user_id": {
            "$oid": "62c05c17a10c56097d006979"
        }
    }]

    [POST] /gallery
    Description: Insert a new image in S3 Bucket and database. If the user isn't a admin, the image saves in pendent status, else needs to be approved.
    P.S: File needs to be a image (.jpeg or .jpg).
    Returns: [200, 500]
    Example: 
    {
        "_id": {
            "$oid": "62c1104cc246da9ef2dd1593"
        },
        "created_at": {
            "$date": "2022-07-03T00:43:08.914Z"
        },
        "pendent": false,
        "photo_bucket": "xxxxxxxxx",
        "user_id": {
            "$oid": "62c05c17a10c56097d006979"
        }
    }

    [POST] /gallery/confirm
    Description: Approve a pendent image created by a not admin user.
    Returns: [200, 404, 500]
    Example: 
    {
        "_id": {
            "$oid": "62c1104cc246da9ef2dd1593"
        },
        "created_at": {
            "$date": "2022-07-03T00:50:32.809Z"
        },
        "pendent": false
    }

    [GET] /gallery/<id>
    Description: Get all information about the gallery:
        - Comments by limit and page
        - Like count and user has liked
        - Image information
    Returns: [200, 404, 500]
    Example: 
    {
        "comments": [
            {
                "_id": {
                    "$oid": "62c0f7360a13b350aaeb7978"
                },
                "created_at": {
                    "$date": "2022-07-02T22:56:06.754Z"
                },
                "gallery_id": {
                    "$oid": "62c0634858ffd07aecc4178c"
                },
                "message": "test_comment_2",
                "user_id": {
                    "$oid": "62c05c17a10c56097d006979"
                }
            },
            {
                "_id": {
                    "$oid": "62c0f7330a13b350aaeb7977"
                },
                "created_at": {
                    "$date": "2022-07-02T22:56:03.269Z"
                },
                "gallery_id": {
                    "$oid": "62c0634858ffd07aecc4178c"
                },
                "message": "test_comment_1",
                "user_id": {
                    "$oid": "62c05c17a10c56097d006979"
                }
            }
        ],
        "gallery": {
            "_id": {
                "$oid": "62c0634858ffd07aecc4178c"
            },
            "created_at": {
                "$date": "2022-07-02T12:24:56.909Z"
            },
            "pendent": false,
            "photo_bucket": "bucket_s3",
            "user_id": {
                "$oid": "62c05c17a10c56097d006979"
            }
        },
        "likes": {
            "count": 1,
            "hasLike": false
        }
    }


## ---> Like
    [GET] /like/<id>
    Description: Get count of likes and user situation into like document.
    Returns: [200, 404]
    Example: 
    {
        "count": 1,
        "hasLike": false
    }

    [POST] /like
    Description: Set like or unlike about the gallery. If unlike, the response don't have a id field.
    Returns: [200, 500]
    Example: 
    {
        "created_at": {
            "$date": "2022-07-03T00:55:28.141Z"
        },
        "gallery_id": {
            "$oid": "62c0634858ffd07aecc4178c"
        },
        "user_id": {
            "$oid": "62c05c17a10c56097d006979"
        }
    }

## ---> Comments
    [GET] /comment/<id>
    Description: Returns a array of comments from gallery id
    Returns: [200, 404]
    Example: 
    [
        {
            "_id": {
                "$oid": "62c0f7360a13b350aaeb7978"
            },
            "created_at": {
                "$date": "2022-07-02T22:56:06.754Z"
            },
            "gallery_id": {
                "$oid": "62c0634858ffd07aecc4178c"
            },
            "message": "test_comment_2",
            "user_id": {
                "$oid": "62c05c17a10c56097d006979"
            }
        }
    ]

    [POST] /comment
    Description: Insert a new comment into database. 
    Returns: [200, 500]
    Example: 
    {
        "_id": {
            "$oid": "62c0f7360a13b350aaeb7978"
        },
        "created_at": {
            "$date": "2022-07-02T22:56:06.754Z"
        },
        "gallery_id": {
            "$oid": "62c0634858ffd07aecc4178c"
        },
        "message": "test_comment_2",
        "user_id": {
            "$oid": "62c05c17a10c56097d006979"
        }
    }