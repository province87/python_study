#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : wuyinan02@playcrab.com
# @Desc    :

from airtest.core.api import *
from poco.drivers.std import StdPoco
from common.Heros import CommonHerosGM
from common.Heros import GetUserInfo
from common.retry import *
from common.CommonMethod import *
import string
import random
import time
import os


class InitCommon:
	def __init__(self,reopen=True):
		"""
		reopen:bool 是否重新打开游戏客户端，默认打开
		"""
		self.__pkgName__ = "com.tencent.tmgp.yxwdzzjy"
		self.__pkgList__ = ["com.playcrab.dazhangmen2.pre"]
		if reopen:
			self.start_game()
			try:
				self.poco = self.start_poco()
			except:
				log("poco = StdPoco() Error!!!!")
				snapshot(msg="实例化失败截图")
				self.stop_game()
			self.GM = self.heros_gm()
		self.__userAccount__ = None

	def start_game(self):
		self.stop_game()
		start_app(self.__pkgName__)
		# time.sleep(15)#这里将来改成动态等待

	def stop_game(self):
		for x in self.__pkgList__:
			stop_app(x)
		stop_app(self.__pkgName__)


	def get_random_string(self):
		strStr = "".join(random.sample(string.ascii_letters,8))
		strNum = str(random.randint(1,100))
		return strStr + strNum

	@retry(tries=3,delay=2)
	def start_poco(self, debug=False):
		"""
		调试时不需要登录又需要重新实例poco时可单独调用使用
		"""
		if not debug:
			time.sleep(15)
		init_poco = StdPoco()
		init_poco.use_render_resolution()
		return init_poco

	def ready_for_login(self):
		__timeout__ = 0
		while not self.poco(name="okBtn1",text="登录").exists() and __timeout__ <= 20:
			time.sleep(1)
			__timeout__ += 1
			print(f"waitting login ready {__timeout__}")
		if __timeout__ > 20:
			snapshot(msg="login ready failed")
			self.stop_game()
			return False
		else:
			print("login ready done")
			return True

	def login(self):
		__timeout__ = 0
		while not self.poco(name="boxIcon",type="ImageView").exists() and __timeout__ <= 40:
			time.sleep(1)
			__timeout__ += 1
			print(f"waitting login ok {__timeout__}")

		if __timeout__ > 40:
			snapshot(msg="login failed")
			self.stop_game()
		else:
			print("login done")
		time.sleep(5)

	def heros_start(self,account=None,debug=False):
		"""
		账号不为空则视为调试模式
		"""
		if account != None:
			self.__userAccount__ = account
			# 调试模式流程中没有实例化的地方，所以加在了这里,掌门2注销后会释放sdk脚本重新加载，时间不确定，5秒不稳定
			try:
				self.poco = self.start_poco(debug)
			except:
				log("poco = StdPoco() Error!!!!")
				snapshot(msg="实例化失败截图")
				self.stop_game()
			self.GM = self.heros_gm()
			if not debug:
				self.GM.login(self.__userAccount__)
				self.login()
			print("调试实例化")
		else:
			self.__userAccount__ = self.get_random_string()
			print("全流程登录")
			if self.ready_for_login():
				self.GM.login(self.__userAccount__)
				self.login()

		log(f"本次测试账号{self.__userAccount__}")
		Get_User_Info = GetUserInfo.GetUserInfo(self.poco ,self.__userAccount__)

		return self.GM, Get_User_Info, self.__userAccount__, self.poco

	def get_account(self):
		return self.__userAccount__

	def heros_gm(self):
		gm = CommonHerosGM.HerosGM(self.poco)
		return gm

	def close_permission(self):
		pass

	def load_config(self,file_abs_path):
		try:
			config = loadFile("local_config.yaml")["HerosInfo"]
		except:
			config = loadFile(judgePath(os.path.dirname(os.path.abspath(file_abs_path))))["HerosInfo"]
		return config

	def fileTag(self,filePath):
		filePath, tmpFileName = os.path.split(filePath)
		targetTag, extension = os.path.splitext(tmpFileName)
		return targetTag
