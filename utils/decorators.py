from fastapi.responses import RedirectResponse
from admin import router
from functools import wraps
import jwt
import os

SECRET_KEY=os.getenv("SECRET_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs["request"].cookies.get("X-Auth")
        if token and jwt.decode(token, SECRET_KEY, JWT_ALGORITHM):
            return await func(*args, **kwargs)
        else:
            redirect_url = router.url_path_for("login")
            return RedirectResponse(redirect_url)

    return wrapper
