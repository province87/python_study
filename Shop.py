# -*- encoding=utf8 -*-
__author__ = "ChenfengWu"
__desc__ = "must"
from airtest.core.api import *
auto_setup(__file__)
from poco.drivers.std import StdPoco
sys.path.append(os.path.dirname(os.path.abspath(__file__)).split("AirTest")[0])
from common.CommonMethod import *
from common.Master import *
from collections import Counter
import operator
import random
try:
    globals().update(loadFile("local_config.yaml")["MasterTable"])
except:
    globals().update(loadFile(judgePath(os.path.dirname(os.path.abspath(__file__))))["MasterTable"])

init_common = CommonAirTest.InitCommon()
GM, getUserInfo, userAccount, poco = init_common.master_start()

#提升等级，商店商品增多
GM.setLevel(50)
time.sleep(2)
poco(name="Button_BtnNav1").click([0.5,0.5])
poco(name="Button_BtnNav1").click([0.5,0.5])
poco(name="Button_BtnNav6").click([0.5,0.5])

boxShopList = poco("rootView").offspring("CheckBoxShop")
boxShopList[1].offspring("Text_btnName").click()
#元宝不足时购买物品
gem = int(poco("rootView").offspring("Text_gemText").get_text())   #记录未消耗钱的元宝数量
if gem == 0:
    tempList = poco("rootView").offspring("Panel_ShopItem")
    tempList[0].child("Button_btnBuy").click([0.5,0.5])
    reminder = poco("rootView").offspring("Text_InfoLabel").get_text()
    try:
        assert_equal(reminder, "掌门，当前元宝不足！是否前往充值？", "元宝不足提示存在")
        snapshot(msg="截图显示元宝不足的弹窗")
    except:
        snapshot(msg="报错截图！")
        init_common.stop_game()
    poco("rootView").offspring("Button_btnOnEvent").offspring("Button_tempBtn").click()

GM.sendItem("gem",30000)    
time.sleep(2)
addGem = int(poco("rootView").offspring("Text_gemText").get_text())   #记录增加元宝后，元宝的数量
tempList = poco("rootView").offspring("Panel_ShopItem")
costGem = tempList[0].offspring("Text_Price").get_text()

#次数用尽测试
def getNum():     
    nums = tempList[0].child("Text_BuyRestriction").get_text()   #可以购买的次数
    num = (nums.split("买")[1])
    num1 = int(num.split("次")[0])
    return num1
costNum = getNum()
snapshot(msg="记录购买次数")
tempList = poco("rootView").offspring("Panel_ShopItem")
tempList[0].child("Button_btnBuy").click([0.5,0.5])
buyTimes = int(poco("rootView").offspring("Text_inputLabel").get_text())
while buyTimes != costNum:
    poco("rootView").offspring("Button_btnMoreAdded").click()
    buyTimes = int(poco("rootView").offspring("Text_inputLabel").get_text())
costAllGem = int(poco("rootView").offspring("Text_AllPrice").get_text())
snapshot(msg="记录消耗的元宝数")
poco("rootView").offspring("Button_btnYes").offspring("Button_tempBtn").click()
lastGem = int(poco("rootView").offspring("Text_gemText").get_text())  #记录购买商品后元宝的数量
try:
    assert_equal((addGem - costAllGem), lastGem, "购买物品后消耗元宝成功")
except:
    snapshot(msg="报错截图！")
    init_common.stop_game()
     
tempList = poco("rootView").offspring("Panel_ShopItem")
lastTime = tempList[0].offspring("Text_BuyRestriction").get_text() #记录次数消耗完后的显示 
try:
    assert_equal(lastTime, "已达购买上限", "购买次数消耗成功")
    snapshot(msg="记录达到上限时的显示")
except:
    snapshot(msg="报错截图！")
    init_common.stop_game()
#购买次数用完，点击购买
tempList[0].child("Button_btnBuy").click([0.5,0.5])   
tip = poco("rootView").offspring("Text_label").exists()
try:
    assert_equal(tip, True, "购买次数用尽后点击购买提示存在")
    snapshot(msg="记录购买次数用尽后点击购买弹出的提示")
except:
    snapshot(msg="报错截图！")
    init_common.stop_game()
#购买商店内的商品，购买前清空背包 
GM.clearBag()
time.sleep(2)      
firstGem = int(poco("rootView").offspring("Text_gemText").get_text())     #记录当前元宝数量  
tempList = poco("rootView").offspring("Panel_ShopItem") 
itemName = tempList[1].offspring("Text_ItemName").get_text()     #记录商品名称
itemCost = int(tempList[1].offspring("Text_Price").get_text())        #记录该商品的消耗
if firstGem < itemCost:
    GM.sendItem("gem",itemCost) 
    sleep(2.0)
#购买商品成功后，扣除元宝数量是否正确
tempList[1].child("Button_btnBuy").click([0.5,0.5])
poco("rootView").offspring("Button_btnYes").offspring("Text_btnName").click()
lastestGem = int(poco("rootView").offspring("Text_gemText").get_text())   #购买商品后的元宝数量
try:
    assert_equal(lastestGem, (firstGem - itemCost), "购买物品消耗元宝正确")
    snapshot(msg="记录购买商品后元宝的变化")
except:
    snapshot(msg="报错截图！")
    init_common.stop_game()
#记录背包内增加购买的对应商品
poco(name="Button_BtnNav1").click([0.5,0.5]) 
poco("rootView").offspring("Button_bag").click()
itemList = poco("rootView").offspring("Panel_itemTable")
lastName = itemList[0].offspring("Text_itemName").get_text()
try:
    assert_equal(lastName, itemName, "背包内增加所购买的物品")
    snapshot(msg="记录背包内物品的显示")
except:
    snapshot(msg="报错截图！")
    init_common.stop_game()
finally:
    init_common.stop_game()   
        
        
