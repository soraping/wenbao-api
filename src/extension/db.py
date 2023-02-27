from peewee_async import PooledMySQLDatabase, MySQLDatabase, Manager
from playhouse.shortcuts import ReconnectMixin
from src.utils import custom_exceptions


class InitMysql:
    _db = None

    def __init__(self, db_config):
        self.config = db_config

    def db(self) -> MySQLDatabase:
        """
        初始化mysql, 返回 MySQLDatabase 实例
        :return:
        """
        if InitMysql._db is None:
            InitMysql._db = ReconnectMySQLDatabase.get_db_instance(self.config)
        return InitMysql._db

    def __call__(self):
        return self.db()

    def mgr(self) -> Manager:
        """
        初始化mysql, 返回 Manager 实例
        :return:
        """
        mgr = Manager(self.db())
        # if not mgr.is_connected:
        #     raise custom_exceptions.MysqlConnectionError
        return mgr


class BaseMysqlDB:
    _instance = None


class MySQLDatabaseConnection(MySQLDatabase, BaseMysqlDB):
    @classmethod
    def get_db_instance(cls, db_config):
        if not cls._instance:
            cls._instance = cls(**db_config)
        return cls._instance


class ReconnectMySQLDatabase(ReconnectMixin, MySQLDatabaseConnection):
    """
    可断线重连db
    """
    pass


class ReconnectAsyncPooledMySQLDatabase(ReconnectMixin, PooledMySQLDatabase, BaseMysqlDB):
    """
    可断线重连的异步db连接池
    """

    @classmethod
    def get_db_instance(cls, db_config):
        if not cls._instance:
            cls._instance = cls(**db_config, max_connections=10)
        return cls._instance


if __name__ == '__main__':
    print(isinstance(ReconnectMySQLDatabase({}), MySQLDatabase))
