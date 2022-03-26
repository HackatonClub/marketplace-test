from datetime import timedelta

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

import app.queries.registr as registr
from app.auth.hash import get_password_hash
from app.auth.JWTtoken import create_access_token
from app.model import User
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES

registr_router = APIRouter(tags=["Registration"])


@registr_router.post('/registration')
async def registration_user(request: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_uid = await registr.check_login(request.username)
    if user_uid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with this login exists")
    if len(request.password) < 6 or request.password.isdigit():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Bad password, password shoud be better :)")
    request.password = get_password_hash(request.password)
    userreg = User(login=request.username, password=request.password)
    await registr.create_user(userreg)
    # generate a jwt token and return
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": request.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
