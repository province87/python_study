import json
import requests
import requests
import json

def dingmessage():
# 请求的URL，WebHook地址
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=69145b8437b497ddac69efcd6685f100b51689d32bc7f19eef3111dea39c16f1"
#构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
}
#构建请求数据
    tex = "上班注意安全，不要迟到"
    message ={

        "msgtype": "text",
        "text": {
            "content": tex
        },
        "at": {

            "isAtAll": True
        }

    }
#对请求的数据进行json封装
    message_json = json.dumps(message)
#发送请求
    info = requests.post(url=webhook,data=message_json,headers=header)
#打印返回的结果
    print(info.text)

if __name__=="__main__":
    dingmessage()