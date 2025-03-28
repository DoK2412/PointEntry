import jwt
import os

from fastapi.responses import JSONResponse

from proxy.proxy_client import RegisterService

from registration.model_request import ConfirmRegistration


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("AUTH_JWT_KEY"), algorithms=[os.getenv("ALGORITHM")])
        return payload, True
    except jwt.ExpiredSignatureError:
        return None, False
    except Exception:
        return None, False


async def registration_user(user_data, request):

    async with RegisterService() as client:
        answer = await client.request(
            request.method,
            request.url.path,
            json=dict(user_data)
        )
        return JSONResponse(status_code=answer.status_code, content={"date": answer.json()})


async def confirm_registration_user(token, request):
    payload, error = await verify_token(token)
    if payload:

        user_data = ConfirmRegistration(**payload)
        async with RegisterService() as client:
            answer = await client.request(
                "POST",
                request.url.path,
                json=dict(user_data)
            )
        return JSONResponse(status_code=answer.status_code, content={"date": answer.json()})

async def login(user, request, response):
    async with RegisterService() as client:
        answer = await client.request(
            request.method,
            request.url.path,
            json=dict(user)
        )
        if answer.status_code == 200:
            answer_json = answer.json()

            response.set_cookie(
                key="SecureRefreshToken",
                value=answer_json['refresh_token'],
                httponly=True,
                max_age=os.getenv("TIME_COOKIES"),
                secure=True,
                samesite="strict",
            )
            return JSONResponse(status_code=answer.status_code, content={"date": {"access_token": answer_json['access_token']}})
        else:
            return JSONResponse(status_code=answer.status_code, content={"date": answer.json()})


async def profile(session_data):
    pass