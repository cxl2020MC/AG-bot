from .log import logger
from .插件 import 路由
from .配置 import 配置

async def 群聊消息处理(请求数据):
    消息 = 请求数据["message"]
    if not 消息:
        logger.warning("此消息为空，放弃此消息")
        return
    # for 配置.get("消息", []).get("群聊", []): # type: ignore
    #     pass
    if 消息[0] == "/":
        消息 = 消息.split(" ")
        for 路由信息 in 路由.路由列表:
            for i in 路由信息["命令"]:
                if i == 消息[0]:
                    logger.info(f'匹配到命令 {i}')
                    await 路由信息["方法"](请求数据, 消息)