from test.mock import gallery_mock
from api import gallery
import pytest
from api.config import Config

def test_pendent_gallery_success(mocker):
    mocker.patch(
        'api.db.gallery.Gallery.get_photos',
        return_value=gallery_mock.pendent_gallery()
    )
    test_class = gallery.photos_pendent(Config.QUERY_LIMIT_DEFAULT, Config.QUERY_PAGE_DEFAULT)
    assert test_class == gallery_mock.pendent_gallery()
    assert test_class[0]["pendent"] == "true"

def test_pendent_gallery_error(mocker):
    with pytest.raises(Exception):
        mocker.patch(
            'api.db.gallery.Gallery.get_photos',
            return_value=gallery_mock.internal_server_error()
        )
        gallery.photos_pendent(Config.QUERY_LIMIT_DEFAULT, Config.QUERY_PAGE_DEFAULT)

def test_confirmed_gallery_success(mocker):
    mocker.patch(
        'api.db.gallery.Gallery.get_photos',
        return_value=gallery_mock.confirmed_gallery()
    )
    test_class = gallery.photos_confirmed(Config.QUERY_LIMIT_DEFAULT, Config.QUERY_PAGE_DEFAULT)
    assert test_class == gallery_mock.confirmed_gallery()
    assert test_class[0]["pendent"] == "false"

def test_confirmed_gallery_error(mocker):
    with pytest.raises(Exception):
        mocker.patch(
            'api.db.gallery.Gallery.get_photos',
            return_value=gallery_mock.internal_server_error()
        )
        gallery.photos_confirmed(Config.QUERY_LIMIT_DEFAULT, Config.QUERY_PAGE_DEFAULT)

def test_get_all_photos_success(mocker):
    mocker.patch(
        'api.db.gallery.Gallery.get_all_photos',
        return_value=gallery_mock.all_gallery()
    )
    test_class = gallery.get_all_photos(Config.QUERY_LIMIT_DEFAULT, Config.QUERY_PAGE_DEFAULT)
    assert test_class == gallery_mock.all_gallery()
    assert test_class[0]["pendent"] == "true"
    assert test_class[1]["pendent"] == "false"

def test_get_all_photos_success_error(mocker):
    with pytest.raises(Exception):
        mocker.patch(
            'api.db.gallery.Gallery.get_all_photos',
            return_value=gallery_mock.not_found_error()
        )
        gallery.photos_confirmed()

def test_get_photo_by_user_success(mocker):
    mocker.patch(
        'api.db.gallery.Gallery.get_user_photos',
        return_value=gallery_mock.all_gallery()
    )
    test_class = gallery.get_photos_by_user("62bee943d330b93cb604317d", Config.QUERY_LIMIT_DEFAULT, Config.QUERY_PAGE_DEFAULT)
    assert test_class == gallery_mock.all_gallery()
    assert test_class[0]["user_id"]["$oid"] == "62bee943d330b93cb604317d"
    assert test_class[0]["user_id"]["$oid"] != "62bee943d330b93cb604317f"

def test_get_photo_by_user_error(mocker):
    with pytest.raises(Exception):
        mocker.patch(
            'api.db.gallery.Gallery.get_user_photos',
            return_value=gallery_mock.not_found_error()
        )
        gallery.photos_confirmed()

def test_insert_success(mocker):
    json = {'photo_bucket': 'photo_bucket_test', 'pendent': 'true'}
    mocker.patch(
        'api.db.gallery.Gallery.insert',
        return_value=gallery_mock.gallery_mock_insert(json)
    )
    test_class = gallery.insert(json)
    assert test_class.photo_bucket == "photo_bucket_test"

def test_insert_error(mocker):
    with pytest.raises(Exception):
        json = {'photo_bucket': 'photo_bucket_test', 'pendent': 'true'}
        mocker.patch(
            'api.db.gallery.Gallery.insert',
            return_value=gallery_mock.internal_server_error()
        )
        gallery.insert(json)

def test_confirm_success(mocker):
    json = {'photo_bucket': 'photo_bucket_test', 'pendent': 'true'}
    mocker.patch(
        'api.db.gallery.Gallery.confirm',
        return_value=gallery_mock.gallery_mock_confirm(json)
    )
    test_class = gallery.confirm(json)
    assert test_class.photo_bucket == "photo_bucket_test"

def test_confirm_error(mocker):
    with pytest.raises(Exception):
        json = {'photo_bucket': 'photo_bucket_test', 'pendent': 'true'}
        mocker.patch(
            'api.db.gallery.Gallery.confirm',
            return_value=gallery_mock.internal_server_error()
        )
        gallery.insert(json)


