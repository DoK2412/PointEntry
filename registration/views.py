import jwt
import os

from fastapi.responses import JSONResponse

from proxy.proxy_client import RegisterService

from registration.madel_request import ConfirmRegistration


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
        response = await client.request(
            request.method,
            request.url.path,
            json=dict(user_data)
        )
        return JSONResponse(status_code=response.status_code, content={"date": response.json()})


async def confirm_registration_user(token, request):
    payload, error = await verify_token(token)
    if payload:

        user_data = ConfirmRegistration(**payload)
        async with RegisterService() as client:
            response = await client.request(
                "POST",
                request.url.path,
                json=dict(user_data)
            )
        return JSONResponse(status_code=response.status_code, content={"date": response.json()})

async def login(user):
    pass

async def profile(session_data):
    pass