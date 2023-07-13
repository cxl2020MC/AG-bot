from AGbot.插件 import 路由
from AGbot import api

@路由.注册命令处理器("echo", ["/echo"])
async def echo(请求数据, 消息):
    群号 = 请求数据["group_id"]
    api.发送群消息(群号, str(消息))