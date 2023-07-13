from fastapi import FastAPI, Request
from .log import logger
from . import main

app = FastAPI()

@app.post("/")
async def json_endpoint(request: Request):
    data = await request.json()
    ret_data = await main.启动主程序(data)
    if ret_data:
        return ret_data
    else:
        return {}