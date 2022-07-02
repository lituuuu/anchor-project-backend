from api.custom_errors import CustomErrors

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
        raise CustomErrors.Unauthorized("You shall not pass")
