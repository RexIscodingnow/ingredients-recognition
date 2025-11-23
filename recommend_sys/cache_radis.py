import redis


class RedisClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._create_instance()

        return cls._instance


    @classmethod
    def _create_instance(cls):
        redis_host = "localhost"
        redis_port = 7379
        redis_db = 0

        try:
            client = redis.Redis(host=redis_host,
                                 port=redis_port,
                                 db=redis_db,
                                 decode_responses=True)
            client.ping()
            return client

        except redis.ConnectionError as e:
            print(f"connection error: {e}")
            return None


    @classmethod
    def reset_instance(cls):
        if cls._instance:
            cls._instance.close()

        cls._instance = None


if __name__ == "__main__":
    redis_client = RedisClient.get_instance()

    redis_client.set('1', 55)
    val = redis_client.get('1')
    pipeline = redis_client.pipeline()

    for i in range(2, 6):
        pipeline.set(f"{i}", 55 + i)

    pipeline.execute()

    for i in range(6):
        val = redis_client.get(f"{i}")
        print(val)

