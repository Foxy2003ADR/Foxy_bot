from __future__ import annotations

from typing import Callable, Optional

from .base import GameAdapter, GameClient


AdapterFactory = Callable[..., GameAdapter]


class GameClientManager:
    """
    Gestiona los clientes de juego de Foxy.

    Permite añadir nuevos juegos sin modificar el núcleo.
    """

    def __init__(self):
        self._adapters: dict[str, AdapterFactory] = {}
        self._clients: dict[int, GameClient] = {}

    # ---------------------------------------------------------
    # REGISTRO DE JUEGOS
    # ---------------------------------------------------------

    def register(
        self,
        name: str,
        adapter_factory: AdapterFactory
    ) -> None:

        name = name.lower().strip()

        self._adapters[name] = adapter_factory

    def unregister(self, name: str) -> None:
        self._adapters.pop(name.lower().strip(), None)

    def available_games(self) -> list[str]:
        return sorted(self._adapters.keys())

    def has_game(self, name: str) -> bool:
        return name.lower().strip() in self._adapters

    # ---------------------------------------------------------
    # CLIENTES
    # ---------------------------------------------------------

    def get_client(self, user_id: int) -> Optional[GameClient]:
        return self._clients.get(user_id)

    def is_connected(self, user_id: int) -> bool:
        client = self.get_client(user_id)

        if client is None:
            return False

        return client.state.connected

    async def connect(
        self,
        user_id: int,
        game: str,
        player_name: str = "Foxy",
        **config
    ) -> GameClient:

        game = game.lower().strip()

        if game not in self._adapters:
            raise ValueError(
                f"Juego no registrado: {game}"
            )

        # Si ya existe un cliente, lo desconectamos.
        old_client = self._clients.get(user_id)

        if old_client is not None:
            try:
                await old_client.disconnect()
            except Exception:
                pass

        adapter = self._adapters[game](
            player_name=player_name
        )

        client = GameClient(adapter)

        await client.connect(**config)

        self._clients[user_id] = client

        return client

    async def disconnect(self, user_id: int) -> bool:

        client = self._clients.get(user_id)

        if client is None:
            return False

        try:
            await client.disconnect()
        finally:
            self._clients.pop(user_id, None)

        return True

    async def disconnect_all(self) -> None:

        clients = list(self._clients.items())

        self._clients.clear()

        for _, client in clients:
            try:
                await client.disconnect()
            except Exception:
                pass

    async def get_state(self, user_id: int):

        client = self.get_client(user_id)

        if client is None:
            return None

        return await client.get_state()