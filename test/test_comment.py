from test.mock import comment_mock
from api import comment
import pytest
from api.config import Config

def test_insert_comment_success(mocker):
    json = {'gallery_id': 'gallery_id_test', 'message': 'my_test'}
    mocker.patch(
        'api.db.comment.Comment.insert',
        return_value=comment_mock.comment_mock_insert(json)
    )
    test_class = comment.insert(json)
    assert test_class.message == "my_test"

def test_insert_comment_error(mocker):
    with pytest.raises(Exception):
        json = {'username': 'my_test', 'email': 'my_test', 'password': 'my_test'}
        mocker.patch(
            'api.db.user.User.insert',
            return_value=comment_mock.internal_server_error()
        )
        comment.insert(json)

def test_get_comment_by_gallery_success(mocker):
    mocker.patch(
        'api.db.comment.Comment.get_comment_by_gallery',
        return_value=comment_mock.list_of_comments()
    )
    test_class = comment.get_comment_by_gallery('gallery_id_test', Config.QUERY_LIMIT_DEFAULT, Config.QUERY_PAGE_DEFAULT)
    assert len(test_class) == 2

def test_get_comment_by_gallery_error(mocker):
    with pytest.raises(Exception):
        mocker.patch(
            'api.db.comment.Comment.get_comment_by_gallery',
            return_value=comment_mock.not_found_error()
        )
        comment.get_comment_by_gallery('gallery_id_test', Config.QUERY_LIMIT_DEFAULT, Config.QUERY_PAGE_DEFAULT)

