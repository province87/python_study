# -*- encoding=utf8 -*-
__author__ = "liusheng"
from airtest.core.api import *
auto_setup(__file__)
from poco.drivers.std import StdPoco
#输入账号,并登录游戏
def login(account):
#实例化一次poco,一用全局初始化就报10053错，很是头疼
    poco = StdPoco()
    if poco(text="登录").exists():
        poco("acountLabel").set_text(account)
        poco(text="登录").click()
        sleep(2)
#调用公告处理函数
        notice()
    else:
        log("登录界面加载失败")
        stop_app("com.tencent.tmgp.yxwdzzjy")
#游戏公告处理，如果有公告关闭所有公告，如果没有公告不做处理
def notice():
#实例化一次poco,一用全局初始化就报10053错，很是头疼
    poco = StdPoco()
    while True:
        try:
            poco(text="游戏公告").wait_for_appearance(timeout=1.5)
            poco("closeBtn",text="确定").click()
            sleep(2)
        except:
            log("没有公告真好！")
            break
#调用登录backend函数
    in_backend()
#登录backend
def in_backend():
    #实例化一次poco,一用全局初始化就报10053错，很是头疼
    poco = StdPoco()
    poco("loginBtn").click()
    sleep(20)
#调用拍脸处理函数
    popup()
#登录游戏后是否有拍脸，如果有拍脸关闭，没有pass
def popup():
    #实例化一次poco,一用全局初始化就报10053错，很是头疼
    poco = StdPoco()
    while True:
        try:
            poco("<Node | Tag = -1").chhild("<Layer | Tag = -1>").offspring("closeBtn").wait(timeout=1.5).click()
        except:
            log("真好没有拍脸，什么也不用干！")
            break
#初始化启动游戏,如果当前调试代码不需要重新登录，把传给函数的值为True
def restart_game(debug,name):
#实例化一次poco,一用全局初始化就报10053错，很是头疼
    poco = StdPoco()
    if poco("<Scene | tag = -1>").exists() and debug==True:
        pass
    else:
        stop_app("com.tencent.tmgp.yxwdzzjy")
        sleep(5)
        start_app("com.tencent.tmgp.yxwdzzjy")
        sleep(18)
#调用登录函数，并接收账号值
        login(name)
#启动游戏函数调用,debug值为True时不重启；值为False时重启并且用name的值为账号登录游戏
restart_game(debug=False,name=12345678
