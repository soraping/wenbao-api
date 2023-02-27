import asyncio_redis


class RedisSession:
    """
    建立redis连接池
    """
    _pool = None

    @classmethod
    async def get_redis_pool(cls, redis_config_dict):
        if not cls._pool:
            cls._pool = await asyncio_redis.Pool.create(**redis_config_dict)

        return cls._pool


if __name__ == '__main__':
    import asyncio
    from src.config.config import Config

    redis_pool = RedisSession.get_redis_pool


    async def do_set():
        redis_connection = await redis_pool(Config.get_config()['redis'])
        await redis_connection.set('name', 'name1')
        res = await redis_connection.get('name')
        print("get name: {0}".format(res))
        return res

    asyncio.run(do_set())