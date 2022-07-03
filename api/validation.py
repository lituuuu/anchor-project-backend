from api.custom_errors import CustomErrors
from bson.objectid import ObjectId

def header_has_valid_file(request):
    try:
        photo = request.files["file"]
    except Exception:
        raise CustomErrors.InternalServer("No file in request")

    if photo.filename == "":
        raise CustomErrors.InternalServer("No file in request")
    if not photo.filename.endswith(".jpg") and not photo.filename.endswith(".jpeg"):
        raise CustomErrors.InternalServer("Not supported file extension, only jpg or jpeg")
    return True


def is_user_admin(user_admin):
    if not user_admin:
        raise CustomErrors.Unauthorized()

def valid_field(content, field):
    try:
        valid_content = content[field]
        if not valid_content:
            raise Exception
    except Exception as e:
        raise CustomErrors.InternalServer("Field validation error")

def valid_objectid(id):
    try:
        ObjectId(id)
    except Exception as e:
        raise CustomErrors.InternalServer("Id is not valid")