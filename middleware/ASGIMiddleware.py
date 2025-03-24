import typing
import os
import jwt

from fastapi import Response
from fastapi.responses import JSONResponse
from uuid import uuid4

from session import SessionData, cookie, backend

from dotenv import load_dotenv

load_dotenv()


Scope = typing.MutableMapping[str, typing.Any]
Message = typing.MutableMapping[str, typing.Any]

Receive = typing.Callable[[], typing.Awaitable[Message]]
Send = typing.Callable[[Message], typing.Awaitable[None]]

ASGIApp = typing.Callable[[Scope, Receive, Send], typing.Awaitable[None]]


def get_token_from_headers(headers: typing.List[typing.Tuple]):
    """
    Функция предназначена для получения ролей авторизованного пользователя
    headers: содержит данные из заголовка необходим для получения токена пользователя
    """
    for row in headers:
        if row[0].decode() == 'authorization':
            auth = [row for row in headers if row[0].decode() == 'authorization'][0]
            return auth[1].decode().split('Bearer ')[-1]
    else:
        return None

async def verify_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("AUTH_JWT_KEY"), algorithms=[os.getenv("ALGORITHM")])
        return payload, True
    except jwt.ExpiredSignatureError:
        return None, False
    except Exception:
        return None, False


class ASGIMiddleware:

    def __init__(self, app,):
        self.app = app
        self.response = Response()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        if scope["type"] not in ["http", "https"]:
            return await self.app(scope, receive, send)
        if scope['path'] in os.getenv("IGNORED_REQUESTS"):
            return await self.app(scope, receive, send)
        token = get_token_from_headers(scope['headers'])
        if token:
            payload, error = await verify_token(token)
            if payload is not None:
                # session = uuid4()
                # data = SessionData(username=payload['user_id'])
                # await backend.create(session, data)
                # cookie.attach_to_response(self.response, session)
                # print(0)
                # # return await self.response(scope, receive, send)
                return await self.app(scope, receive, send)
            else:
                response = JSONResponse(content={'code': '403', 'message': 'Токен авторизации не активен, обновите токен'})
                return await response(scope, receive, send)
        else:
            response = JSONResponse(content={'code': '403', 'message': 'Токен авторизации не найден.'})
            return await response(scope, receive, send)