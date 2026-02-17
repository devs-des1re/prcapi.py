"""
PRC Private Server API v1 wrapper.

Usage::

    from library import Client

    client = Client()

    @client.event
    async def on_ready(client):
        server = await client.get_server()
        print(server.name)

    client.run("your-api-key")
"""

from .client import Client
from .exceptions import (
    APIError,
    Forbidden,
    HTTPException,
    PRCException,
    RateLimited,
)
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

__all__ = [
    "Client",
    "Server",
    "Player",
    "JoinLog",
    "KillLog",
    "CommandLog",
    "ModCall",
    "Vehicle",
    "Staff",
    "PRCException",
    "HTTPException",
    "Forbidden",
    "RateLimited",
    "APIError",
]


__version__ = "0.0.1"
