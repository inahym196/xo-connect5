from xo_connect5.models.users import Players, User

from redis import StrictRedis


class RedisClientError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail


class RedisClient:
    def __init__(self) -> None:
        self._client = StrictRedis()

    async def get_players(self, board_id: int) -> Players:
        players_bytes = self._client.hget(name=f'board{board_id}', key='players')
        if not players_bytes:
            raise RedisClientError(detail=f'board{board_id}-players key is not exist')

        split_players = players_bytes.decode().split(':')
        if len(split_players) != 2:
            raise RedisClientError(detail=f'board{board_id}-players key cannot parse')

        first_username, draw_username = split_players[0], split_players[1]
        if first_username == '_' and draw_username == '_':
            return Players(first=None, draw=None)
        return Players(first=User(name=first_username), draw=User(name=draw_username))


async def get_players_from_db(board_id: int) -> Players:
    redis_client = RedisClient()
    players = await redis_client.get_players(board_id)
    return players
