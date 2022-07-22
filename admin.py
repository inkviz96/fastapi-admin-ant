import os

from fastapi.staticfiles import StaticFiles
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from users.forms import UserCreateForm
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
# from models.models import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Union

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates/")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from pydantic import BaseModel
#
# def fake_hash_password(password: str):
#     return "fakehashed" + password
#
# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }

#
# class UserInDB(User):
#     hashed_password: str
#
#
# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
#
#
# def fake_decode_token(token):
#     # This doesn't provide any security at all
#     # Check the next version
#     user = get_user(fake_users_db, token)
#     return user
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user
#
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
# @router.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     return {"access_token": user.username, "token_type": "bearer"}
#
#
# @router.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
#
#
# @router.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}



from sqlalchemy.orm import Session
import bcrypt
from models import models
from database.database_connection import session
import jwt
from datetime import datetime, timedelta
from utils.decorators import auth_required
from utils.sql_admin import get_all_objects, get_model_fields, get_object, update_obj
from utils.data import short
from ad import Admin

SECRET_KEY=os.getenv("SECRET_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.name==username).first()


@router.get("/", response_class=HTMLResponse)
@router.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {'request': request, 'result': True})

@router.post("/", response_class=HTMLResponse)
@router.post("/login/", response_class=HTMLResponse)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    db: Session = session
    user = get_user(db, form_data.username)
    try:
        if user and bcrypt.checkpw(form_data.password.encode('utf-8'), user.password.encode("UTF-8")):
            payload = {"name": user.name, "time_expiration": (datetime.now() + timedelta(minutes=10)).timestamp()}
            token = jwt.encode(payload, SECRET_KEY, JWT_ALGORITHM)
            redirect_url = router.url_path_for("admin_panel")
            response = RedirectResponse(redirect_url)
            response.set_cookie(key="X-Auth", value=token)
            return response
        else:
            return templates.TemplateResponse("login.html", {'request': request, 'result': False})
    except Exception as e:
        print(e)
        return templates.TemplateResponse("login.html", {'request': request, 'result': False})
from utils.sql_admin import get_all

@router.post("/admin_panel/", response_class=HTMLResponse)
@auth_required
async def admin_panel(request: Request):
    models = list(get_all())
    response = templates.TemplateResponse("admin_panel.html", {"request": request, "models": models})
    response.set_cookie(request.cookies.get("X-Auth"))
    return response


@router.get("/admin_panel/", response_class=HTMLResponse)
@auth_required
async def admin_panel(request: Request):
    # models = list(get_all())
    models = Admin().models
    response = templates.TemplateResponse("admin_panel.html", {"request": request, "models": models})
    response.set_cookie(request.cookies.get("X-Auth"))
    return response


@router.get("/model/{name}/", response_class=HTMLResponse)
@auth_required
async def model(request: Request, name: str):
    objects = short(get_all_objects(name))
    # models = list(get_all())
    models = Admin().models
    fields = [field[1] for field in get_model_fields(name)]
    response = templates.TemplateResponse("objects.html", {"request": request, "models": models, "objects": objects, "fields": fields})
    response.set_cookie(request.cookies.get("X-Auth"))
    return response


@router.get("/edit/{model}/{id}/")
@auth_required
async def edit(request: Request, model: str, id: int):
    obj = get_object(model, id)
    # models = list(get_all())
    models = Admin().models
    fields = [field[1] for field in get_model_fields(model)]
    response = templates.TemplateResponse("edit.html", {"request": request, "models": models, "objects": obj, "fields": fields})
    response.set_cookie(request.cookies.get("X-Auth"))
    return response


@router.post("/edit/{model}/{id}/")
@auth_required
async def edit(request: Request, model:str, id: int, form_data: dict = Form(...)):
    # models = list(get_all())
    models = Admin().models
    fields = [field[1] for field in get_model_fields(model)]
    query = [f"{key}={value} " for key, value in form_data.items()]
    update_obj(table_name=model, id=id, fields=fields, query=query)
    obj = get_object(model, id)
    response = templates.TemplateResponse("edit.html", {"request": request, "models": models, "objects": obj, "fields": fields})
    response.set_cookie(request.cookies.get("X-Auth"))
    return response
