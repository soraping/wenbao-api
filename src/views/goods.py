from sanic import response, Blueprint

goods_bp = Blueprint('goods', url_prefix='/goods')


@goods_bp.get('/list')
async def get_goods_list(request):
    await request.app.ctx.redis.set('name', 'zhangsan')
    name = await request.app.ctx.redis.get('name')
    return response.json({"goods_list": [1, 2, 3]})
