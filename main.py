from fastapi import FastAPI
import admin
from fastapi.middleware.cors import CORSMiddleware
from middleware.auth_token import AuthToken


app = FastAPI()

# """CORS settings"""
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.add_middleware(AuthToken)


app.include_router(admin.router)
