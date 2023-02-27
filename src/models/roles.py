from enum import Enum
from peewee import (
    CharField,
    PrimaryKeyField
)
from src.models.base import BaseModel


class RoleTypeEnum(Enum):
    """
    角色类型
    """
    USER = 'USER'
    # 管理员
    ADMIN = 'ADMIN'
    # 自定义
    CUSTOM = 'CUSTOM'


class RoleModel(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=20, verbose_name='role name')
    type = CharField(max_length=20, verbose_name='role type')

    class Meta:
        table_name = 'roles'