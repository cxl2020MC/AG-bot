from typing import Any
from .log import logger
import importlib
import functools


class 插件:
    def __init__(self, 插件名称: str, 插件描述: str = "") -> None:
        self.插件名称 = 插件名称
        self.插件描述 = 插件描述
        logger.debug(f"注册插件 {插件名称} 成功")


class Router:
    def __init__(self, 路由列表=None):
        self.路由列表 = 路由列表 or []  # 初始化路由列表，如果没有传入路由列表，则创建空列表

    def 祖传(self, name, command):
        '''
        注册命令处理程序。
        '''
        logger.debug(f"注册命令处理程序: {name}, {command}")
        
        def decorator(func):
            @functools.wraps(func)
            async def wrapped(*args, **kwargs):
                return await func(*args, **kwargs)
            
            route_data = {
                "name": name,
                "command": command,
                "handler": wrapped
            }
            logger.debug(f"路由数据: {route_data}")
            self.路由列表.append(route_data)
            return wrapped
        return decorator

路由 = Router()  # 创建路由实例


def 加载插件(插件名称: str, **导入配置) -> None:
    logger.info(f"加载插件: {插件名称} ")
    插件 =  importlib.import_module(插件名称, **导入配置)
    logger.info(f"插件 {插件名称} 加载成功")


if __name__ == "__main__":
    pass
