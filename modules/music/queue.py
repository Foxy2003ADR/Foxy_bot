from dataclasses import dataclass, field


@dataclass
class Song:
    title: str
    url: str
    webpage_url: str
    duration: int | None = None
    requester: str | None = None


@dataclass
class MusicQueue:
    songs: list[Song] = field(default_factory=list)
    current_index: int = -1

    @property
    def current(self):
        if 0 <= self.current_index < len(self.songs):
            return self.songs[self.current_index]
        return None

    def add(self, song: Song):
        self.songs.append(song)

    def next(self):
        if self.current_index + 1 < len(self.songs):
            self.current_index += 1
            return self.current
        return None

    def previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            return self.current
        return None

    def clear(self):
        self.songs.clear()
        self.current_index = -1

    def has_next(self):
        return self.current_index + 1 < len(self.songs)

    def has_previous(self):
        return self.current_index > 0


# Una cola independiente para cada servidor de Discord
queues: dict[int, MusicQueue] = {}


def get_queue(guild_id: int) -> MusicQueue:
    if guild_id not in queues:
        queues[guild_id] = MusicQueue()

    return queues[guild_id]