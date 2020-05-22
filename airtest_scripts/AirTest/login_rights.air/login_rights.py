# -*- encoding=utf8 -*-
__author__ = "ChenfengWu"
__desc__ = "stop"
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco_android = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

auto_setup(__file__)
sys.path.append(os.path.dirname(os.path.abspath(__file__)).split("AirTest")[0])

pkg_name = "com.tencent.tmgp.yxwdzzjy"
start_app(pkg_name)
tip_list = ["始终允许","允许","总是允许","确定"]
timeout = 0 
while timeout <= 30:
    for x in tip_list:
        if poco_android(text = x).exists():
            poco_android(text = x).click()
        else:
            time.sleep(1)
            timeout += 1
            print(f"waitting login ready {timeout}")
if timeout > 30:        
    stop_app(pkg_name)


