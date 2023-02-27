from src.models.base import BaseModel
from peewee import (
    IntegerField,
    PrimaryKeyField,
    CharField,
    ForeignKeyField
)
from .roles import RoleModel


class UserModel(BaseModel):
    id = PrimaryKeyField()
    username = CharField(max_length=20, verbose_name='user name')
    password = CharField(max_length=50, verbose_name='user password')
    salt = CharField(max_length=16, verbose_name='password salt')
    age = IntegerField(null=True, verbose_name='user age')
    role = ForeignKeyField(model=RoleModel, null=True, on_delete='SET NULL', verbose_name='role for user')

    class Meta:
        table_name = 'user'
