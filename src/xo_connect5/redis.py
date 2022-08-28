from redis import StrictRedis
from xo_connect5.models.users import OrderType, User, UserInDB


class RedisClient:
    def __init__(self) -> None:
        self._client = StrictRedis()

    async def get_order_from_db(self, user: User) -> OrderType:
        order_bytes = self._client.hget(name='order', key=user.name)
        if not order_bytes:
            return OrderType.NONE

        order = order_bytes.decode()
        if order not in [OrderType.FIRST, OrderType.DRAW]:
            order = OrderType.NONE
        return order

    async def get_user_in_db(self, user: User) -> UserInDB:
        order = await self.get_order_from_db(user)
        return UserInDB(name=user.name, order=order)


async def get_order_from_db(user: User) -> OrderType:
    redis_client = RedisClient()
    order = await redis_client.get_order_from_db(user)
    return order


async def get_user_in_db(user: User) -> UserInDB:
    redis_client = RedisClient()
    user_in_db = await redis_client.get_user_in_db(user)
    return user_in_db
