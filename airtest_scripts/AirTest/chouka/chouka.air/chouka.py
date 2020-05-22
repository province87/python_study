# -*- encoding=utf8 -*-
__author__ = "ChenfengWu"
__desc__ = "must"
from airtest.core.api import *
from collections import Counter
import operator
auto_setup(__file__)
sys.path.append(os.path.dirname(os.path.abspath(__file__)).split("AirTest")[0])
from common.Heros import *

init_common = CommonAirTest.InitCommon()
GM, getUserInfo, userAccount, poco = init_common.heros_start()
globals().update(init_common.load_config(__file__))

def get_client_result():  # 获取恭喜获得界面道具
    item_list = poco.freeze()
    item_data = item_list(name="scrollView")
    get_json = HerosMethod.ToolJson(QA_SCRIPT)
    result = {}
    result_item = {}
    result_team = {}
    for x in item_data.offspring("iconColor"):
        num_sort = ((str(x)).split("[")[1]).split("]")[0]
        for y in item_data.offspring("Label"):
            name_sort = ((str(y)).split("[")[1]).split("]")[0]
            if num_sort == name_sort:
                item_name = y.get_text()
                if "限定礼包" in item_name:
                    item_count = int(x.offspring("numLab").get_text())
                    item_tag = str(get_json.noet_bag_name_query(item_name))
                    if item_tag in result_item:
                        result_item[item_tag] += item_count
                    else:
                        result_item[item_tag] = item_count
                else:        
                    if x.offspring("numLab").exists() and x.offspring("runeLab").get_text():
                        rune_lab = int(x.offspring("runeLab").get_text().replace("+",""))
                        item_count = int(x.offspring("numLab").get_text())
                        item_tag = get_json.name_query(item_name,rune_lab)
                        if item_tag in result_item:
                            result_item[item_tag] += item_count
                        else:
                            result_item[item_tag] = item_count
                    elif x.offspring("numLab").exists() and not x.offspring("runeLab").get_text():
                        item_count = int(x.offspring("numLab").get_text())
                        item_tag = get_json.name_query(item_name)
                        if item_tag in result_item:
                            result_item[item_tag] += item_count
                        else:
                            result_item[item_tag] = item_count

                    elif not x.offspring("numLab").exists():
                        item_count = 1
                        team_tag = get_json.team_name_query(item_name)
                        if team_tag in result_team:
                            result_team[team_tag] += item_count
                        else:
                            result_team[team_tag] = item_count
    return result_item,result_team    

def merge(dict1,dict2):#合并道具
    x,y = Counter(dict1), Counter(dict2)
    z = dict(x+y)
    return z

def bag_num():#记录当前背包状态
    bag_dict = {}
    for x in getUserInfo.get_items():
        bag_dict[x] = getUserInfo.get_items()[x]["num"]
    return bag_dict

def interface_num(btname):
    tools_have = int(poco(name="toolLab").get_text())
    tool = int(poco(name=btname).offspring("cost").get_text().split("/")[0])
    tool_cost = int(poco(name=btname).offspring("cost").get_text().split("/")[1])
    return tools_have,tool,tool_cost

def have_lucky(btn_name):
    sum_lucky = int(poco(name="luckyLab").get_text())
    cost_text = poco(name=btn_name).offspring("cost").get_text()
    return sum_lucky,cost_text
    
def num_miss():#道具不足抽卡失败
    try:
        assert_equal(touch_lab,False,"道具不足，抽卡失败")
        snapshot(msg="道具不足，抽卡失败")
    except:
        snapshot(msg="道具不足报错")
        init_common.stop_game() 
        
def have_team():#当前拥有兵团
    team = []
    for x in getUserInfo.get_teams():
        team.append(x)
    return team

def lucky_miss():
    title = poco(name="titleTip").exists()
    try:
        assert_equal(title , True ,"幸运币不足提示正确")
        snapshot(msg="幸运币不足提示正确")
    except:
        snapshot(msg="幸运币不足提示错误")
        init_common.stop_game() 
    poco(name="btn2").click()  
    
def waiting(name):
    while poco(name="name").exists() or not poco(name=name).exists():
        time.sleep(2)
        if poco(name="name").exists():
            poco(name="name").click()
            time.sleep(1)    
        else:
            time.sleep(2)  

def team_contrast(name):
    team_list1 = []
    for x in name:
        team_list1.append(x)
    return team_list1

def single_card(name,exp_name,tool,bag_name,team_befor):
    team_list0 = team_contrast(name)
    sum_team = team_befor + team_list0
    item = merge(tool,exp_name)
    item_dict_last = merge(item,bag_name)
    return item_dict_last,sum_team

setting_json = HerosMethod.HerosMethod(QA_SCRIPT,"setting").get_all_data()
for k,v in setting_json.items():#获取setting表里的相关配置
    try:
        exec(f"{k} = {str(v['value'])}")
    except:
        pass
tools_id = G_DRAWCOST_TOOL_SINGLE[1]
gem_free_arward = str(G_FIRST_DRAW_GEM_FREE_ARWARD[0][0])#钻石抽首次必得
gem_arward = str(G_FIRST_DRAW_GEM_ARWARD[0][0])#花费钻石抽首次必得
GM.upgrade_level(30)
time.sleep(2)
GM.upgrade_level(30)
time.sleep(4)
poco(name="chouka").click((0.5,0.5))
bag = bag_num()

#--------普通抽卡------------
poco(name="toolLayer").click()
touch_lab = poco(name="touchLab").exists()
#普通单次抽卡
send_exp = {str(G_DRAWTOOL_SEND_TEXP[1]):G_DRAWTOOL_SEND_TEXP[2]}
poco(name="buyOneBtn").click()
num_miss()        
GM.send_items(tools_id,1)
time.sleep(2)
team_list_now = have_team()
poco(name="buyOneBtn").click()
waiting("touchLab")
tool_list,team_dict = get_client_result()
team_list2 = have_team()
item_dict,team_list_last = single_card(team_dict,send_exp,tool_list,bag,team_list_now)    
bag_1_time = bag_num()
poco(name="touchLab").click()
tools_have_num ,tool_num , tool_cost_num = interface_num("buyOneCostLayer") 
try:
    assert_equal(operator.eq(bag_1_time,item_dict), True ,"单次普通抽卡结束后，获得物品正确&道具抽卡给怪兽经验正确，前后端数据已验证")
    assert_equal(team_list_last ==  team_list2, True ,"单抽如果获得兵团验证正确")
    assert_equal(bag_1_time.get(tools_id) , None ,"单次普通抽卡消耗道具正确，后端数据已验证")
    assert_equal(tools_have_num == tool_num , True ,"单次普通抽卡消耗道具正确，前端数据已验证")
    assert_equal(tool_cost_num , G_DRAWCOST_TOOL_SINGLE[2] ,"单次普通抽卡消耗道具数量显示正确，前后端已验证")
    snapshot(msg="单次普通抽卡消耗和获得验证成功")
except:
    snapshot(msg="单次普通抽卡消耗和获得验证失败")
    init_common.stop_game() 
#普通十次抽卡
GM.send_items(tools_id,G_DRAWCOST_TOOL_TENTIMES[2] - 1)
time.sleep(2)
send_exp = {str(G_DRAWTOOL_SEND_TEXP[1]):G_DRAWTOOL_SEND_TEXP[2] * 10}
poco(name="buyTenBtn").click()
num_miss()
GM.send_items(tools_id,1)
team_list_now = have_team() 
poco(name="buyTenBtn").click()
waiting("backBtn")
tool_list,team_dict = get_client_result()  
team_list2 = have_team()
item_dict,team_list_last = single_card(team_dict,send_exp,tool_list,bag_1_time,team_list_now)
bag_10_time = bag_num()
time.sleep(2)
poco(name="backBtn").click()
tools_have_num ,tool_num , tool_cost_num = interface_num("buyTenCostLayer") 
try:
    assert_equal(operator.eq(bag_10_time,item_dict), True ,"十次普通抽卡结束后，获得物品正确&道具抽卡给怪兽经验正确，前后端数据已验证")
    assert_equal(team_list_last ==  team_list2, True ,"获得兵团验证正确")
    assert_equal(bag_1_time.get(tools_id) , None ,"十次普通抽卡消耗道具正确，后端数据已验证")
    assert_equal(tools_have_num == tool_num , True ,"十次普通抽卡消耗道具正确，前端数据已验证")
    assert_equal(tool_cost_num , G_DRAWCOST_TOOL_TENTIMES[2] ,"十次普通抽卡消耗道具数量显示正确，前后端已验证")
    snapshot(msg="10次普通抽卡消耗和获得验证成功")
except:
    snapshot(msg="10次普通抽卡消耗和获得验证失败")
    init_common.stop_game() 
#普通100次购买
GM.send_items(tools_id,G_DRAWCOST_TOOL_TENTIMES[2] * 10 - 1)
time.sleep(2)
send_exp = {str(G_DRAWTOOL_SEND_TEXP[1]):G_DRAWTOOL_SEND_TEXP[2] * 100}
poco(name="buy100Btn").click()
num_miss()
GM.send_items(tools_id,1)
team_list_now = have_team() 
poco(name="buy100Btn").click()
waiting("backBtn")
tool_list,team_dict = get_client_result()
team_list2 = have_team()
item_dict,team_list_last = single_card(team_dict,send_exp,tool_list,bag_10_time,team_list_now)
bag_100_time = bag_num()
time.sleep(2)
poco(name="backBtn").click()
tools_have_num ,tool_num , tool_cost_num = interface_num("buy100CostLayer") 
try:
    assert_equal(operator.eq(bag_100_time,item_dict), True ,"100次普通抽卡结束后，获得物品正确&道具抽卡给怪兽经验正确，前后端数据已验证")
    assert_equal(team_list_last ==  team_list2, True ,"获得兵团验证正确")
    assert_equal(bag_100_time.get(tools_id) , None ,"100次普通抽卡消耗道具正确，后端数据已验证")
    assert_equal(tools_have_num == tool_num , True ,"100次普通抽卡消耗道具正确，前端数据已验证")
    assert_equal(tool_cost_num , G_DRAWCOST_TOOL_TENTIMES[2] * 10 ,"100次普通抽卡消耗道具数量显示正确，前后端已验证")
    snapshot(msg="100次普通抽卡消耗和获得验证成功")
except:
    snapshot(msg="100次普通抽卡消耗和获得验证失败")
    init_common.stop_game() 
CommonUI.CommonUI(poco).close_btn("returnBtn")    
#------------钻石抽卡--------------
time.sleep(2)
poco(name="gemLayer").click()
lucky_nums,cost_text_later = have_lucky("buyOneCostLayer")
lucky_id = "luckyCoin"
send_gem_exp = {str(G_DRAWGEM_SEND_TEXP[1]):G_DRAWGEM_SEND_TEXP[2]}
if lucky_nums != 0:
    GM.add_res(lucky_id,-lucky_nums)
    time.sleep(2) 
if cost_text_later == "本次免费":
    team_list_now = have_team() 
    poco(name = "buyOneBtn").click()
    waiting("touchLab")
    tool_list,team_dict =  get_client_result()
    team_list2 = have_team()
    item_dict,team_list_last = single_card(team_dict,send_gem_exp,tool_list,bag_100_time,team_list_now)
    poco(name="touchLab").click()
    lucky_nums,cost_text_later = have_lucky("buyOneCostLayer")    
    bag_1_free_gem = bag_num()
    try:
        assert_equal(operator.eq(bag_1_free_gem,item_dict), True ,"首次免费钻石抽获得道具正确")
        assert_equal(team_list2 == team_list_last, True ,"首次免费钻石抽获得兵团正确")
        assert_equal(gem_free_arward in team_dict  , True ,"首次免费必得兵团正确")
        assert_equal(gem_free_arward in team_list2  , True ,"获得的兵团已增加，后端数据已验证")
        assert_equal(cost_text_later == "本次免费"  , False ,"免费次数消耗后不再免费")
        assert_equal(lucky_nums , 0 ,"有免费次数时不消耗幸运币")
        assert_equal(poco(name="greenText").exists(), True ,"首次付费钻石抽打折显示正确")
        assert_equal(int(poco(name="greenText").get_text()), int(G_DRAWCOST_GEM_SINGLE[2]*float(G_DISCOUNT_FIRST_SINGLE_DRAW)) ,"首次付费钻石抽消耗数量正确")        
        snapshot(msg="首次免费必得兵团正确&消耗正确")
    except:
        snapshot(msg="首次免费必得兵团&消耗错误")
        init_common.stop_game()     
GM.add_res(lucky_id,int(G_DRAWCOST_GEM_SINGLE[2]*float(G_DISCOUNT_FIRST_SINGLE_DRAW)) - 1)
time.sleep(2)
poco(name="buyOneBtn").click()
lucky_miss()  
GM.add_res(lucky_id,1)
time.sleep(2)
team_list_now = have_team()
poco(name="buyOneBtn").click()   
waiting("touchLab")
tool_list,team_dict = get_client_result()
team_list2 = have_team()
item_dict,team_list_last = single_card(team_dict,send_gem_exp,tool_list,bag_1_free_gem,team_list_now)
poco(name="touchLab").click()
lucky_nums,cost_text_later = have_lucky("buyOneCostLayer")        
bag_1_gem = bag_num()
try:
    assert_equal(gem_arward in team_dict  , True ,"首次付费必得兵团正确")
    assert_equal(gem_arward in team_list2  , True ,"获得的兵团已增加，后端数据已验证")
    assert_equal(team_list2 == team_list_last, True ,"首次钻石抽获得兵团正确")
    assert_equal(operator.eq(bag_1_gem,item_dict), True ,"首次付费钻石抽获得道具正确")
    assert_equal(lucky_nums == getUserInfo.get_lucky() == 0, True ,"单次钻石抽消耗幸运币正确，前后端已验证")
    assert_equal(int(cost_text_later) , G_DRAWCOST_GEM_SINGLE[2],"单次钻石抽消耗幸运币界面显示正确")
    snapshot(msg="首次钻石付费抽卡消耗和获得验证成功")
except:
    snapshot(msg="首次钻石付费抽卡消耗和获得验证失败")
    init_common.stop_game()  
#钻石十连
send_gem_tenexp = {str(G_DRAWGEM_SEND_TEXP[1]):G_DRAWGEM_SEND_TEXP[2]*10}
GM.add_res(lucky_id,int(G_DRAWCOST_GEM_TENTIMES[2] * float(G_DISCOUNT_TENTIMES_DRAW))-1)
time.sleep(2)
poco(name="buyTenBtn").click()
lucky_miss()    
GM.add_res(lucky_id,1)
time.sleep(2)
team_list_now = have_team()
poco(name="buyTenBtn").click()  
waiting("backBtn")
tool_list,team_dict = get_client_result()
team_list2 = have_team()
item_dict,team_list_last = single_card(team_dict,send_gem_tenexp,tool_list,bag_1_gem,team_list_now)
poco(name="backBtn").click()
lucky_nums,cost_text_later = have_lucky("buyTenCostLayer")        
bag_10_gem = bag_num()
try:
    assert_equal(operator.eq(bag_10_gem,item_dict), True ,"十连钻石抽获得道具正确")
    assert_equal(team_list2 == team_list_last, True ,"十连钻石抽获得兵团正确")
    assert_equal(lucky_nums == getUserInfo.get_lucky() == 0, True ,"十连钻石抽消耗幸运币正确，前后端已验证")
    assert_equal(int(cost_text_later) , int(G_DRAWCOST_GEM_TENTIMES[2] * float(G_DISCOUNT_TENTIMES_DRAW)),"十连钻石抽消耗幸运币界面显示正确")
    snapshot(msg="十连钻石付费抽卡消耗和获得验证成功")
except:
    snapshot(msg="十连钻石付费抽卡消耗和获得验证失败")
    init_common.stop_game()  
#--------阵营抽卡----------
CommonUI.CommonUI(poco).close_btn("returnBtn") 
poco(name="raceDrawBtn").click()
poco(name="raceLayer").click()
lucky_nums,cost_text_later = have_lucky("buyOneCostLayer")
#阵营单抽
if cost_text_later == "本次免费":
    poco(name = "buyOneBtn").click()
    waiting("backBtn")
    tool_list,team_dict =  get_client_result()
    poco(name="backBtn").click()
    lucky_nums,cost_text_later = have_lucky("buyOneCostLayer")    
    item_dict = merge(tool_list,bag_10_gem)  
    bag_1_free_zhenying = bag_num()
    try:
        assert_equal(operator.eq(bag_1_free_zhenying,item_dict), True ,"首次免费阵营抽获得道具正确")
        assert_equal(cost_text_later == "本次免费"  , False ,"免费次数消耗后不再免费")
        assert_equal(lucky_nums , 0 ,"有免费次数时不消耗幸运币")
        assert_equal(poco(name="raceDiscountLab").exists(), True ,"首次付费阵营抽打折显示正确")
        assert_equal(int(poco(name="raceDiscountLab").get_text()), int(G_DRAWCOST_GEM_SINGLE[2]*float(G_DISCOUNT_FIRST_SINGLE_DRAW)) ,"首次付费阵营抽消耗数量正确")
        snapshot(msg="首次免费必得兵团正确&消耗正确&首次付费阵营抽消耗正确")        
    except:
        snapshot(msg="首次免费阵营抽经获得道具正确")
        init_common.stop_game()  
GM.add_res(lucky_id,int(G_DRAWCOST_GEM_SINGLE[2]*float(G_DISCOUNT_FIRST_SINGLE_DRAW)) - 1)
time.sleep(2)
poco(name="buyOneBtn").click()
lucky_miss()  
GM.add_res(lucky_id,1)
time.sleep(2)
poco(name="buyOneBtn").click()   
waiting("backBtn")
tool_list,team_dict = get_client_result()
poco(name="backBtn").click()
lucky_nums,cost_text_later = have_lucky("buyOneCostLayer")        
item_dict = merge(tool_list,bag_1_free_zhenying)    
bag_1_zhenying = bag_num()
try:
    assert_equal(operator.eq(bag_1_zhenying,item_dict), True ,"首次付费阵营抽获得道具正确")
    assert_equal(lucky_nums == getUserInfo.get_lucky() == 0, True ,"单次阵营抽消耗幸运币正确，前后端已验证")
    assert_equal(int(cost_text_later) , G_DRAWCOST_GEM_SINGLE[2],"单次阵营抽消耗幸运币界面显示正确")
    snapshot(msg="首次阵营付费抽卡消耗和获得验证成功")
except:
    snapshot(msg="首次阵营付费抽卡消耗和获得验证失败")
    init_common.stop_game()   

#阵营十连
GM.add_res(lucky_id,int(G_DRAWCOST_GEM_TENTIMES[2] * float(G_DISCOUNT_TENTIMES_DRAW))-1)
time.sleep(2)
poco(name="buyTenBtn").click()
lucky_miss()    
GM.add_res(lucky_id,1)
time.sleep(2)
poco(name="buyTenBtn").click()  
waiting("backBtn")
tool_list,team_dict = get_client_result()
poco(name="backBtn").click()
lucky_nums,cost_text_later = have_lucky("buyTenCostLayer") 
item_dict = merge(tool_list,bag_1_zhenying)    
bag_10_zhenying = bag_num()
# print(set(bag_10_zhenying.items()) ^ set(item_dict.items()),"!!!!")
try:
    assert_equal(operator.eq(bag_10_zhenying,item_dict), True ,"十连阵营抽获得道具正确")
    assert_equal(lucky_nums == getUserInfo.get_lucky() == 0, True ,"十连阵营抽消耗幸运币正确，前后端已验证")
    assert_equal(int(cost_text_later) , int(G_DRAWCOST_GEM_TENTIMES[2] * float(G_DISCOUNT_TENTIMES_DRAW)),"十连阵营抽消耗幸运币界面显示正确")
    snapshot(msg="十连阵营付费抽卡消耗和获得验证成功")
except:
    snapshot(msg="十连阵营付费抽卡消耗和获得验证失败")
    init_common.stop_game()
init_common.stop_game()








