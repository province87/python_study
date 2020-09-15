#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : wuyinan02@playcrab.com
# @Desc    :


from airtest.core.api import *
from poco.drivers.std import StdPoco
import requests
import json
import time

class HerosGM:
    """
    poco.agent.c.call("gm", '{"tMethod":"Tools.addRes", "type":"gem", "num":100}')
    poco.agent.c.call("AutoLogin","a1","9241",True,True)强制引导是否关闭，触发引导是否关闭,true关闭，false或者nil开启
    poco.agent.c.call("Logout")
    """

    def __init__(self, poco):
        self.poco = poco
        self.url = "http://123.207.27.151:8008/"

    def wait_time(self,t=2):
        time.sleep(t)


    def login(self, account, skip_must_guide=True, skip_trigger_guide=True):
        """
            account:账号
            skip_must_guide:是否跳过强制新手引导
            skip_trigger_guide:是否跳过触发引导
        """
        self.poco.agent.c.call("AutoLogin", str(account), "9601", skip_must_guide, skip_trigger_guide)

    def logout(self):
        # 退出游戏
        self.poco.agent.c.call("Logout")

# 清空背包
    def clear_bag(self):
        self.poco.agent.c.call("gm", '{"tMethod":"Tools.clearUserData", "type":"4"}')

# 设置玩家等级
    def upgrade_level(self, lv):
        """
            调整玩家等级
            lv:
            等级,填几级升几级,不是升到多少级
        """
        self.poco.agent.c.call("gm", '{{"tMethod":"Tools.upgradeLevel", "level":{}}}'.format(lv))

# 设置玩家VIP等级
    def set_vip_level(self, lv):
        """
            调整玩家等级
            lv:
            等级,填几级升几级,不是升到多少级
        """
        self.poco.agent.c.call("gm", '{{"tMethod":"Tools.setVipLevel", "level":{}}}'.format(lv))

# 增加、减少道具
    def send_items(self, itemID, itemNum):
        """
        添加物品，会进入背包的道具
        itemID:
            添加/减少道具id
        itemNUm：
            添加道具数量，负数为减少
        """
        self.poco.agent.c.call("gm", '{{"tMethod":"Tools.sendItems", "goodsId": {},"goodsNum": {}}}'.format(itemID, itemNum))

# 增加（资源类型配置在static表内）
    def add_res(self, typeID, itemNum):
        """
        添加资源，货币类
        typeID:
            添加资源id
        itemNUm：
            添加资源数量，数量不能为负
        """
        self.poco.agent.c.call("gm", '{{"tMethod":"Tools.addRes", "type":"{}", "num":{}}}'.format(typeID, itemNum))

# 发放兵团
    def create_team(self, teamId):
        """
        发放兵团
        teamId 兵团id
        """
        self.poco.agent.c.call("gm", {"tMethod":"Tools.createTeam", "teamIds":[teamId]})

# 发放英雄
    def send_hero(self, heroId):
        """
        发放英雄
        heroId 英雄id
        """
        self.poco.agent.c.call("gm", {"tMethod":"Tools.sendHero", "heroIds":[heroId]})

# 跳过攻城战，跳过该功能等级上限可从90增加到110
    def siege_to_over(self, rid):
        """
        跳过攻城战
        """
        self.poco.agent.c.call("gm", '{{"tMethod":"Tools.siegeToOver", "rid": {}}}'.format(rid))

# 一键copy玩家数据
    def auto_key_copy(self, rids):
        """
        一键copy玩家数据
        rids 需要复制玩家的rid
        """
        self.poco.agent.c.call("gm", '{{"tMethod":"Tools.autoKeyCopy", "rids": {}}}'.format(rids))

# 根据账号查询玩家基本信息
    def get_user_by_account(self, userAcc):
        """
        根据userAccount查询rid
        userAcc 为需要查看的userAccount
        """
        ridQuery = {
            "mod": "http",
            "method": "Tools.getUserByAccount",
            "__noauth__": 1,
            "pGroup": "aqq",
            "sec": "9601",
            "MAX_FILE_SIZE": 9900000,
            "rid": 0,
            "name": userAcc,
            "uploadFrom": "提交"
        }
        getRid = requests.get(self.url, params=ridQuery)
        return getRid.json()["roles"]["9601"]["rid"]

# 获取玩家json数据
    def get_user_json(self, rid):
        """
        根据rid查询用户信息
        """
        ridQuery = {
            "mod": "http",
            "method": "System.getUserJson",
            "__noauth__": 1,
            "pGroup": "aqq",
            "sec": "9601",
            "MAX_FILE_SIZE": 9900000,
            "rid": rid,
            "uploadFrom": "提交"
        }
        getRid = requests.get(self.url, params=ridQuery)
        return json.loads(getRid.json()["result"])
