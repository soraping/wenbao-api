import os
from enum import Enum


class ModeEnum(Enum):
    DEV = 'DEV'
    PRO = 'PRO'

    @classmethod
    def __missing__(cls, value):
        for mode in cls:
            if mode.value == value.upper():
                return mode


def load_config():
    """
    第一种配置文件加载方式
    :return:
    """
    mode = os.environ.get('MODE', ModeEnum.DEV.value)

    try:
        if mode == ModeEnum.PRO.value:
            from .pro_config import ProConfig
            ProConfig.ENV = "pro"

            # 生成日志文件路径
            if not os.path.exists(ProConfig.LOGGING_INFO_FILE):
                os.makedirs(os.path.dirname(ProConfig.LOGGING_INFO_FILE))

            return ProConfig
        else:
            from .dev_config import DevConfig
            return DevConfig

    except ImportError:
        from .config import Config
        return Config


CONFIG = load_config()
