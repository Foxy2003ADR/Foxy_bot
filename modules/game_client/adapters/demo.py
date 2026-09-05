from ..base import GameAdapter, GameState


class DemoAdapter(GameAdapter):

    game_name = "demo"

    async def connect(self, **config) -> GameState:

        self.state.connected = True
        self.state.in_game = True

        self.state.x = 0
        self.state.y = 0

        self.state.hp = 100
        self.state.max_hp = 100

        self.state.extra = {
            "message": "Foxy ha entrado al mundo de prueba."
        }

        return self.state

    async def disconnect(self) -> GameState:

        self.state.connected = False
        self.state.in_game = False

        self.state.extra = {
            "message": "Foxy ha salido del mundo de prueba."
        }

        return self.state

    async def send_chat(self, message: str) -> GameState:

        self.state.extra["last_chat"] = message

        return self.state

    async def move(self, direction: str) -> GameState:

        direction = direction.lower().strip()

        if direction == "arriba":
            self.state.y += 1

        elif direction == "abajo":
            self.state.y -= 1

        elif direction == "izquierda":
            self.state.x -= 1

        elif direction == "derecha":
            self.state.x += 1

        else:
            self.state.extra["error"] = (
                f"Dirección desconocida: {direction}"
            )

        self.state.extra["last_move"] = direction

        return self.state

    async def interact(self) -> GameState:

        self.state.extra["last_action"] = "interactuar"

        return self.state