import traceback
import json
import asyncio

from .log import logger
from .配置 import 配置
from . import api
from . import 消息处理

'''
from log import log

from bot import api
from bot import 私聊消息处理
from bot import 群聊消息处理
'''

分割线 = "\n------------------------------\n"


async def 启动主程序(请求数据):
    try:
        return await 主程序(请求数据)
    except:  # Exception as e:
        # print(type(e), e)
        # exc_type, exc_value, exc_obj = sys.exc_info()
        错误信息 = traceback.format_exc()  # limit=1
        错误信息 = "执行 主程序 时出现报错,报错信息:\n{}\n请求数据:{}".format(错误信息, 请求数据)
        logger.error(错误信息)
        try:
            # api.发送私聊消息(配置文件.管理员QQ号,  错误信息)#+ str(type(e)) + str(e))
            pass
        except Exception as e:
            logger.warning(f"{type(e)}: {e}")  # type: ignore
            logger.warning("发送错误信息失败")
        try:
            # 写入报错信息
            with open(file="./log/报错信息.txt", mode="w", encoding="utf-8")as f:
                f.write(错误信息)
        except Exception as e:
            logger.warning(f"{type(e)}: {e}")  # type: ignore
            logger.warning("写入错误信息失败")

def 入群欢迎(请求数据):
    return
    群号 = 请求数据["group_id"]
    QQ号 = 请求数据["user_id"]
    # 新成员管理的群名单 = 配置文件.新成员管理的群名单
    路径 = "./请求数据/config/入群欢迎.json"
    try:
        with open(路径, "r", encoding="UTF-8") as f:
            请求数据 = f.read()
            logger.debug(请求数据)
            请求数据 = json.loads(请求数据)
            logger.debug("请求数据: " + str(请求数据))
        新成员管理的群名单 = 请求数据
    except:
        say = '''入群欢迎出现错误：\n {}'''.format(traceback.format_exc())
        logger.error(say)
        新成员管理的群名单 = []
    logger.info("开始处理！新成员管理的群名单：" + str(新成员管理的群名单))
    是否欢迎 = False
    for i in 新成员管理的群名单:
        if int(i) == int(群号):
            是否欢迎 = True
    if 是否欢迎:
        import random
        内容 = 配置文件.入群欢迎语
        内容 = 内容[random.randint(0, len(内容) - 1)]
        if 内容.find("{qq_id}") != -1:
            内容 = 内容.format(qq_id=QQ号)
        api.发送群消息(群号, 内容)


async def 主程序(请求数据):
    if 请求数据["post_type"] != "meta_event":
        logger.debug("收到post请求:" + 分割线 + str(请求数据) + 分割线)
    if 请求数据["post_type"] == "message" or 请求数据["post_type"] == "message_sent":
        if 请求数据["message_type"] == "group":
            群名称 = await api.获取群信息(请求数据["group_id"])
            say = f'收到来自群 {群名称["群名称"]}({请求数据["group_id"]}) 内 {请求数据["sender"]["nickname"]}({请求数据["sender"]["user_id"]}) 的id为: {请求数据["message_id"]} 的消息：{请求数据["message"]}'
            logger.info(say)
            await 消息处理.群聊消息处理(请求数据)
        elif 请求数据["message_type"] == "private":
            if 请求数据["post_type"] == "message":
                say = f'收到来自: {请求数据["sender"]["nickname"]}({请求数据["user_id"]})id为: {请求数据["message_id"]} 消息,消息内容：{请求数据["message"]}'
                logger.info(say)
                # 私聊消息处理.私聊消息处理(请求数据)
            elif 请求数据["post_type"] == "message_sent":
                say = f'收到来自: {请求数据["sender"]["nickname"]}({请求数据["user_id"]}) 发给 {请求数据["target_id"]} id为: {请求数据["message_id"]} 消息,消息内容：{请求数据["message"]}'
                logger.info(say)
                # 私聊消息处理.私聊消息处理(请求数据)
    elif 请求数据["post_type"] == "notice":
        if 请求数据["notice_type"] == "group_increase":
            群名称 = await api.获取群信息(请求数据["group_id"])
            群成员信息 = await api.获取群成员信息(请求数据["group_id"], 请求数据["user_id"])
            say = f'群 {群名称["群名称"]}({请求数据["group_id"]}) 内有了新成员: {群成员信息["昵称"]}({请求数据["user_id"]})'
            logger.info(say)
            入群欢迎(请求数据)
        elif 请求数据["notice_type"] == "group_decrease":
            if 请求数据["sub_type"] == "leave":
                子类型 = "成员主动退群"
            elif 请求数据["sub_type"] == "kick":
                子类型 = "成员被踢"
            elif 请求数据["sub_type"] == "kick_me":
                子类型 = "登录号被踢"
            else:
                子类型 = "未知"
            群名称 = await api.获取群信息(请求数据["group_id"])
            say = f'群 {群名称["群名称"]}({请求数据["group_id"]}) 内有{子类型}: {api.获取陌生人信息(请求数据["user_id"])["昵称"],}({请求数据["user_id"]})'
            logger.info(say)
        elif 请求数据["notice_type"] == "group_recall":
            群名称 = await api.获取群信息(请求数据["group_id"])
            if 请求数据["user_id"] == 请求数据["operator_id"]:
                群成员信息 = await api.获取群成员信息(请求数据["group_id"], 请求数据["user_id"])
                say = "群 {群名称}({群号}) 内的 {消息发送者昵称}({消息发送者}) 撤回了一条消息,消息id:{消息id}".format(群名称=群名称["群名称"],
                                                                                       群号=请求数据["group_id"],
                                                                                       消息发送者昵称=群成员信息["昵称"],
                                                                                       消息发送者=请求数据["user_id"],
                                                                                       消息id=请求数据["message_id"])
            else:
                消息发送者昵称 = await api.获取群成员信息(请求数据["group_id"], 请求数据["user_id"])
                操作者昵称 = await api.获取群成员信息(
                    请求数据["group_id"], 请求数据["operator_id"])
                say = "群 {群名称}({群号}) 内的 {操作者昵称}({操作者QQ号}) 撤回了一条成员 {消息发送者昵称}({消息发送者}) 的消息,消息id:{消息id}".format(群名称=群名称,
                                                                                                             群号=请求数据["group_id"],
                                                                                                             操作者昵称=操作者昵称["昵称"],
                                                                                                             操作者QQ号=请求数据["operator_id"],
                                                                                                             消息发送者昵称=消息发送者昵称["昵称"],
                                                                                                             消息发送者=请求数据["user_id"],
                                                                                                             消息id=请求数据["message_id"])
            logger.info(say)
        elif 请求数据["notice_type"] == "group_ban":
            群号 = 请求数据["group_id"]
            操作者 = 请求数据["operator_id"]
            被禁言者 = 请求数据["user_id"]
            禁言时长 = 请求数据["duration"]
            群名称 = await api.获取群信息(群号)
            if 请求数据["sub_type"] == "ban":
                # 禁言
                say = "群 {群名称}({群号}) 内的成员 {被禁言者} 被 {操作者} 禁言 {禁言时长} 秒".format(群名称=群名称["群名称"],
                                                                             群号=群号,
                                                                             被禁言者=被禁言者,
                                                                             操作者=操作者,
                                                                             禁言时长=禁言时长)
                logger.info(say)
            elif 请求数据["sub_type"] == "lift_ban":
                # 解除禁言
                say = "群 {群名称}({群号}) 内的成员 {被禁言者} 被 {操作者} 解除禁言,禁言时长 {禁言时长} 秒".format(群名称=群名称,
                                                                                    群号=群号,
                                                                                    被禁言者=被禁言者,
                                                                                    操作者=操作者,
                                                                                    禁言时长=禁言时长)
                logger.info(say)
