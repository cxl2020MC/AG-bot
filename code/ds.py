import time
import random
import json
from typing import Any
from hashlib import md5


def get_ds(body: Any, query: str = ""):
    # 将要使用的salt，此为2.44.1版本的salt。
    salt = "xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs"
    # body(post)和query(get)一般来说不会同时存在。
    # 可以使用json库的dumps函数将对象转为JSON字符串。
    body = json.dumps(body)
    # query = "&".join(sorted(query.split("&")))
    t = int(time.time())
    # 直接用更简单粗暴的方法
    r = random.randint(100001, 200000)
    main = f"salt={salt}&t={t}&r={r}&b={body}&q={query}"
    print(main)
    ds = md5(main.encode(encoding='UTF-8')).hexdigest()

    final = f"{t},{r},{ds}" # 最终结果。
    return final