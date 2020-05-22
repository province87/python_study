#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : wuyinan02@playcrab.com
# @Desc    : 

from airtest.core.android.adb import ADB
import copy
import os
import json
import yaml
# import csv
import hashlib
import random
import string
import time
import datetime
import shutil
import logging as lg
import multiprocessing
import requests


def loadFile(path, data_type=1):
#需重写getCsv
	if str(os.path.splitext(path)[-1]) == ".csv":
		if data_type != 1:
			return getCsv(path, "dict")
		else:
			return getCsv(path)
	elif str(os.path.splitext(path)[-1]) == ".yaml":
		with open(path, 'r', encoding='utf-8') as yamlFile:
			return yaml.load(yamlFile)
	elif str(os.path.splitext(path)[-1]) == ".json":
		with open(path, 'r', encoding='utf-8') as jsonFile:
			return json.load(jsonFile)
			# return json.loads(json.dumps(json.load(jsonFile)).replace('\\ufeff',""))
	else:
		return "暂时不支持{}类型".format(os.path.splitext(path)[-1])


def writeJsonFile(filedata, fileName, openType=False):
	if openType != False:
		with open(fileName,openType,encoding='utf-8') as tempFile:
			tempFile.write(json.dumps(filedata, ensure_ascii=False, sort_keys=False, indent=4))
	else:
		with open(fileName,"w",encoding='utf-8') as tempFile:
			tempFile.write(json.dumps(filedata, ensure_ascii=False, sort_keys=False, indent=4))	


# globals().update(loadFile("local_config.yaml")["version_management"])
# globals().update(loadFile("local_config.yaml")["AirTest_Config"])
"""
关闭此处的加载，修改为使用时根据路径加载，这里加载会出现导入模块上的底层逻辑bug
"""
def getCsv(self):
	pass


def getHashCode(filepath, model="hash"):
	with open(filepath, 'rb') as getfile:
		if model == "hash":
			sha1obj = hashlib.sha1()
			sha1obj.update(getfile.read())
			return sha1obj.hexdigest()
		elif model == "md5":
			md5obj = hashlib.md5()
			md5obj.update(getfile.read())
			return md5obj.hexdigest()
		else:
			return "modle error"


def performance(f):
	# global test
	def fn(*args, **kw):
		t_start = time.time()
		r = f(*args, **kw)
		t_end = time.time()
		print('call {}() in {}s'.format(f.__name__,(t_end - t_start)))
		# test.append('call {}() in {}}s'.format(f.__name__,(t_end - t_start)))
		return r
	return fn


def getRandomString():
	strStr = "".join(random.sample(string.ascii_letters,8))
	strNum = str(random.randint(1,100))
	return strStr + strNum


def formatTime(timeStamp,timeType="day"):
	if timeType == "day":
		return time.strftime('%Y-%m-%d',time.localtime(timeStamp))
	elif timeType == "hour":
		return time.strftime('%Y-%m-%d %H:',time.localtime(timeStamp))
	elif timeType == "minute":
		return time.strftime('%Y-%m-%d %H:%M',time.localtime(timeStamp))
	elif timeType == "second":
		return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timeStamp))

def pt(var):
	try:
		len(var)
		print(">>>"*10)
		print("var={},type={},len={}".format(var,type(var),len(var)))
		print("<<<"*10)
	except TypeError as e:
		print(">>>"*10)
		print("var={},type={}".format(var,type(var)))
		print("<<<"*10)


def checkEnvironment():
	pass


def getTime():
	ct = time.time()
	localTime = time.localtime(ct)
	dataHead = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
	dataSecs = int((ct - int(ct)) * 1000)
	return "{}:{}".format(dataHead,dataSecs)


def totleTime(startTime,endTime):
	formatTimeStr = "%Y-%m-%d %H:%M:%S"
	start = datetime.datetime.strptime(time.strftime(formatTimeStr, time.localtime(startTime)),formatTimeStr)
	end = datetime.datetime.strptime(time.strftime(formatTimeStr, time.localtime(endTime)),formatTimeStr)
	return end - start


def randomChineseName(numLen=5):
	randomName = ""
	for x in range(numLen):
		val = random.randint(0x4e00, 0x9fbf)
		randomName += chr(val)
	return randomName
	

def updateReports(csvPath, fileData, projectName): # 更新测试报告
    dataList = [["Date", "Project", "CreatTime", "Reports"]]
    if os.path.exists("{}/index.html".format(csvPath)):
        os.remove("{}/index.html".format(csvPath))
    if not os.path.exists("{}/index.csv".format(csvPath)):
        with open("{}/index.csv".format(csvPath), "w", newline='', encoding='utf_8_sig') as csvFile:
            csv_write = csv.writer(csvFile, dialect='excel')
            for x in dataList:
                csv_write.writerow(x)

    with open("{}/index.csv".format(csvPath), "a", encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([fileData, projectName, getTime(), '<a href="{}/index.html">查看结果</a>'.format(fileData)])
    os.system("csvtotable {}/index.csv {}/index.html".format(csvPath, csvPath))


def mkFolder(path, creat=True): # 创建唯一报告目录
	indexNum = 1
	baseName = formatTime(time.time(), "day")
	folder = "{}-{}".format(baseName,indexNum)
	while os.path.exists(os.path.join(path,folder)):
		indexNum += 1
		folder = "{}-{}".format(baseName,indexNum)
	folder = "{}-{}".format(baseName,indexNum)

	if creat:
		os.mkdir(os.path.join(path,folder))
	return os.path.join(path,folder)


class getCase:
	def __init__(self):
		"""
		写方法没有加进程锁，写的方法加进程锁的话在目前逻辑下会导致逻辑，
		读取的用例与设备因为读速度大于写速度，会导致读取同一设备与用例
		暂时取消写的进程锁，讲写方法放入调用方法进程锁内，有小概率会导致调用写方法时死锁
		这个类的方法全部是由外面拿进来的
		"""
		self.mlock = multiprocessing.Lock()


	def getDevices(self):
		self.mlock.acquire()
		tempDevices = loadFile("devices.json")
		if len(tempDevices) <= 0:
			print("please waitting...")
			self.mlock.release()
			return False
		else:
			for x in tempDevices:
				tempKeys = x
				devicesID = {tempKeys:tempDevices[x]}
				break
			del tempDevices[tempKeys]
			self.writeJson(tempDevices, "devices.json")
			self.mlock.release()
			return devicesID


	def getTestCase(self,allCase=False):
		self.mlock.acquire()
		testCaseList = []
		caseData = loadFile("tempTestCase.json")
		if not allCase:
			if len(caseData) > 0:
				for x in caseData:
					case = random.sample(caseData,1)
					break
				executeCase = case[0]
				caseData.remove(case[0])
			else:
				executeCase = []
			self.writeJson(caseData, "tempTestCase.json")	
			self.mlock.release()
			return executeCase
		else:
			for x in caseData:
				testCaseList.append(x["scriptName"] + ".air")
			self.mlock.release()
			return testCaseList	


	def writeJson(self,filedata, fileName, openType=False):
		# self.mlock.acquire()
		if openType != False:
			with open(fileName,openType,encoding='utf-8') as tempFile:
				tempFile.write(json.dumps(filedata, ensure_ascii=False, sort_keys=False, indent=4))
		else:
			with open(fileName,"w",encoding='utf-8') as tempFile:
				tempFile.write(json.dumps(filedata, ensure_ascii=False, sort_keys=False, indent=4))
		# self.mlock.release()


	def modifyDevicesJson(self,devicesList):
		self.mlock.acquire()
		getDevicesList = loadFile("devices.json")
		newDict = copy.deepcopy(getDevicesList)
		for x in devicesList:
			for key,value in getDevicesList.items():
				if x == value:
					del newDict[key]
					self.writeJson(newDict,"devices.json")
					self.mlock.release()
					break
				else:
					self.mlock.release()


	def creatDevicesJson(self):
		self.mlock.acquire()
		devicesList = ADB().devices()
		devicesDict = {}
		for x in range(len(devicesList)):
			devicesDict["devices" + str(x)] = devicesList[x][0]
		self.writeJson(devicesDict, "devices.json")
		self.mlock.release()


	def creatTestCase(self,filePath):
		self.mlock.acquire()
		tempList = []
		testCase = loadFile(filePath)
		for x in testCase:
			if x["isRun"]:
				tempList.append(x)
		self.writeJson(tempList, "tempTestCase.json")
		self.mlock.release()
		return tempList


def getWalleuiInfo(project, jobID):
	if project != "war":
		info = requests.get("http://walleui.{}.playcrab-inc.com/updatepackage/getinfo?game={}&job_id={}".format(project,project,jobID))
	else:
		info = requests.get("http://walleui.playcrab-inc.com:8000/updatepackage/getinfo?game=war&job_id={}".format(jobID))
	jsonInfo = eval(str(info.text))
	return jsonInfo["modules_tag"]


def copyFile(src,dct):
	if os.path.exists(dct):
		shutil.rmtree(dct)
	newPath = dct.replace("/tempFolder","")
	# with open('{}/status.json'.format(newPath),"w",encoding='utf-8') as tempFile:
	# 	tempFile.write(json.dumps('\{"a":1\}', ensure_ascii=False, sort_keys=False, indent=4))
	shutil.copytree(src, dct, symlinks=True, ignore=shutil.ignore_patterns('*.lua'))


def judgePath(airPath):
	return airPath.split("AirTest")[0] + "local_config.yaml"

def getChineseNumber(num):
	mapping = ('零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十','十一', '十二', '十三', '十四', '十五', '十六', '十七','十八', '十九')
	lenNumber = ('', '十', '百', '千',)
	maxNumber = 10 ** 4
	assert(0 <= num and num < maxNumber)
	if num < 20:
		numChinese = "第{}章".format(mapping[num])
		print(numChinese)
	else:
		tempList = []
		while num >= 10:
			tempList.append(num % 10)
			num = num / 10
		tempList.append(num)
		tempVar = len(tempList)  # 位数
		result = ''

		for index, var in enumerate(tempList):
			var = int(var)
			if var != 0:
				result += lenNumber[index] + mapping[var]
			elif var == 0 and index == 1 and tempList[index] != 0:
				result += mapping[var]

		numChinese = "第{}章".format(result[::-1])
		print(numChinese)
	return "\n".join(numChinese)


def fileTag(filePath):
	filePath, tmpFileName = os.path.split(filePath)
	targetTag, extension = os.path.splitext(tmpFileName)
	return targetTag


def getFileName(filePath):
	if ".air" in filePath.split("AirTest/")[-1].split("/")[0]:
		return ""
	else:
		return filePath.split("AirTest/")[-1].split("/")[0]

def handleLog(path):
	timeList = []
	result = True
	with open("{}/log.txt".format(path)) as logfile:
		for line in logfile.readlines():
			test = json.loads(line)
			# print(test,type(test))
			timeList.append(test["time"])

			if "traceback" in test["data"]:
				result = False
				break
	times = totleTime(min(timeList),max(timeList))
	return {"times":str(times),"result":result}


	