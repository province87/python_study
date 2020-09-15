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

#提升vip后，可以购买商品的次数增加
GM.setLevel(50)
time.sleep(2)
poco(name="Button_BtnNav1").click([0.5,0.5])
poco(name="Button_BtnNav6").click([0.5,0.5])
boxShopList = poco("rootView").offspring("CheckBoxShop")
boxShopList[1].offspring("Text_btnName").click()
tempList = poco("rootView").offspring("Panel_ShopItem")
costGem = tempList[0].offspring("Text_Price").get_text()
def getNum():     
    nums = tempList[0].child("Text_BuyRestriction").get_text()   #可以购买的次数
    num = (nums.split("买")[1])
    num1 = int(num.split("次")[0])
    return num1
costNum = getNum()
snapshot(msg="记录提升vip前可以购买的次数")
poco(name="Button_BtnNav1").click([0.5,0.5])
GM.setVipLevel(15)     #提升vip等级
time.sleep(2)
poco(name="Button_BtnNav6").click([0.5,0.5])
boxShopList = poco("rootView").offspring("CheckBoxShop")
boxShopList[1].offspring("Text_btnName").click()
tempList = poco("rootView").offspring("Panel_ShopItem")
costGem1 = tempList[0].offspring("Text_Price").get_text()
getNum();
costNumLast = getNum()
try:
    assert_not_equal(costNumLast, costNum, "提升vip等级后，购买次数增加成功")
    snapshot(msg="截图记录提升vip后购买次数增加")
except:
    snapshot(msg="报错截图！")
    init_common.stop_game()
GM.sendItem("gem",50000)
time.sleep(2)

# 购买不同类型的物品  
money = poco("rootView").offspring("Text_sliverText").get_text()
itemList1 = poco("rootView").offspring("Panel_ShopItem")
itemListLen = len(itemList1)
itemList = []
for x in range(itemListLen - 1):
    itemList.append(itemList1[x])
item = loadFile("{}/tempFolder/{}".format(QA_SCRIPT,"shop/item.json"))
bagItem = []
for x in item:
    itemTag = item[x].get("itemtag")
    bagItem.append(itemTag)
nameList = MasterMethod.ItemJson(QA_SCRIPT)
nameLast = nameList.idQuery(bagItem)
bagList = []
for x in nameLast:
    shopName = nameLast[x].get("name")
    bagList.append(shopName)
snapshot(msg="记录当前商品列表")
for x in itemList:
    itemName = x.offspring("Text_ItemName").get_text()
    if itemName == "十万银两":
        x.offspring("Button_tempBtn").click()
        time.sleep(1)
        poco("rootView").offspring("Button_btnYes").offspring("Button_tempBtn").click()
        moneyLast = poco("rootView").offspring("Text_sliverText").get_text()
        try: 
            assert_not_equal(money, moneyLast, "购买的十万银两增加成功")
        except:
            snapshot(msg="报错截图！")
            init_common.stop_game()
        poco(name="Button_BtnNav1").click([0.5,0.5])
        poco(name="Button_BtnNav6").click([0.5,0.5])
        boxShopList = poco("rootView").offspring("CheckBoxShop")
        boxShopList[1].offspring("Text_btnName").click() 
    if itemName != "十万银两" and itemName != "高级参悟书" and itemName in bagList :        
        GM.clearBag()
        time.sleep(2)        
        x.offspring("Button_tempBtn").click()
        time.sleep(1)
        poco("rootView").offspring("Button_btnYes").offspring("Button_tempBtn").click()
        poco(name="Button_BtnNav1").click([0.5,0.5])    
        poco("rootView").offspring("Button_bag").click()
        itemBagList = poco("rootView").offspring("Panel_itemTable")
        for x in itemBagList:
            lastName = x.offspring("Text_itemName").get_text()
            if lastName == itemName:
                try:
                    assert_equal(lastName, itemName, "背包内增加所购买的物品")
                    snapshot(msg="记录背包内增加已购买的物品")
                except:
                    snapshot(msg="报错截图！")
                    init_common.stop_game()  
        poco(name="Button_BtnNav1").click([0.5,0.5])
        poco(name="Button_BtnNav6").click([0.5,0.5])
        boxShopList = poco("rootView").offspring("CheckBoxShop")
        boxShopList[1].offspring("Text_btnName").click()           
    if itemName == "高级参悟书":
        x.offspring("Button_tempBtn").click()
        time.sleep(1)
        poco("rootView").offspring("Button_btnYes").offspring("Button_tempBtn").click()
        poco(name="Button_BtnNav1").click([0.5,0.5])
        poco("rootView").offspring("Button_mystery").click()
        bookList = poco("rootView").offspring("Text_equipName")  
        for x in bookList:      
            bookName = x.offspring("Text_templateName").get_text()   
            if bookName == itemName:
                try:
                    assert_equal(bookName, itemName, "背包内增加所购买的物品")
                    snapshot(msg="记录高级参悟书是否购买成功")
                except:
                    snapshot(msg="报错截图！")
                    init_common.stop_game() 
        poco(name="Button_BtnNav1").click([0.5,0.5])
        poco(name="Button_BtnNav6").click([0.5,0.5])
        boxShopList = poco("rootView").offspring("CheckBoxShop")
        boxShopList[1].offspring("Text_btnName").click()

#购买不在当前界面的物品    
status = True
while status:
    time.sleep(2)    
    shopList = poco("rootView").offspring("Panel_ShopItem")
    name1 = shopList[-1].offspring("Text_ItemName").get_text()
    if len(shopList) == 9:
        posA = shopList[2].focus('center')     
        posB = shopList[-3].focus('center')
    else:
        posA = shopList[1].focus('center')      
        posB = shopList[-2].focus('center')
    (posB).drag_to(posA,duration=2) 
    shopList = poco("rootView").offspring("Panel_ShopItem")
    name2 = shopList[-1].offspring("Text_ItemName").get_text()  
    if name1 == name2:
        status = False   
shopList[-1].offspring("Button_tempBtn").click()
sleep(1)
poco("rootView").offspring("Button_btnYes").offspring("Button_tempBtn").click()
itemBag = getUserInfo.getBag()
itemTagBag = []
for x in itemBag:
    itemTagBag.append(x)
nameList = MasterMethod.ItemJson(QA_SCRIPT)
nameInBag = nameList.idQuery(itemTagBag)
lastNames = []
for x in nameInBag:
    lastNames.append(nameInBag[x].get("name"))
x = name2 in lastNames
try:
    assert_equal(x, True, "购买的最后一个商品进入背包")
except:
    snapshot(msg="报错截图！")
    init_common.stop_game()
poco(name="Button_BtnNav1").click([0.5,0.5])
poco(name="Button_BtnNav6").click([0.5,0.5])
boxShopList = poco("rootView").offspring("CheckBoxShop")
boxShopList[1].offspring("Text_btnName").click()
#购买商品后验证次数是否被消耗   
tempList = poco("rootView").offspring("Panel_ShopItem")
timesBefore = int(((tempList[0].offspring("Text_BuyRestriction").get_text()).split("买")[1]).split("次")[0])
tempList = poco("rootView").offspring("Panel_ShopItem")
tempList[0].offspring("Button_tempBtn").click()
times = int(poco("rootView").offspring("Text_inputLabel").get_text())
while times != timesBefore:
    poco("rootView").offspring("Button_btnMoreAdded").click()
    times = int(poco("rootView").offspring("Text_inputLabel").get_text())
poco("rootView").offspring("Button_btnYes").offspring("Button_tempBtn").click()
tempList = poco("rootView").offspring("Panel_ShopItem")
timeList = []
for x in tempList:
    timeLast = x.offspring("Text_BuyRestriction").get_text()
    timeList.append(timeLast)
allBuy = "已达购买上限" in timeList
try:
    assert_equal(allBuy, True, "提升vip等级后，购买次数可以消耗")
    snapshot(msg="提升vip等级后，购买次数可以消耗")
except:
    snapshot(msg="报错截图！")
    init_common.stop_game()
finally:
    init_common.stop_game()     