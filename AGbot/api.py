import requests
import aiohttp
import traceback
import re
from .log import logger
from typing import Any

try:
    from .配置 import 配置
    cqhttpurl = 配置["go_cqhttp"]["url"]
except Exception:
    print('配置文件导入失败')
    traceback.print_exc()
    cqhttpurl = "http://127.0.0.1:5700"


async def 发送私聊消息(QQ号: Any, message: str) -> None:
    logger.info(f"发送私聊消息到QQ: {QQ号} ，消息内容: {message}")
    url = f"{cqhttpurl}/send_private_msg"
    post_data = {"user_id": QQ号, "message": message}
    logger.debug(f"请求gocqhttp({url})data:{post_data}")
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=post_data) as resp:
            data = await resp.json()
            logger.debug(f"gocqhttp返回:{data}")
            if data["status"] == "failed":
                发送api调用失败消息(url, post_data, data)


async def 发送群消息(群号, message) -> None:
    logger.info("发送群消息到: {群号} ，消息内容: {message}".format(群号=群号, message=message))
    url = cqhttpurl + "/send_group_msg"
    post_data = {"group_id": 群号, "message": message}
    logger.debug(f"请求gocqhttp({url})data:{post_data}")
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=post_data) as resp:
            data = await resp.json()
            logger.debug(f"gocqhttp返回:{data}")
            if data["status"] == "failed":
                发送api调用失败消息(url, post_data, data)


def 发送api调用失败消息(url, 请求数据, 返回数据):
    报错消息模板 = '''请求url: {url} 时出现问题!
data: {请求数据}
go-cqhttp返回: {返回数据}'''
    内容 = 报错消息模板.format(url=url, 请求数据=请求数据, 返回数据=返回数据)
    # import 配置文件
    # 发送私聊消息(配置文件.管理员QQ号, 内容)
    raise Exception(内容)


async def 获取群信息(群号) -> dict:
    url = cqhttpurl + "/get_group_info"
    post_data = {"group_id": 群号}
    # print("请求gocqhttp（" + url + "）data:" + str(data))
    # data = requests.post(url, post_data).json()
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=post_data) as resp:
            data = await resp.json()
            # print("gocqhttp返回：" + str(post_data))
            try:
                群名称 = data['data']['group_name']
            except Exception:
                群名称 = '未知'
            try:
                群备注 = data['data']['group_memo']
            except Exception:
                群备注 = '未知'
            return {'群名称': 群名称, '群备注': 群备注}


async def 群组单人禁言(群号, QQ号, 禁言时间):
    url = cqhttpurl + "/set_group_ban"
    data = {"group_id": 群号, "user_id": QQ号, "duration": 禁言时间}
    print("请求gocqhttp（" + url + "）data:" + str(data))
    post = requests.post(url, data)
    post_data = post.json()
    print("gocqhttp返回：" + str(post_data))
    if post_data['retcode'] != 0:
        # return post_data['wording']
        await 发送群消息(群号, str(post_data))


def 撤回消息(消息id):
    url = cqhttpurl + "/delete_msg"
    data = {"message_id": 消息id}
    print("请求gocqhttp（" + url + "）data:" + str(data))
    post = requests.post(url, data)
    post_data = post.json()
    print("gocqhttp返回：" + str(post_data))


def 冒泡排序法(arr):
    n = len(arr)
    # 遍历所有数组元素
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def 获取当前路径():
    import os
    path = os.getcwd()
    # path = os.path.abspath('.')
    print('path:', path)
    return path


def 获取文件路径(file_name):
    import os
    # path = os.getcwd()
    path = os.path.abspath(file_name)
    print('path:', path)
    return path


def 下载文件(url, file_name):
    down_res = requests.get(url=url)
    with open(file_name, "wb") as code:
        code.write(down_res.content)
    path = 获取文件路径(file_name)
    return path


def cqcode解析(text):
    pattern = r'\[CQ:(\w+)(.*?)\]'
    matches = re.findall(pattern, text)
    ret_data = {}
    for match in matches:
        type = match[0]
        data = {}
        for item in match[1].split(','):
            if item.strip():
                key, value = item.split('=')
                # data[key] = value.strip()
                data.update({key: value})
        ret_data.update({type: data})
    return ret_data


def 获取消息(消息id):
    url = cqhttpurl + "/get_msg"
    data = {"message_id": 消息id}
    print("请求gocqhttp（" + url + "）data:" + str(data))
    post = requests.post(url, data)
    post_data = post.json()
    print("gocqhttp返回：" + str(post_data))
    data = post_data['data']
    发送者 = data['sender']
    发送时间 = data['time']
    消息内容 = data['message']
    return {'发送者': 发送者, '发送时间': 发送时间, '消息内容': 消息内容}


def 群组全员禁言(群号, 是否禁言):
    url = cqhttpurl + "/set_group_whole_ban"
    data = {"group_id": 群号, 'enable': 是否禁言}
    print("请求gocqhttp（" + url + "）data:" + str(data))
    post = requests.post(url, data)
    post_data = post.json()
    print("gocqhttp返回：" + str(post_data))


def 获取陌生人信息(QQ号) -> dict:
    url = cqhttpurl + "/get_stranger_info"
    data = {"user_id": QQ号}
    logger.debug("请求gocqhttp（" + url + "）data:" + str(data))
    post = requests.post(url, data)
    post_data = post.json()
    logger.debug("gocqhttp返回：" + str(post_data))
    data = post_data['data']
    昵称 = data['nickname']
    性别 = data['sex']
    年龄 = data['age']
    qid = data['qid']
    if 性别 == 'male':
        性别 = '男'
    elif 性别 == 'female':
        性别 = '女'
    elif 性别 == 'unknown':
        性别 = '未知'
    return {'昵称': 昵称, '性别': 性别, '年龄': 年龄, 'qid': qid}


async def 获取群成员信息(群号, QQ号) -> dict:
    url = cqhttpurl + "/get_group_member_info"
    post_data = {"group_id": 群号, "user_id": QQ号}
    logger.debug(f"请求gocqhttp({url}) data:" + str(post_data))

    # data = requests.post(url, post_data).json()
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=post_data) as resp:
            data = await resp.json()

            logger.debug(f"gocqhttp返回: {data}")

            data = data['data']
            昵称 = data['nickname']
            性别 = data['sex']
            年龄 = data['age']
            角色 = data['role']
            if 性别 == 'male':
                性别 = '男'
            elif 性别 == 'female':
                性别 = '女'
            elif 性别 == 'unknown':
                性别 = '未知'

            if 角色 == 'owner':
                角色 = '群主'
            elif 角色 == 'admin':
                角色 = '管理员'
            elif 角色 == 'member':
                角色 = '成员'
            return {'昵称': 昵称, '性别': 性别, '年龄': 年龄, '角色': 角色}


def 获取登录号信息():
    url = cqhttpurl + "/get_loggerin_info"
    data = requests.post(url)
    return data.json()['data']


def 拼接命令(命令, 开始):
    number = 0
    msg = ''
    for i in 命令:
        if number >= 开始:
            msg = msg + i + ' '
        number = number + 1
    return msg


def 创建文件夹(路径):
    import os
    # 创建文件夹
    路径 = 路径.strip()
    路径 = 路径.rstrip("\\")
    是否存在 = os.path.exists(路径)

    if not 是否存在:
        os.makedirs(路径)
        print(路径+"创建成功")
        return True
    else:
        print(路径+"已存在")
