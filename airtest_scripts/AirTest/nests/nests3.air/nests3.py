# -*- encoding=utf8 -*-
__author__ = "ChenfengWu"
__desc__ = "random"
from airtest.core.api import *
auto_setup(__file__)
sys.path.append(os.path.dirname(os.path.abspath(__file__)).split("AirTest")[0])
from common.Heros import *

init_common = CommonAirTest.InitCommon()
GM, getUserInfo, userAccount, poco = init_common.heros_start()
globals().update(init_common.load_config(__file__))

GM.upgrade_level(35)
GM.upgrade_level(34)
time.sleep(4)

nests_json = HerosMethod.HerosMethod(QA_SCRIPT,"nests").get_all_data()
#阵营类型
race = {1:"城堡",2:"壁垒",3:"墓园",4:"据点",5:"地狱",6:"塔楼",7:"地下城",8:"要塞",9:"元素",10:"港口"}
race_type = init_common.fileTag(__file__).replace("nests","")
# race_type = fileTag(__file__).replace("nests","")#通过文件名获取阵营的类型
for x in race:
    if x == int(race_type):
        race_name = race[x]#阵营名字
GM.add_res("gold",-(getUserInfo.get_gold()))
time.sleep(2)

def goto_chaoxue():#去指定兵种界面
    poco(name="chaoxue").click()
    time.sleep(2)
    menu_list = poco(name="menuNode").offspring("nameLabel")
    if int(race_type) >= 5:
        posA = menu_list[0]
        posB = menu_list[4]
        posB.drag_to(posA,duration=1)
        menu_list = poco(name="menuNode").offspring("nameLabel")
        time.sleep(2)
    for x in menu_list:
        if x.get_text() == race_name:
            x.click()  
            break
            
def find_team(rank_num):#查看当前阵营下的第几个兵营
    for x in nests_json :
        if nests_json[x]["race"] == race_type:
            rank = nests_json[x]["rank"]
            if rank == str(rank_num):
                team = nests_json[x]["team"]
                upgrade = nests_json[x]["upgrade"]
                build = nests_json[x]["build"]
                id_num = x 
                exchange = nests_json[x]["exchange"]
                born_limit = nests_json[x]["born_limit"]
                break
    return team, upgrade ,build ,id_num ,exchange,born_limit

goto_chaoxue()            
#统计当前拥有的兵团id
team_list = []
for x in getUserInfo.get_teams():
    team_list.append(x)
rank_list = []
for x in nests_json:
    if nests_json[x]["race"] == race_type:
        rank_list.append(nests_json[x]["rank"])
            
#验证兵营解锁条件
for num in range(1,len(rank_list) + 1):
    team_id,upgrade_list, build_list ,id_list,exchange_list,born_limit_list = find_team(num)
    posA = poco(name="item_{}".format(num)).focus([0.5,0.5])
    posB = poco(name="item_{}".format(num-1)).focus([0.5,0.5])
    lock_tip = poco(name="item_{}".format(num)).offspring("lockNode").exists()
    build_tip = poco(name="item_{}".format(num)).offspring("buildNode").exists()
    if num >= len(rank_list) / 2:
        posA.drag_to(posB)

    if team_id not in team_list:
        try:
            assert_equal(lock_tip,True,"未拥有对应兵种该兵营未解锁")
            snapshot(msg="兵营未解锁，提示正确")
        except:
            snapshot(msg="兵营未解锁，提示不正确")
            init_common.stop_game() 
        GM.create_team(int(team_id))
        time.sleep(2)
    else:
        try:
            assert_equal(build_tip,True,"兵营拥有对应兵种已解锁")
            snapshot(msg="兵营拥有对应兵种已解锁")
        except:
            snapshot(msg="兵营拥有对应兵种，提示不正确")
            init_common.stop_game() 
CommonUI.CommonUI(poco).close_btn()
goto_chaoxue() 
#--------建造&升级兵营--------------            
for num in range(1,len(rank_list) + 1):
    team_id,upgrade_list ,build_list ,id_list ,exchange_list,born_limit_list= find_team(num)
    posA = poco(name="item_{}".format(num)).focus([0.5, 0.5])
    posB = poco(name="item_{}".format(num-1)).focus([0.5, 0.5])
    build_btn = poco(name="item_{}".format(num)).offspring("buildLabel")
    if num >= len(rank_list) / 2:
        posA.drag_to(posB)
 
    try:
        assert_equal(build_btn.exists(),True,"兵营已解锁，可以建造")
        snapshot(msg="兵营已解锁，可以建造")
    except:
        snapshot(msg="兵营已解锁，不能建造")
        init_common.stop_game() 
    build_btn.click()
    for x in build_list:
        GM.add_res(x[0],x[2] - 1)
    poco(name="buildBtn").click()
    try:
        assert_equal(poco(name="approach1").exists(),True,"创建兵营资源不足提示存在")
        snapshot(msg="创建兵营资源不足提示存在")
    except:
        snapshot(msg="创建兵营资源不足提示不正确")
        init_common.stop_game()     
    CommonUI.CommonUI(poco).close_btn("btn_close")
    for x in build_list:
        GM.add_res(x[0],1)
    poco(name="buildBtn").click()    
    lv = int(poco(name="item_{}".format(num)).offspring("lvLabel").get_text().split(".")[1])
    lv_after = getUserInfo.get_nests()[race_type][id_list]["lvl"]
    upgrade_btn = poco(name="item_{}".format(num)).offspring("upgradeLabel")
    try:
        assert_equal(upgrade_btn.exists(),True,"兵营建造成功")
        assert_equal(lv == lv_after == 1,True,"兵营创建成功后，兵营等级正确")
        assert_equal(getUserInfo.get_gold(),0,"兵营创建成功消耗资源正确")
        snapshot(msg="兵营建造正确")
    except:
        snapshot(msg="兵营建造数据不正确")
        init_common.stop_game() 
    max_lv = len(upgrade_list) +1    
    while lv_after != max_lv:   
        upgrade_btn.click()  
        poco(name="updateBtn").click() 
        try:
            assert_equal(poco(name="approach1").exists(),True,"升级兵营资源不足提示存在")
            snapshot(msg="升级兵营资源不足提示存在")
        except:
            snapshot(msg="升级兵营资源不足提示不正确")
            init_common.stop_game()   
        CommonUI.CommonUI(poco).close_btn("btn_close")  
        for x in upgrade_list[lv_after - 1]:
            GM.add_res(x[0],x[2])    
            time.sleep(2)
        speed_later = poco(name="rRateLabel").get_text().replace("小时/个","")
        later_lv = int(poco(name="rNameLabel").get_text().split(".")[1])   
        poco(name="updateBtn").click()
        lv_now = int(poco(name="item_{}".format(num)).offspring("lvLabel").get_text().split(".")[1])
        lv_after = getUserInfo.get_nests()[race_type][id_list]["lvl"]  
        if lv_after != max_lv:
            upgrade_btn.click() 
            speed_now = poco(name="lRateLabel").get_text().replace("小时/个","")  
            CommonUI.CommonUI(poco).close_btn("closeBtn")
        else:
            speed_now = speed_later
        try:
            assert_equal(lv_now == lv_after == later_lv ,True,"兵营升级成功后，兵营等级正确")
            assert_equal(speed_now == speed_later,True,"兵营升级成功后，生产速率正确")
            assert_equal(getUserInfo.get_gold(),0,"兵营升级成功消耗资源正确")
            snapshot(msg="兵营建造正确")
        except:
            snapshot(msg="兵营建造数据不正确")
            init_common.stop_game()   
    lv_now = int(poco(name="item_{}".format(num)).offspring("lvLabel").get_text().split(".")[1])
    lv_after = getUserInfo.get_nests()[race_type][id_list]["lvl"]   
    try:
        assert_equal(upgrade_btn.exists(),False,"兵营已达满级，升级按钮隐藏")
        assert_equal(lv_now == lv_after == max_lv,True,"兵营升到满级正确")
        snapshot(msg="兵营达到满级正确")
    except:
        snapshot(msg="兵营达到满级数据正确")
        init_common.stop_game()   
    for x in exchange_list:
        GM.add_res(x[0],x[2] - 1)
        time.sleep(2)
        need_nests = x[2]
    poco(name="item_{}".format(num)).offspring("towerIcon").click()
    poco(name="exchangeBtn").click()
    try:
        assert_equal(poco(name="label1").exists(),True,"星银数量不够，不能兑换碎片")
        snapshot(msg="星银数量不够，不能兑换碎片")
    except:
        snapshot(msg="星银数量不够，不能兑换碎片报错")
        init_common.stop_game() 
    temporary = poco(name="label1").parent()#临时处理
    temporary.offspring("closeBtn").click()         
    for x in exchange_list:
        GM.add_res(x[0],1)
        time.sleep(2)
        cost_type = x[0]
        need_nests = x[2]
        have_nests = getUserInfo.get_all_info().get(cost_type)   
    CommonUI.CommonUI(poco).close_btn("closeBtn")   
    poco(name="item_{}".format(num)).offspring("towerIcon").click()
    nests_num = poco(name=("<Label | Tag = -1, Label = '{}/{}'>").format(have_nests,need_nests)).get_text()
    have_count = poco(name="countLabel").get_text()
    frg_num = getUserInfo.get_nests()[race_type][id_list]["frg"] 
    try:
        assert_equal(nests_num,str(have_nests)+"/"+str(need_nests),"拥有星银数和需要数量显示一致")
        snapshot(msg="拥有星银数和需要数量显示一致")
    except:
        snapshot(msg="拥有星银数和需要数量显示不一致")
        init_common.stop_game() 
    poco(name="exchangeBtn").click()
    have_count_later = poco(name="countLabel").get_text()
    nests_num_later = poco(name=("<Label | Tag = -1, Label = '{}/{}'>").format(0,need_nests)).get_text()
    frg_num_later = getUserInfo.get_nests()[race_type][id_list]["frg"]
    try:
        assert_equal(getUserInfo.get_all_info().get(cost_type),0,"消耗星银数正确")
        assert_equal(nests_num_later,"0/"+str(need_nests),"拥有星银数和需要数量显示一致")
        assert_equal(int(have_count_later),int(have_count) + 1,"增加碎片数量正确")
        assert_equal(frg_num - 1,frg_num_later ,"存储量减少正确")
        snapshot(msg="兑换碎片成功后，数据验证正确")
    except:
        snapshot(msg="兑换碎片成功后，数据验证不正确")
        init_common.stop_game() 
    #兑换多个
    for x in exchange_list:
        GM.add_res(x[0],x[2] * frg_num_later)
        time.sleep(2)
    CommonUI.CommonUI(poco).close_btn("closeBtn")   
    poco(name="item_{}".format(num)).offspring("towerIcon").click()    
    poco(name="addTenBtn").click()
    poco(name="exchangeBtn").click()
    suipian_num = poco(name="countLabel").get_text()
    frg_num_last = getUserInfo.get_nests()[race_type][id_list]["frg"]
    try:
        assert_equal(frg_num_last,0,"存储量为0")
        assert_equal(int(suipian_num),1 + frg_num_later,"增加碎片数量正确")
        assert_equal(getUserInfo.get_all_info().get(cost_type),0,"消耗星银数正确")
        snapshot(msg="购买多次碎片数据正确")
    except:
        snapshot(msg="购买多次碎片数据不正确")
        init_common.stop_game() 
    poco(name="exchangeBtn").click()
    suipian_num_last = poco(name="countLabel").get_text()
    try:
        assert_equal(suipian_num_last,suipian_num,"存储量已满，点击兑换无变化")
        snapshot(msg="存储量已满，点击兑换无变化")
    except:
        snapshot(msg="存储量已满，点击兑换报错")
        init_common.stop_game() 
    CommonUI.CommonUI(poco).close_btn("closeBtn") 
init_common.stop_game() 

            





    
    
    
    
    
    
    
