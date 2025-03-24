from idlelib.query import Query

from fastapi import APIRouter, Request, Depends, Response, Query

from path import *
from registration.madel_request import Registration, Login
from registration.views import (registration_user,
                                confirm_registration_user, login, profile)

from fastapi.security import OAuth2PasswordBearer

from session import cookie, SessionData, verifier


registration = APIRouter(prefix="/registr", tags=["Registration"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@registration.post(REGISTER)
async def post_register(register: Registration, request: Request):
    result = await registration_user(register, request)
    return result


@registration.get(CONFIRMATION_REGISTR)
async def post_confirmation_register(request: Request,
                                     data: str = Query(description="Временный токен подтверждения.")):
    result = await confirm_registration_user(data, request)
    return result

@registration.post(LOGIN)
async def get_login(user: Login):
    result = await login(user)
    return result

@registration.get(PROFILE, dependencies=[Depends(cookie)])
async def get_profile(session_data: SessionData = Depends(verifier)):
    print(session_data)
    result = await profile(session_data)
    return result

