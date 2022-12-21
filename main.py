from typing import List
import fastapi as _fastapi
from fastapi import File, UploadFile, Form, BackgroundTasks
import fastapi.security as _security

import sqlalchemy.orm as _orm
from fastapi.middleware.cors import CORSMiddleware
import services as _services, schemas as _schemas
from database import Base, engine
from starlette.responses import JSONResponse

import services as _services, schemas as _schemas


Base.metadata.create_all(bind=engine)


app = _fastapi.FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.post("/api/users", tags=["users"])
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Votre email est déjà utilisé")

    user = await _services.create_user(user, db)

    return await _services.create_token(user)



@app.post("/api/token", tags=["users"])
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Utilisateur non enregistré")

    return await _services.create_token(user)




@app.get("/api/users/me", tags=["users"], response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user


@app.delete("/api/user/me/delete", tags=["users"])
async def delete_user(user : _schemas.User = _fastapi.Depends(_services.delete_current_user)):
    return user



@app.get("/")
async def root():
    return {"message": "Hello World"}