from sanic.log import logger
from motor.motor_asyncio import AsyncIOMotorClient
from src.utils import singleton


@singleton
class MotorBase:
    _db = {}
    _collection = {}

    def __init__(self, host='127.0.0.1', port='27017', username=None, password=None, database=''):
        self.motor_uri = ''
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def client(self, db_name):
        self.motor_uri = 'mongodb://{account}{host}:{port}/{database}'.format(
            account='{username}:{password}@'.format(
                username=self.username,
                password=self.password) if self.username else '',
            host=self.host,
            port=self.port,
            database=db_name)
        logger.info(f"mongo 连接地址 {self.motor_uri}")
        return AsyncIOMotorClient(self.motor_uri)

    # @property
    # def db(self):
    #     if self._db is not None:
    #         self._db = self.client(self.database)[self.database]
    #     return self._db

    def get_db(self, db_name):
        """
        db 缓存
        db 实例
        :param db_name:
        :return:
        """
        db_name = db_name if db_name is None else self.database
        logger.info(f'获取 mongo/{db_name} 库实例')
        if db_name not in self._db:
            self._db[db_name] = self.client(db_name)[db_name]
        return self._db[db_name]

    def get_collection(self, db_name, collection):
        """
        集合缓存
        获取一个集合实例
        :param db_name:
        :param collection:
        :return:
        """
        collection_key = db_name + collection
        logger.info(f'获取 mongo/{db_name}.{collection} 集合实例')
        if collection_key not in self._collection:
            self._collection[collection_key] = self.get_db(db_name)[collection]

        return self._collection[collection_key]


if __name__ == '__main__':
    import asyncio
    from src.config.config import Config

    mb = MotorBase(**Config.get_config()['mongo'])
    mongo_db = mb.get_db('yx-d2c')

    async def run(db):
        data = {
            "adminId": 'A123321',
            "openId": "123321321321",
            'dbs': [
                {
                    'cartItemId': "A998480_261146_261146_1670295716042",
                    'levelPrice': "300",
                    'salePrice': "300",
                    'spuId': "261146",
                    'skuId': "g471382",
                    'shopId': "A998480",
                    'quantity': 1
                }
            ]
        }

        result = await db.wxa_cart.insert_one(data)

        print(result)

        return result

    async def query(db):
        ...

    asyncio.run(run(mongo_db))
