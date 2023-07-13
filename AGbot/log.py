# https://loguru.readthedocs.io/en/stable/index.html
from loguru import logger
import sys

# 移除默认控制台输出
logger.remove()

# 添加控制台输出
logger.add(sys.stdout, level="INFO", colorize=True,
           format="[{time:YYYY-MM-DD HH:mm:ss}] [<level>{level}</level>]: <level>{message}</level>")

# 输出到文件
logger.add("./log/log_{time}.log", format="[{time:YYYY-MM-DD HH:mm:ss}] [{level}]: {message}",
           rotation="10 MB", retention="14 days")  # type: ignore


if __name__ == "__main__":
    logger.debug('This is debug information')
    logger.info('This is info information')
    logger.warning('This is warn information')
    logger.error('This is error information')
