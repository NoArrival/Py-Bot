#!/usr/bin/env python
# -*- coding:utf-8 -*-

import uvicorn,os,telegram
from fastapi import FastAPI
from pydantic import BaseModel
from Process import command_message,text_message,default

app = FastAPI()
token = ''

if os.name == 'nt':
    proxy = telegram.utils.request.Request(proxy_url='http://127.0.0.1:10809')
    bot = telegram.Bot(token=token, request=proxy)
else:
    bot = telegram.Bot(token=token)



class Webhook_request(BaseModel):
    update_id: int
    message: dict = None


command_selection = {                       #事先获得函数地址，注，此处函数并未执行。
        "/start": command_message.start,
        "/help": command_message.help,
        "/query": command_message.query,
          }

@app.post("/")
def main(data:Webhook_request):
    data = data.dict()
    info = default.Get_info_Message(data)

    if info.isUnknown:              #检测用户发送数据类型是否未知，若未知，则发送消息错误提示
        result = "请发送命令消息或文本消息"
    else:                           #命令分发，此处实现用的是字典的get方法
        execute = command_selection.get(info.command,text_message.repetition)       #注：该处函数并未执行
        result = execute(info.text)                 #执行对应函数，获取返回内容

    bot.send_message(chat_id=info.chat_id, text=result)
    return {"status": "请求成功"}


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        debug=True)
