import datetime
from typing import Dict, Union
from peewee import (
    DateTimeField,
    Model
)
from playhouse.shortcuts import model_to_dict

from src.config import CONFIG
from src.extension.db import InitMysql

ModelDictType = Dict[str, Union[datetime.datetime, int, str]]

database = InitMysql(CONFIG.get_config()['mysql'])()


class BaseModel(Model):
    create_time = DateTimeField(default=datetime.datetime.utcnow, formats='%Y-%m-%d %H:%M:%S',
                                verbose_name='create time')
    update_time = DateTimeField(default=datetime.datetime.utcnow, formats='%Y-%m-%d %H:%M:%S',
                                verbose_name='modify time')

    def model_to_dict(self, exclude=None) -> ModelDictType:
        """
        model 转 dict
        能递归，更方面
        :return:
        """
        return model_to_dict(self, exclude=exclude)

    # def to_dict(self) -> Dict[str, Union[datetime.datetime, int, str]]:
    #     """
    #     model 转 dict
    #     不能递归
    #     :return:
    #     """
    #     return {f: getattr(self, f) for f in self._meta.fields}

    def __getitem__(self, key):
        return self.__dict__['__data__'].get(key, '')

    class Meta:
        database = database
