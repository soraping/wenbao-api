from peewee import (
    CharField,
    PrimaryKeyField,
    ForeignKeyField
)
from .base import BaseModel
from .category import CategoryModel


class GoodsModel(BaseModel):
    """
    商品资料
    """
    id = PrimaryKeyField()
    catId = ForeignKeyField(model=CategoryModel, null=True, on_delete='SET NULL', verbose_name='role for user')
    name = CharField(max_length=20, verbose_name='商品名称')
    spuId = CharField(max_length=10, verbose_name='商品spu')


    producer = CharField(max_length=10, verbose_name='商品作者')
    spec = CharField(max_length=50, verbose_name='规格')
    stuff = CharField(max_length=50, verbose_name='材料')
    content = CharField(max_length=255, verbose_name='详情')

    class Meta:
        table_name = 'goods'
