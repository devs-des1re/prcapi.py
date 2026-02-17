"""Data models for PRC API v1 responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Server:  # pylint: disable=too-many-instance-attributes
    """Server status from GET /server.
    
    Args:
        name (str): The name of the server.
        owner_id (int): The ID of the owner of the server.
        co_owner_ids (list[int]): The IDs of the co-owners of the server.
        current_players (int): The current number of players on the server.
        max_players (int): The maximum number of players the server can hold.
    """

    name: str
    owner_id: int
    co_owner_ids: list[int]
    current_players: int
    max_players: int
    join_key: str
    acc_verified_req: str
    team_balance: bool

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Server:
        """Create a Server object from the API data.
        
        Args:
            data (dict[str, Any]): The API data.
            
        Returns:
            Server: The Server object.
        """
        return cls(
            name=data.get("Name", ""),
            owner_id=data.get("OwnerId", 0),
            co_owner_ids=data.get("CoOwnerIds", []),
            current_players=data.get("CurrentPlayers", 0),
            max_players=data.get("MaxPlayers", 0),
            join_key=data.get("JoinKey", ""),
            acc_verified_req=data.get("AccVerifiedReq", ""),
            team_balance=data.get("TeamBalance", False),
        )


@dataclass
class Player:
    """Player in server from GET /server/players.
    
    Args:
        player (str): The name of the player.
        permission (str): The permission of the player.
        callsign (str | None): The callsign of the player.
        team (str): The team of the player.
    """

    player: str
    permission: str
    callsign: str | None
    team: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Player:
        """Create a Player object from the API data.
        
        Args:
            data (dict[str, Any]): The API data.
            
        Returns:
            Player: The Player object.
        """
        return cls(
            player=data.get("Player", ""),
            permission=data.get("Permission", ""),
            callsign=data.get("Callsign"),
            team=data.get("Team", ""),
        )


@dataclass
class JoinLog:
    """Join log entry from GET /server/joinlogs.
    
    Args:
        join (bool): Whether the player joined the server.
        timestamp (int): The timestamp of the join.
        player (str): The name of the player.
    """

    join: bool
    timestamp: int
    player: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> JoinLog:
        """Create a JoinLog object from the API data.
        
        Args:
            data (dict[str, Any]): The API data.
            
        Returns:
            JoinLog: The JoinLog object.
        """
        return cls(
            join=data.get("Join", False),
            timestamp=data.get("Timestamp", 0),
            player=data.get("Player", ""),
        )


@dataclass
class KillLog:
    """Kill log entry from GET /server/killlogs.
    
    Args:
        killed (str): The name of the player who was killed.
        timestamp (int): The timestamp of the kill.
        killer (str): The name of the player who killed the player.
    """

    killed: str
    timestamp: int
    killer: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> KillLog:
        """Create a KillLog object from the API data.
        
        Args:
            data (dict[str, Any]): The API data.
            
        Returns:
            KillLog: The KillLog object.
        """
        return cls(
            killed=data.get("Killed", ""),
            timestamp=data.get("Timestamp", 0),
            killer=data.get("Killer", ""),
        )


@dataclass
class CommandLog:
    """Command log entry from GET /server/commandlogs.
    
    Args:
        player (str): The name of the player who executed the command.
        timestamp (int): The timestamp of the command.
        command (str): The command that was executed.
    """

    player: str
    timestamp: int
    command: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CommandLog:
        """Create a CommandLog object from the API data.
        
        Args:
            data (dict[str, Any]): The API data.
            
        Returns:
            CommandLog: The CommandLog object.
        """
        return cls(
            player=data.get("Player", ""),
            timestamp=data.get("Timestamp", 0),
            command=data.get("Command", ""),
        )


@dataclass
class ModCall:
    """Mod call entry from GET /server/modcalls.
    
    Args:
        caller (str): The name of the player who called the mod.
        moderator (str | None): The name of the moderator who responded to the mod call.
        timestamp (int): The timestamp of the mod call.
    """

    caller: str
    moderator: str | None
    timestamp: int

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> ModCall:
        """Create a ModCall object from the API data.
        
        Args:
            data (dict[str, Any]): The API data.
            
        Returns:
            ModCall: The ModCall object.
        """
        return cls(
            caller=data.get("Caller", ""),
            moderator=data.get("Moderator"),
            timestamp=data.get("Timestamp", 0),
        )


@dataclass
class Vehicle:
    """Spawned vehicle from GET /server/vehicles.
    
    Args:
        texture (str | None): The texture of the vehicle.
        name (str): The name of the vehicle.
        owner (str): The name of the player who owns the vehicle.
    """

    texture: str | None
    name: str
    owner: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Vehicle:
        """Create a Vehicle object from the API data.
        
        Args:
            data (dict[str, Any]): The API data.
            
        Returns:
            Vehicle: The Vehicle object.
        """
        return cls(
            texture=data.get("Texture"),
            name=data.get("Name", ""),
            owner=data.get("Owner", ""),
        )


@dataclass
class Staff:
    """Server staff (deprecated) from GET /server/staff.
    
    Args:
        co_owners (list[int]): The IDs of the co-owners of the server.
        admins (dict[str, str]): The admins of the server.
        mods (dict[str, str]): The mods of the server.
    """

    co_owners: list[int]
    admins: dict[str, str]
    mods: dict[str, str]

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Staff:
        """Create a Staff object from the API data.
        
        Args:
            data (dict[str, Any]): The API data.
            
        Returns:
            Staff: The Staff object.
        """
        return cls(
            co_owners=data.get("CoOwners", []),
            admins=data.get("Admins", {}),
            mods=data.get("Mods", {}),
        )
