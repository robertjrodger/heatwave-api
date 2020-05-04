"""
Middleware support for API-key authentication.
"""
from typing import Sequence

from fastapi import status
from starlette.datastructures import Headers
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class TrustedKeyMiddleware:

    __slots__ = ("app", "_allowed_keys")

    def __init__(self, app: ASGIApp, allowed_keys: Sequence[str],) -> None:
        self.app = app
        self._allowed_keys = tuple(allowed_keys)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        headers = Headers(scope=scope)
        key = headers.get("X-API-KEY")
        if key and key in self._allowed_keys:
            await self.app(scope, receive, send)
        else:
            response = PlainTextResponse(
                "Invalid or missing API key.", status_code=status.HTTP_403_FORBIDDEN
            )
            await response(scope, receive, send)
