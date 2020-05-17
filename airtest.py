# -*- encoding=utf8 -*-
__author__ = "Administrator"
from airtest.core.api import *

auto_setup(__file__,devices=["Android://localhost:5037/GWY0217405000331"],logdir=r"C:\Users\Administrator\Desktop\logs\")
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
# poco("com.huawei.intelligent:id/weather_icon").swipe([-0.1,0.08])
# 向左滑动
# poco("com.huawei.intelligent:id/view_smartcare").focus([1,0.5]).swipe([-0.5,0],duration=1)
# 向右滑动
# poco("com.huawei.intelligent:id/view_smartcare").swipe([1,0],duration=1)
# 向上滑动
# 方法1
# poco("com.huawei.intelligent:id/view_smartcare").swipe([0,-1],duration=1)
# 方法2
# poco("com.huawei.intelligent:id/view_smartcare").swipe('up',duration=1)
# 向下滑动
# 方法1
# poco("com.huawei.intelligent:id/view_smartcare").swipe([0,1],duration=1)
# 方法2
# poco("com.huawei.intelligent:id/view_smartcare").swipe("down",duration=1)
# 向右上45度角滑动
# poco("com.huawei.intelligent:id/view_smartcare").swipe([0.5,-0.5],duration=1)
# # snapshot(width=720)
# # snapshot(filename=r"F:\AirtestIDE_2020-01-21_py3_win64\airtest_scripts\scripts_logs\swipe_test.jpg",width=80,high=100,msg="滑动成功")
# snapshot(filename=r"F:\AirtestIDE_2020-01-21_py3_win64\airtest_scripts\scripts_logs\swipe_test.jpg",msg="滑动成功")
# poco("com.huawei.intelligent:id/weather_icon",type="android.widget.ImageView").swipe([0,1],duration=2)
# poco("com.huawei.intelligent:id/hiboard_main_layout").offspring("com.huawei.intelligent:id/dragGridView").child("android.widget.RelativeLayout")[3].offspring("com.huawei.intelligent:id/item_image").swipe([-1,0],duration=1)
# snapshot(msg="swipe to finish")
select_input_phone_number=poco("com.huawei.intelligent:id/hiboard_main_layout").offspring("com.huawei.intelligent:id/expressguide_card_message",text="绑定手机号码，及时获取快递动态。")
# print("看下这个值",select_input_phone_number.wait(timeout=5))
select_input_phone_number.click()
#先用poco获取text="手机号"ui元素对像的name属性
first=poco(text="手机号").get_name()
#拿获取到的名字属性和实际名字属性比较，不能直接拿取出的控件去比较
assert_equal("com.huawei.intelligent:id/phone_number",first,"是否出现输入手机号")
poco("com.huawei.intelligent:id/phone_number",text="手机号").set_text("1551")
keyevent("BACK")
keyevent("BACK")
poco("com.huawei.intelligent:id/hiboard_main_layout").offspring("com.huawei.intelligent:id/search_edit_text").click()
poco("com.huawei.search:id/search_edittext")
text("照相机")
sleep(1)
poco(text="取消").click()
sleep(1)
keyevent("back")
keyevent("back")
sames = poco("com.huawei.intelligent:id/hiboard_main_layout").offspring("android.widget.RelativeLayout").child(
    "com.huawei.intelligent:id/dragGridView").child("android.widget.RelativeLayout")
c = 1
for same in sames:
    print("第:%d次对像路径：%s" % (c, same))
    c += 1
    item_text = same.offspring("com.huawei.intelligent:id/item_text").get_text()
    print("列表中对像有：", item_text)
    if item_text == "换电池":
        print("列表中存在")
        same.offspring("com.huawei.intelligent:id/item_text").swipe([-1, 0], duration=1)
        try:
            assert_1 = poco(text="学生模式").get_text()
            assert_equal("学生模式", assert_1, "是否滑东成功")
            city_dirc = {}
            tianqi_dirc = {}
            # 取出当前时间
            dirc_1 = poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child(
                "com.huawei.android.totemweather:id/include_dual_single_city2")
            dirc_2 = poco("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child(
                "com.huawei.android.totemweather:id/include_dual_single_city1")
            city_name = dirc_1.offspring("com.huawei.android.totemweather:id/widget_city_name").get_text()
            print("城市名字", city_name)
            time_hour = dirc_1.offspring("com.huawei.android.totemweather:id/widget_time_hour").get_text()
            print("小时：", time_hour)
            time_minute = dirc_1.offspring("com.huawei.android.totemweather:id/widget_time_minute").get_text()
            print("分钟：", time_minute)
            time_date = dirc_1.offspring("com.huawei.android.totemweather:id/widget_city_date").get_text()
            print("日期：", time_date)
            print("==============下面是第二个城市===================")
            city_name2 = dirc_2.offspring("com.huawei.android.totemweather:id/widget_city_name").get_text()
            print("城市名字", city_name2)
            time_hour2 = dirc_2.offspring("com.huawei.android.totemweather:id/widget_time_hour").get_text()
            print("小时：", time_hour2)
            time_minute2 = dirc_2.offspring("com.huawei.android.totemweather:id/widget_time_minute").get_text()
            print("分钟：", time_minute2)
            time_date2 = dirc_2.offspring("com.huawei.android.totemweather:id/widget_city_date").get_text()
            print("日期：", time_date2)
            smallicon = dirc_1.offspring(
                "com.huawei.android.totemweather:id/widget_currentweather_smallicon").attr("desc")
            print("天气:", smallicon)
            wendu2 = dirc_2.offspring("com.huawei.android.totemweather:id/widget_current_temperature").get_text()
            print("温度：", wendu2)
            tianqi_dirc["日期"] = time_date
            tianqi_dirc["时间"] = time_minute
            tianqi_dirc["温度"] = 31
            city_dirc["太原"] = tianqi_dirc
            print(city_dirc)

        except Exception as err:
            print("断言失败：", err)
        break
