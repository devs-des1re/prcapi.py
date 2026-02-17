"""HTTP client for PRC API v1 with rate limit handling."""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp

from .exceptions import Forbidden, HTTPException, RateLimited

BASE_URL = "https://api.policeroleplay.community/v1"


class Route:  # pylint: disable=too-few-public-methods
    """Represents an API route.
    
    Args:
        method (str): The HTTP method to use.
        path (str): The path to the API route.
    """

    def __init__(self, method: str, path: str):
        self.method = method
        self.path = path
        self.url = f"{BASE_URL}{path}"


class HTTPClient:
    """Low-level HTTP client with Server-Key auth and rate limit respect.
    
    Args:
        server_key (str): The server key to use.
        authorization (str | None): The authorization to use.
        session (aiohttp.ClientSession | None): The session to use.
    """

    def __init__(
        self,
        server_key: str,
        *,
        authorization: str | None = None,
        session: aiohttp.ClientSession | None = None,
    ):
        self.server_key = server_key
        self.authorization = authorization
        self._session = session
        self._owned_session = session is None

    def _headers(self) -> dict[str, str]:
        """Get the headers for the HTTP client.
        
        Returns:
            dict[str, str]: The headers for the HTTP client.
        """
        headers = {
            "server-key": self.server_key,
            "Content-Type": "application/json",
        }
        if self.authorization:
            headers["Authorization"] = self.authorization
        return headers

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get the session for the HTTP client.
        
        Returns:
            aiohttp.ClientSession: The session for the HTTP client.
        """
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(headers=self._headers())
        return self._session

    async def request(
        self,
        route: Route,
        *,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Request the API.

        Args:
            route (Route): The route to request.
            json (dict[str, Any] | None, optional): The JSON data to send. Defaults to None.

        Raises:
            Forbidden: The server key is invalid or unauthorized.
            RateLimited: The request is rate limited.
            HTTPException: The request failed.
            HTTPException: The request is rate limited.

        Returns:
            Any: The data from the API.
        """
        session = await self._get_session()
        url = route.url

        for attempt in range(2):
            async with session.request(
                route.method,
                url,
                json=json,
                headers=self._headers(),
            ) as resp:
                data = None
                if resp.content_type == "application/json":
                    try:
                        data = await resp.json()
                    except (aiohttp.ContentTypeError, ValueError):
                        pass
                if data is None and resp.content_length:
                    data = {"message": (await resp.text())}

                if resp.status == 200:
                    return data

                if resp.status == 403:
                    raise Forbidden((data or {}).get("message", "Unauthorized"))

                if resp.status == 429:
                    body = data or {}
                    retry_after = float(body.get("retry_after", 5))
                    bucket = body.get("bucket") or resp.headers.get("X-RateLimit-Bucket")
                    if attempt == 0 and retry_after > 0:
                        await asyncio.sleep(retry_after)
                        continue
                    raise RateLimited(
                        body.get("message", "Rate limited"),
                        retry_after=retry_after,
                        bucket=bucket,
                    )

                message = (data or {}).get("message", resp.reason or f"HTTP {resp.status}")
                raise HTTPException(resp.status, message, data)

        raise HTTPException(429, "Rate limited")

    async def close(self) -> None:
        """Close the HTTP client.
        
        Returns:
            None: The HTTP client is closed.
        """
        if self._owned_session and self._session and not self._session.closed:
            await self._session.close()
