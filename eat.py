#!/usr/bin/env python3
#encoding=utf-8
import json
import requests
def sendmesssage(message):
    url = "https://oapi.dingtalk.com/robot/send?access_token=a320162d58121be30990b6c00b2cb14f579250aaacaa56bc3d06650165eb43e5"
    HEADERS = {
        "Content-Type":"application/json;charset=utf-8"
    }
    String_TextMsg = {
        "msgtype":"text",
        "text":{"content":"吃饭吃饭！"+ message},#"吃饭吃饭！"自定义的机器人关键字配置的这样，所以要跟上关键字，要不然发送失败报310000错误
        "at":{
            "isAtAll":"true"
        }
    }
    String_TextMsg = json.dumps(String_TextMsg)
    res = requests.post(url, data=String_TextMsg, headers=HEADERS)
    print(res.text)
if __name__ == "__main__":
    message = "人是铁饭是钢一顿不吃饿的慌，赶紧吃饭！"
    sendmesssage(message)