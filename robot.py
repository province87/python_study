#!/usr/bin/env python3
#encoding=utf-8
import json
import requests
def sendmesssage(message):
    url = "https://oapi.dingtalk.com/robot/send?access_token=ad4a906bf3389fda5fc14f77161b2ed410c1cf422253af4a51a45e19a97d3015"
    HEADERS = {
        "Content-Type":"application/json;charset=utf-8"
    }
    String_TextMsg={
        "msgtype":"link",
        "link":{
            "text":"日报"+ message,
            "title":"交日报了！",
            "PicUrl":"",
            "messageUrl":"https://docs.qq.com/sheet/DRkpFRUVITVJsVVpv"
        },
        "at": {
            "isAtAll": "true"
        }
    }
    String_TextMsg = json.dumps(String_TextMsg)
    res = requests.post(url,data=String_TextMsg,headers=HEADERS)
    print(res.links)
if __name__ == "__main__":
    message = "又是一天了！"
    sendmesssage(message)