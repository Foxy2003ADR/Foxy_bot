from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class GameState:
    connected: bool = False
    in_game: bool = False

    game: Optional[str] = None
    player_name: str = "Foxy"

    hp: Optional[int] = None
    max_hp: Optional[int] = None

    x: Optional[float] = None
    y: Optional[float] = None

    extra: dict[str, Any] = field(default_factory=dict)


class GameAdapter(ABC):
    """
    Adaptador base para cualquier juego.

    Cada juego implementará esta interfaz.
    """

    game_name: str = "unknown"

    def __init__(self, player_name: str = "Foxy"):
        self.player_name = player_name
        self.state = GameState(
            game=self.game_name,
            player_name=player_name
        )

    @abstractmethod
    async def connect(self, **config) -> GameState:
        """Conecta al juego."""
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self) -> GameState:
        """Desconecta del juego."""
        raise NotImplementedError

    @abstractmethod
    async def send_chat(self, message: str) -> GameState:
        """Envía un mensaje al chat del juego."""
        raise NotImplementedError

    @abstractmethod
    async def move(self, direction: str) -> GameState:
        """Mueve al personaje."""
        raise NotImplementedError

    @abstractmethod
    async def interact(self) -> GameState:
        """Realiza una interacción."""
        raise NotImplementedError

    async def get_state(self) -> GameState:
        """Devuelve el estado actual."""
        return self.state


class GameClient:
    """
    Cliente genérico que utiliza un GameAdapter.
    """

    def __init__(self, adapter: GameAdapter):
        self.adapter = adapter

    @property
    def game_name(self) -> str:
        return self.adapter.game_name

    @property
    def state(self) -> GameState:
        return self.adapter.state

    async def connect(self, **config) -> GameState:
        return await self.adapter.connect(**config)

    async def disconnect(self) -> GameState:
        return await self.adapter.disconnect()

    async def send_chat(self, message: str) -> GameState:
        return await self.adapter.send_chat(message)

    async def move(self, direction: str) -> GameState:
        return await self.adapter.move(direction)

    async def interact(self) -> GameState:
        return await self.adapter.interact()

    async def get_state(self) -> GameState:
        return await self.adapter.get_state()