from orjson import dumps
from sanic import Sanic
from sanic.log import logger
from sanic_ext import Extend

from src.config import CONFIG
from src.core.context import MyContent, Request
from src.core.exceptions import InitErrorHandler
from src.extension.jwt_ext import JwtExt
from src.extension.db import InitMysql
from src.views import bg_group

# 配置信息
app_config = CONFIG.get_config()

# 服务
app = Sanic(name=app_config['PROJECT_NAME'],
            dumps=dumps,
            ctx=MyContent(),
            request_class=Request,
            log_config=app_config['BASE_LOGGING'])
app.config.update(app_config)

# 扩展
Extend(app)

# 注册路由
app.blueprint(bg_group)


@bg_group.middleware('request')
async def interceptor(request: Request):
    request.ctx = request.app.ctx
    # forms 模块使用 session 对象
    # 使用了jwt，没有必要再用引入 sanic-session
    request.ctx.session = {}


@app.after_server_start
async def setup(app: Sanic, loop) -> None:
    logger.info("app start")
    logger.info(f"启动环境 => {app.config['ENV']}")
    logger.info(f"启动核心 => {app.config['WORKERS']}")

    # 异常处理
    InitErrorHandler.initialize(app)

    # # 注册 redis
    # redis_pool = RedisSession.get_redis_pool(app.config['redis'])
    # app.ctx.redis = await redis_pool
    # logger.info("redis 连接成功")

    # jwt
    with JwtExt.initialize(app) as manager:
        manager.config.secret_key = app.config['JWT']['secret_key']

    # # 注册 mysql
    app.ctx.db = InitMysql(app.config['mysql']).mgr()

    #
    # # 注册 mongo
    # app.ctx.mongo = MotorBase(**app.config['mongo']).get_db(app.config['mongo']['database'])
    # logger.info("mongo 连接成功")


@app.after_server_stop
async def stop(app: Sanic):
    logger.info("app stop")
    await app.ctx.db.close()
    # await app.ctx.redis.close()
    # await app.ctx.mongo.close()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8089,
        workers=app.config['WORKERS'],
        debug=app.config['DEBUG'],
        access_log=app.config['ACCESS_LOG'])
