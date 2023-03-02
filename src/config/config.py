import os
import types
import yaml


class AttrDict(dict):
    """
    字典转换器
    """

    def __init__(self, *args, **kwargs) -> None:
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Config:
    PROJECT_NAME = 'wenbao-app'
    TIMEZONE = 'Asia/Shanghai'
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    # 模式
    ENV = "dev"
    # 服务worker数量
    WORKERS = 1

    # 跨域
    CORS_ORIGINS = "*"

    # 表单提交不需要加密
    WTF_CSRF_ENABLED = False

    # jwt
    JWT = {
        "secret_key": "wenbao",
        "access_token_expires": 1
    }

    # 初始化管理员账号
    ADMIN = {
        "username": "admin",
        "password": "admin123"
    }

    @classmethod
    def get_config(cls):
        """
        第二种配置加载方式
        加载 .yaml 文件

        修改实例，为app.config.update实际参数
        遍历实例参数，子类属性也会遍历
        """
        # 读取yaml配置
        with open(os.path.join(cls.BASE_DIR, f'config/db-{cls.ENV}.yaml')) as f:
            config_file_dict = AttrDict(yaml.safe_load(f))

        # 去掉method
        attr_gen = (i for i in dir(cls) if type(getattr(cls, i)) is not types.MethodType)

        # class 配置项
        class_config = {
            attr: getattr(cls, attr)
            for attr in attr_gen
            if not attr.startswith('__')
        }
        # 拼接配置
        class_config.update(config_file_dict)
        return class_config


if __name__ == '__main__':
    print(Config.get_config())