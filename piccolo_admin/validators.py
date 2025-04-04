from piccolo.apps.user.tables import BaseUser
from piccolo_api.crud.endpoints import PiccoloCRUD
from starlette.middleware.exceptions import HTTPException
from starlette.requests import Request


def superuser_validators(_: PiccoloCRUD, request: Request):
    """
    We need to provide extra validation on certain tables (e.g. user and
    sessions), so only superusers can perform certain actions, otherwise the
    security of the application can be compromised.
    """
    user: BaseUser = request.user.user
    if user.superuser:
        return
    if request.method.upper() in ["PUT", "PATCH", "DELETE", "POST"]:
        raise HTTPException(
            status_code=405,
            detail="Only superusers can perform these actions.",
        )
