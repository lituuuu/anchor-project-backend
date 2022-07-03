from test.mock import like_mock
from api import like
from bson.objectid import ObjectId
import pytest

def test_like_success(mocker):
    json = {'gallery_id': '62c0634858ffd07aecc4178c'}
    mocker.patch(
        'api.db.like.Like.has_like_by_user_and_galery',
        return_value=True
    )
    mocker.patch(
        'api.db.like.Like.insert',
        return_value=True
    )
    like.like_photo(json)

def test_unlike_success(mocker):
    json = {'gallery_id': '62c0634858ffd07aecc4178c'}
    mocker.patch(
        'api.db.like.Like.has_like_by_user_and_galery',
        return_value=False
    )
    mocker.patch(
        'api.db.like.Like.remove',
        return_value=True
    )
    like.like_photo(json)

def test_like_error(mocker):
    with pytest.raises(Exception):
        json = {'gallery_id': 'gallery_id_test'}
        mocker.patch(
            'api.db.like.Like.has_like_by_user_and_galery',
            return_value=True
        )
        mocker.patch(
            'api.db.like.Like.remove',
            return_value=like_mock.internal_server_error()
        )
        like.like_photo(json)

def test_unlike_error(mocker):
    with pytest.raises(Exception):
        json = {'gallery_id': 'gallery_id_test'}
        mocker.patch(
            'api.db.like.Like.has_like_by_user_and_galery',
            return_value=False
        )
        mocker.patch(
            'api.db.like.Like.remove',
            return_value=like_mock.internal_server_error()
        )
        like.like_photo(json)

