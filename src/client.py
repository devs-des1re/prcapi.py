"""Client for the PRC Private Server API v1."""

from __future__ import annotations

import asyncio
from typing import Any, Callable, Coroutine

from .http import HTTPClient, Route
from .models import (
    CommandLog,
    JoinLog,
    KillLog,
    ModCall,
    Player,
    Server,
    Staff,
    Vehicle,
)


class Client:
    """Client for the PRC Private Server API v1.
    
    Args:
        server_key (str | None): The server key to use.
        authorization (str | None): The authorization to use.
    """

    def __init__(
        self,
        server_key: str | None = None,
        *,
        authorization: str | None = None,
    ):
        """Initialize the client.
        
        Args:
            server_key (str | None): The server key to use.
            authorization (str | None): The authorization to use.
        """
        self.server_key = server_key
        self.authorization = authorization
        self._http: HTTPClient | None = None
        self._on_ready: Callable[..., Coroutine[Any, Any, Any]] | None = None
        self._events: dict[str, Callable[..., Coroutine[Any, Any, Any]]] = {}
        self._closed = False

    def event(self, coro: Callable[..., Coroutine[Any, Any, Any]]):
        """Decorator to register an event handler.
        
        Args:
            coro (Callable[..., Coroutine[Any, Any, Any]]): The event handler.
            
        Returns:
            Callable[..., Coroutine[Any, Any, Any]]: The event handler.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("Event handler must be a coroutine function")
        name = coro.__name__
        if name == "on_ready":
            self._on_ready = coro
        else:
            if not hasattr(self, "_events"):
                self._events = {}
            self._events[name] = coro
        return coro

    def _ensure_http(self) -> HTTPClient:
        """Ensure the HTTP client is initialized.
        
        Returns:
            HTTPClient: The HTTP client.
        """
        if self._http is None:
            if not self.server_key:
                raise RuntimeError("Server API has not been set.")
            self._http = HTTPClient(
                self.server_key,
                authorization=self.authorization,
            )
        return self._http

    def run(
        self,
        server_key: str | None = None,
        *,
        authorization: str | None = None,
    ) -> None:
        """Start the client (blocking).
        
        Args:
            server_key (str | None): The server key to use.
            authorization (str | None): The authorization to use.
        """
        if server_key is not None:
            self.server_key = server_key
        if authorization is not None:
            self.authorization = authorization

        async def _runner():
            await self._start()
            try:
                await asyncio.Future()
            except asyncio.CancelledError:
                pass
            finally:
                await self.close()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_runner())
        except KeyboardInterrupt:
            pass
        finally:
            if not self._closed:
                loop.run_until_complete(self.close())
            loop.close()

    async def _start(self) -> None:
        """Start the client.
        
        Returns:
            None: The client is started.
        """
        self._ensure_http()
        if self._on_ready is not None:
            await self._on_ready(self)

    async def close(self) -> None:
        """Close the client and release resources.
        
        Returns:
            None: The client is closed.
        """
        if self._closed:
            return
        if self._http is not None:
            await self._http.close()
            self._http = None
        self._closed = True

    # ---------- API methods (v1) ----------

    async def get_server(self) -> Server:
        """Fetch server status (GET /server).
        
        Returns:
            Server: The server status.
        """
        data = await self._ensure_http().request(Route("GET", "/server"))
        return Server.from_api(data)

    async def get_players(self) -> list[Player]:
        """Fetch players currently in the server (GET /server/players).
        
        Returns:
            list[Player]: The players currently in the server.
        """
        data = await self._ensure_http().request(Route("GET", "/server/players"))
        if isinstance(data, list):
            return [Player.from_api(p) for p in data]
        return []

    async def run_command(self, command: str) -> dict[str, Any]:
        """Run a command as "virtual server management" (POST /server/command).
        
        Args:
            command (str): The command to run.
            
        Returns:
            dict[str, Any]: The data from the API.
        """
        data = await self._ensure_http().request(
            Route("POST", "/server/command"),
            json={"command": command},
        )
        return data or {}

    async def get_joinlogs(self) -> list[JoinLog]:
        """Fetch join logs (GET /server/joinlogs).
        
        Returns:
            list[JoinLog]: The join logs.
        """
        data = await self._ensure_http().request(Route("GET", "/server/joinlogs"))
        if isinstance(data, list):
            return [JoinLog.from_api(e) for e in data]
        return []

    async def get_queue(self) -> list[int]:
        """Fetch players in queue by Roblox ID (GET /server/queue).
        
        Returns:
            list[int]: The players in queue.
        """
        data = await self._ensure_http().request(Route("GET", "/server/queue"))
        return data if isinstance(data, list) else []

    async def get_killlogs(self) -> list[KillLog]:
        """Fetch kill logs (GET /server/killlogs).
        
        Returns:
            list[KillLog]: The kill logs.
        """
        data = await self._ensure_http().request(Route("GET", "/server/killlogs"))
        if isinstance(data, list):
            return [KillLog.from_api(e) for e in data]
        return []

    async def get_commandlogs(self) -> list[CommandLog]:
        """Fetch command logs (GET /server/commandlogs).
        
        Returns:
            list[CommandLog]: The command logs.
        """
        data = await self._ensure_http().request(Route("GET", "/server/commandlogs"))
        if isinstance(data, list):
            return [CommandLog.from_api(e) for e in data]
        return []

    async def get_modcalls(self) -> list[ModCall]:
        """Fetch moderator call logs (GET /server/modcalls).
        
        Returns:
            list[ModCall]: The moderator call logs.
        """
        data = await self._ensure_http().request(Route("GET", "/server/modcalls"))
        if isinstance(data, list):
            return [ModCall.from_api(e) for e in data]
        return []

    async def get_bans(self) -> dict[str, Any]:
        """Fetch bans (GET /server/bans). Returns object keyed by PlayerId.
        
        Returns:
            dict[str, Any]: The bans.
        """
        data = await self._ensure_http().request(Route("GET", "/server/bans"))
        return data if isinstance(data, dict) else {}

    async def get_vehicles(self) -> list[Vehicle]:
        """Fetch spawned vehicles (GET /server/vehicles).
        
        Returns:
            list[Vehicle]: The spawned vehicles.
        """
        data = await self._ensure_http().request(Route("GET", "/server/vehicles"))
        if isinstance(data, list):
            return [Vehicle.from_api(v) for v in data]
        return []

    async def get_staff(self) -> Staff:
        """Fetch server staff - mods and admins (GET /server/staff). Deprecated by API.
        
        Returns:
            Staff: The server staff.
        """
        data = await self._ensure_http().request(Route("GET", "/server/staff"))
        return Staff.from_api(data or {})
