#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : wuyinan02@playcrab.com
# @Desc    :

from common.Heros import CommonHerosGM
from poco.drivers.std import StdPoco
from common.CommonMethod import *
import requests
import json


class GetUserInfo:
	def __init__(self,poco,userAccount):
		self.poco = poco
		self.GM = CommonHerosGM.HerosGM(self.poco)
		self.rid = self.GM.get_user_by_account(userAccount)
		self.get_user_info = self.GM.get_user_json(self.rid)

	def refresh_user_info(self):
		self.get_user_info = self.GM.get_user_json(self.rid)
		return self.get_user_info

	def get_all_info(self, refresh=True):
		if refresh:
			return self.refresh_user_info()
		else:
 			return self.get_user_info

	def get_nests(self, refresh=True):#兵营
		if refresh:
			return self.refresh_user_info().get("nests")
		else:
			return self.get_user_info.get("nests")

	def get_gold(self, refresh=True):#金币
		if refresh:
			return self.refresh_user_info().get("gold")
		else:
			return self.get_user_info.get("gold")

	def get_lucky(self, refresh=True):#幸运币
		if refresh:
			return self.refresh_user_info().get("luckyCoin")
		else:
			return self.get_user_info.get("luckyCoin")

	def get_teams(self, refresh=True):#兵团
		if refresh:
			return self.refresh_user_info().get("teams")
		else:
			return self.get_user_info.get("teams")

	def get_items(self, refresh=True):#道具
		if refresh:
			return self.refresh_user_info().get("items")
		else:
			return self.get_user_info.get("items")						