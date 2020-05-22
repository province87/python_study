#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : wuyinan02@playcrab.com
# @Desc    : 

from common.CommonMethod import *
import os
import csv
import json
import shutil
import sys


def format_key(keystring):
	return keystring.split("$")[0]

def csv2json(filename):
	tmpResult = []
	finalResult = {}
	with open(filename,"r",encoding='GB18030') as f:
		reader = csv.reader(f)

		for index,row in enumerate(reader):
			if index == 0:
				keyList = list(map(format_key,row))
			elif index == 1:
				keyType = row#提取type(程序没有用到，属于策划注释，大部分可能对不上)
			else:
				if index < 5:
					pass#前2-4行注释行，没有用无需导入json
				else:
					tmpDict = {}#转换
					for rownum,value in enumerate(row):#按行提取
						if value != '' and keyList[rownum] != '':#空value，无效key，空key筛选
							if '[' in value:#数组
								try:
									tmpDict[keyList[rownum]] = eval(value.replace("，",","))#筛选中文逗号后尝试用eval统一数据格式
								except:
									tmpValue = str(value.replace("[","").replace("]",""))#特殊处理(012非法Int,int(str)报错处理)，这里无法有效处理多维数组
									tmpDict[keyList[rownum]] = tmpValue.split(",")#还原数组格式
							else:
								if keyType[rownum] == "int":
									try:
										tmpDict[keyList[rownum]] = int(value) #int转换
									except:
										tmpDict[keyList[rownum]] = value
								elif keyType[rownum] == "float":
									try:
										tmpDict[keyList[rownum]] = float(value) #float转换
									except:
									 	tmpDict[keyList[rownum]] = value
								else:
									tmpDict[keyList[rownum]] = value #字符串处理
					if tmpDict != {}:
						tmpResult.append(tmpDict)

	for x in tmpResult:
		tempKey = False
		if x.get("id"):
			tempKey = copy.deepcopy(x["id"])
			del x["id"]
		elif x.get("Id"):
			tempKey = copy.deepcopy(x["Id"])
			del x["Id"]
		elif x.get("tag"):
			tempKey = copy.deepcopy(x["tag"])
			del x["tag"]
		elif x.get("goodsId"):
			tempKey = copy.deepcopy(x["goodsId"])
			del x["goodsId"]
		elif x.get("languageid"):
			tempKey = copy.deepcopy(x["languageid"])
			del x["languageid"]
		elif x.get("awardId"):
			tempKey = copy.deepcopy(x["awardId"])
			del x["awardId"]
		if tempKey != False:
			tempValue = copy.deepcopy(x)
			finalResult[tempKey] = tempValue
	return finalResult


def write2json(path, data):
	with open(path,'w') as jsonFile:
		jsonFile.write(json.dumps(data, indent=4, ensure_ascii=False))


def Convert(config):
	if os.path.exists(config["JsonPath"]):
		shutil.rmtree(config["JsonPath"])
	os.mkdir(config["JsonPath"])
	for root,dirs,files in os.walk(os.path.join(config["configPath"])):
		for x in files:
			# if x[-3:] == "csv" and x[:4] != "lang":#跳过lang表的处理
			if x[-3:] == "csv":
				filename = x.replace("csv","json")
				try:
					jsonData = csv2json(os.path.join(root,x))
					write2json(os.path.join(config["QA_SCRIPT"],"herojson",filename),jsonData)
					print("#### operate: [{}]                      ".format(x))
				except:
					print(f"[Error!!!!] Convert {root}/{x} Error")


