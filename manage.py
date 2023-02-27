import asyncio
import peewee
from rich.console import Console
from rich import print as rprint
from src.config import CONFIG
from src.extension import InitMysql
from migrations import MigratorOperate
from src.models import RoleTypeEnum, RoleModel, UserModel
from src.utils import gen_random, gen_password, auto_load_gen

config_data = CONFIG.get_config()
mgr = InitMysql(config_data['mysql']).mgr()

console = Console()


def log(msg, mode='info'):
    style = {
        'info': "bold blue",
        'warn': "bold yellow",
        'error': "bold red",
        'start': 'bold yellow',
        'done': "bold green"
    }
    console.print(f'【{config_data["PROJECT_NAME"]}】{msg}', style=style[mode])


async def run():
    log("开始安装...", mode='start')
    await create_table()
    # await role()
    # await admin()
    await mgr.close()
    log("安装完成", mode='done')


async def create_table():
    log("开始创建数据表...")
    # 获取模块
    models = auto_load_gen('src.models.__init__')
    for model in models:
        # 通过子类判断更加合理
        if issubclass(model, peewee.Model):
            MigratorOperate(model)
            log(f"生成表 {model._meta.table_name}")

    log("数据表创建完成!", mode='done')


async def role():
    log("初始化系统默认角色...")
    role_list = [
        {
            "name": "管理员",
            "type": RoleTypeEnum.ADMIN.value
        },
        {
            "name": "用户",
            "type": RoleTypeEnum.USER.value
        }
    ]
    await mgr.execute(
        RoleModel.insert_many(role_list)
    )
    log("系统默认角色创建完成!", mode='done')


async def admin():
    log("初始化管理员账号...")
    admin_data = config_data.get('ADMIN', dict(username="admin", password="admin123"))
    salt = gen_random(length=12)
    admin_data['salt'] = salt
    admin_data['password'] = gen_password(admin_data['password'], salt)
    admin_role_gen = await mgr.execute(
        RoleModel.select().where((RoleModel.type == RoleTypeEnum.ADMIN.value))
    )
    admin_data['role'] = admin_role_gen[0]['id']
    admin_data['age'] = 10
    rprint(admin_data)
    await mgr.execute(
        UserModel.insert(**admin_data)
    )
    log("管理员账号创建完成！", mode='done')


if __name__ == '__main__':
    asyncio.run(run())
