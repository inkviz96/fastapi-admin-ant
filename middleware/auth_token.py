from fastapi import Request
import jwt
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from admin import router, SECRET_KEY, JWT_ALGORITHM

import bcrypt
from database.database_connection import session
from sqlalchemy.orm import Session
from models import models

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.name==username).first()

# def check(body: bytes):
#     print('ddddddddddddddddd')
#     if body:
#         username, password = body.decode('utf-8').split("&")
#     else:
#         return (b"X-auth", b"0")
#     db: Session = session
#     user = get_user(db, username)
#     if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode("UTF-8")):
#         print('sssssssssssss')
#         payload = {"name": user.name, "time_expiration": (datetime.now() + timedelta(minutes=10)).timestamp()}
#         token = jwt.encode(payload, SECRET_KEY, JWT_ALGORITHM)
#         header_token = (b"X-Auth", token.encode("utf-8"))
#         return header_token


class AuthToken(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # do something with the request object

        token = request.headers.get("X-auth", None)
        if token and request.scope['path'] != "/admin/login/":
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            if datetime.now().timestamp() < decoded['time_expiration']:
                redirect_url = router.url_path_for("admin_panel")
                return RedirectResponse(redirect_url)
        elif not token and request.scope['path'] != "/admin/login/":
            redirect_url = router.url_path_for("login")
            return RedirectResponse(redirect_url)
        elif not token and request.scope['path'] == "/admin/login/":
            print(request.cookies)
            response = await call_next(request)
            return response
