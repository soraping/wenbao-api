import functools
from datetime import datetime
from playhouse.migrate import MySQLDatabase, MySQLMigrator, Model, migrate as peewee_migrate
from peewee import (
    PrimaryKeyField,
    CharField,
    DateTimeField
)
from src.config import CONFIG

config_dict = CONFIG.get_config()
db_manager = MySQLDatabase(**config_dict['mysql'])
migrator = MySQLMigrator(db_manager)


def migration_record(version='1.0', author='admin', desc=''):
    """
    记录操作
    :return:
    """
    def decorator(fn):
        @functools.wraps(fn)
        def _decorator(*args, **kwargs):
            fn(*args, **kwargs)
            target_self = args[0]
            MigrationRecordModel.create(
                table=target_self._name,
                create_time=datetime.utcnow(),
                version=version,
                author=author,
                desc=desc,
                function=target_self.__class__.__name__ + '.' + fn.__name__
            )
        return _decorator
    return decorator


class MigrationRecordModel(Model):
    """
    表操作模型
    """
    id = PrimaryKeyField()
    table = CharField(null=True)
    version = CharField(null=True)
    author = CharField(null=True)
    function = CharField(null=True)
    desc = CharField(null=True)
    create_time = DateTimeField(verbose_name='创建时间',
                                default=datetime.utcnow(), help_text='表操作记录')

    class Meta:
        table_name = 'migration_record'
        database = db_manager


class MigratorOperate:
    _db = db_manager
    _migrator = migrator

    def __init__(self, model):
        # 操作记录初始化
        self._mr = MigrationRecordModel()
        self._db.create_tables(([self._mr]), safe=True)

        # 对应模型
        self._model = model
        self._model._meta.database = self._db

        # 建表
        self._model.create_table(safe=True)
        # 表名
        self._name = self._model._meta.table_name

    def add_column(self, col, field=None):
        """
        新增字段
        :param col:
        :param field:
        :return:
        """
        print('Migrating==> [%s] add_column: %s' % (self._name, col))
        field = getattr(self._model, col) if not field else field
        return peewee_migrate(self._migrator.add_column(self._name, col, field))

    def rename_column(self, old, new):
        """
        重命名字段名
        :param old:
        :param new:
        :return:
        """
        print('Migrating==> [%s] rename_column: (%s)-->(%s)' % (self._name, old, new))
        return peewee_migrate(self._migrator.rename_column(self._name, old, new))

    def drop_column(self, col):
        """
        删除字段
        :param col:
        :return:
        """
        print('Migrating==> [%s] drop_column: %s' % (self._name, col))
        return peewee_migrate(self._migrator.drop_column(self._name, col))

    def drop_not_null(self, col):
        """
        可以为空
        :param col:
        :return:
        """
        print('Migrating==> [%s] drop_not_null: %s' % (self._name, col))
        return peewee_migrate(self._migrator.drop_not_null(self._name, col))

    def add_not_null(self, col):
        """
        不可为空
        :param col:
        :return:
        """
        print('Migrating==> [%s] add_not_null: %s' % (self._name, col))
        return peewee_migrate(self._migrator.add_not_null(self._name, col))

    def add_unique(self, *cols):
        """
        唯一约束
        :param cols:
        :return:
        """
        return peewee_migrate(self._migrator.add_unique(self._name, *cols))

    @migration_record()
    def auto_migrate(self):
        # 新增字段 排除父类字段以及魔术方法
        model_owner_args_gen = (args for args in set(dir(self._model)) - set(dir(Model)) if
                                not args.startswith("_") and args != "DoesNotExist")
        for args in model_owner_args_gen:
            field = getattr(self._model, args)
            self.add_column(args, field)

    @migration_record()
    def add_table_column(self, col):
        """
        新增一个表字段
        :param col:
        :return:
        """
        self.add_column(col, getattr(self._model, col))


if __name__ == '__main__':
    from src.models import RoleModel, UserModel
    mr = MigratorOperate(RoleModel)
    # mr.add_table_column('desc')
