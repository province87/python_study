# -*- encoding=utf8 -*-
__author__ = "ChenfengWu"
__desc__ = "must"
from airtest.core.api import *
import operator
auto_setup(__file__)
sys.path.append(os.path.dirname(os.path.abspath(__file__)).split("AirTest")[0])
from common.Heros import *

init_common = CommonAirTest.InitCommon()
GM, getUserInfo, userAccount, poco = init_common.heros_start()
globals().update(init_common.load_config(__file__))

GM.upgrade_level(35)
time.sleep(2)
GM.upgrade_level(34)
time.sleep(3)
#配置表
ability_json = HerosMethod.HerosMethod(QA_SCRIPT,"ability").get_all_data()
ability_effect_json = HerosMethod.HerosMethod(QA_SCRIPT,"abilityEffect").get_all_data()
peerage_json = HerosMethod.HerosMethod(QA_SCRIPT,"peerage").get_all_data()
cost_type = "310001" #激活特权需要的道具
#刷新界面
poco(name="bagBtn").click()
CommonUI.CommonUI(poco).close_btn("closeBtn")

poco(name="privilegeBtn").click()
while poco(name="awardLab").exists():
    CommonUI.CommonUI(poco).close_btn("closeBtn")
#扣除初始默认的特权币    
ability_exp = getUserInfo.get_items().get(cost_type)["num"]
GM.send_items(cost_type,-ability_exp)
time.sleep(2)   

for idnum in range(0,len(peerage_json)):
    while poco(name="mc1").offspring("bitmap").exists():
        name = poco(name="title2").offspring("name").get_text()
        poco(name="mc1").offspring("bitmap").click()
        old_name = poco(name="oldName").get_text()
        new_name = poco(name="newName").get_text()
        while not poco(name="tishi").exists():
            time.sleep(2)
        poco(name="tishi").click() 
        name_later = poco(name="title2").offspring("name").get_text()
        try:
            assert_equal(name == old_name, True ,"特权名称显示正确")
            assert_equal(new_name ==  name_later, True ,"特权晋升成功后，名称显示正确")
            snapshot(msg="特权名称更新正确")
        except:
            snapshot(msg="特权名称更新不正确")
            init_common.stop_game() 
    #当前特权等级
    peerage_lv = getUserInfo.get_all_info().get("privileges")["peerage"]
    for x in peerage_json:
        if int(x) == peerage_lv:
            effect_list = peerage_json[x]["effectId"]
            condition_list = peerage_json[x]["condition"]
            break
    name = poco(name="name").get_text()
    effect_dict = dict(map(lambda x,y:[x,y],effect_list,condition_list))
    detail_list = poco(name="tableViewBg").offspring("detailCell")
    for effect ,detail in zip(effect_dict , detail_list ):
        for ab in ability_effect_json:
            if effect == int(ab):
                cost_num = ability_effect_json[ab]["cost"]
                ability_id = effect_dict[effect]
                level_max = ability_json[str(ability_id)]["level"]
                GM.send_items(cost_type,cost_num[0] - 1)
                time.sleep(2)    
                detail.offspring("upgrade").click()
                old_Lv = int(poco(name="oldAbilityLevel").get_text().replace("Lv.",""))
                poco(name="burst").click()
                old_Lv_later = int(poco(name="oldAbilityLevel").get_text().replace("Lv.",""))
                try:
                    assert_equal(old_Lv,old_Lv_later,"特权币不足，升级失败")
                    snapshot(msg="特权币不足，升级失败")
                except:
                    snapshot(msg="特权币不足，升级失败报错")
                    init_common.stop_game() 
                GM.send_items(cost_type,1) 
                time.sleep(2)
                poco(name="burst").click()
                lv_now = int(poco(name="oldAbilityLevel").get_text().replace("Lv.",""))
                CommonUI.CommonUI(poco).close_btn("closeBtn")
                level_now = int((detail.offspring("level").get_text().split("/")[0]).split(".")[1])
                level_after = int((detail.offspring("level").get_text().split("/")[1]).split(".")[1])
                try:
                    assert_equal(lv_now == old_Lv_later + 1 == level_now, True ,"特权升级成功,数据已验证")
                    assert_equal(getUserInfo.get_items().get(cost_type) , None ,"特权升级成功消耗特权币数量正确")
                    snapshot(msg="特权升级成功，数据验证正确")
                except:
                    snapshot(msg="特权升级成功，数据验证不正确")
                    init_common.stop_game()  
                while level_now != int(level_max):
                    detail.offspring("upgrade").click()
                    parent = poco(name="effectBg").parent()
                    GM.send_items(cost_type,cost_num[level_now] * (int(level_max) - level_now) )
                    time.sleep(2)                     
                    while not parent.offspring("maxLevel").exists():
                        poco(name="burst").click()
                    lv_now = int(poco(name="oldAbilityLevel").get_text().replace("Lv.",""))
                    CommonUI.CommonUI(poco).close_btn("closeBtn")
                    level_now = int((detail.offspring("level").get_text().split("/")[0]).split(".")[1])
                    level_after = int((detail.offspring("level").get_text().split("/")[1]).split(".")[1])
                try:
                    assert_equal(level_now == int(level_max) == level_after == lv_now, True ,"特权升到满级成功数据已验证")
                    assert_equal(getUserInfo.get_items().get(cost_type) , None ,"特权升级成功消耗特权币数量正确")
                    assert_equal(poco(name="maxLevel").exists() , True ,"已满级提示存在")
                    snapshot(msg="特权满级，数据验证正确")
                except:
                    snapshot(msg="特权满级，数据验证不正确")
                    init_common.stop_game()  
#全部特权升至满级后验证后端属性
ability_sum_list = getUserInfo.get_all_info().get("privileges")["abilityList"]
id_list = []
id_level_list = []
ability_dict = {}
for x in ability_json:
    id_list.append(ability_json[x]["effectId"])
    id_level_list.append(int(ability_json[x]["level"]))
for x in range(0,len(id_list)):
    if id_list[x] in ability_dict:
        ability_dict[id_list[x]] += [id_level_list[x]]
    else:
        ability_dict[id_list[x]] = [id_level_list[x]]
for x in ability_dict:
    ability_dict[x] = sum(ability_dict[x])
try:
    assert_equal(operator.eq(ability_sum_list,ability_dict), True ,"特权等级全部升满后，前后端数据正确（后端获取特权id和对应等级与读取配置表计算出来的特权id和对应等级相等")
    snapshot(msg="特权满级，后端等级验证正确")
except:
    snapshot(msg="特权满级，后端等级验证不正确")
    init_common.stop_game()  
#领取每日奖励
gold_num_before = getUserInfo.get_gold()
poco(name="lingqu").offspring("bitmap").click()
name_tip = poco(name="maxLayer").offspring("name").get_text()
gift_num = int(poco(name="numLab").get_text().replace("w", ""))
wages_num = peerage_json[str(len(peerage_json))]["wages"][0][2]
if "w" in poco(name="numLab").get_text():
    gold_num = gift_num * 10000
else:
    gold_num = int(poco(name="numLab"))
poco(text="领取").click()
time.sleep(4)
gold_num_later = getUserInfo.get_gold()
try:
    assert_equal(gold_num_before + gold_num == gold_num_later == wages_num + gold_num_before , True ,"领取每日奖励计算正确")
    snapshot(msg="领取每日奖励计算正确")
except:
    snapshot(msg="领取每日奖励计算不正确")
finally:
    init_common.stop_game() 
   
