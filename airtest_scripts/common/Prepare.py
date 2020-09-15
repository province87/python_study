#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : wuyinan02@playcrab.com
# @Desc    : 

from common.CommonMethod import *

from airtest.core.android.adb import ADB
import os
import requests
import subprocess
import urllib

class PrepareAirtest:
    def __init__(self,yamlConfig,version_id=False):
        self.yaml = yamlConfig
        self.projectName = self.yaml["ProjectName"]
        if self.projectName != "war":
            urlBase = "http://walleui.master.playcrab-inc.com/version/getmodule?game="
        else:
            urlBase = "http://walleui.playcrab-inc.com:8000/version/getmodule?game="

        if self.yaml["getType"]["clusterPrefix"] and not version_id:
            self.queryType = "cluster_prefix"
            self.value = self.yaml["getType"]["clusterPrefix"]

        else: 
            self.queryType = "version_id"
            if version_id:
                print("指定versionid")
                self.value = str(version_id)
            else:
                self.value = self.yaml["getType"]["version_id"]

        if self.yaml["getType"]["clusterPrefix"] and self.yaml["getType"]["version_id"]:
            self.queryType = "cluster_prefix"
            self.value = self.yaml["getType"]["clusterPrefix"]

        self.url = "{}{}&{}={}".format(urlBase,self.projectName,self.queryType,self.value)
        print(self.url)

        
    def getWalleuiInfo(self):
        info = requests.get(self.url)
        jsonInfo = eval(str(info.text))
        return jsonInfo

    def getNewVersion(self):
        walleuiInfo = self.getWalleuiInfo()
        apkPath = ""
        if walleuiInfo["result"] == "success":
            apkVersion = walleuiInfo["version_id"]
            if os.path.exists("{}/{}.apk".format(self.yaml["APKPath"],"{}-{}".format(self.projectName,apkVersion))):
                apkPath = "{}/{}.apk".format(self.yaml["APKPath"],"{}-{}".format(self.projectName,apkVersion))
            for x in walleuiInfo["data"]:
                if x["module"]["name"] == "config" and x["module"]["repo_type"] == "SVN":
                    svnVersion = x["tag"]
                    break
            return {"apkVersion":apkVersion,"svnVersion":svnVersion,"apkPath":apkPath}
        else:
            return {}
# print(getNewVersion(test["ProjectName"],clusterPrefix=test["getType"]["clusterPrefix"],version_id=test["getType"]["version_id"]))
    def svnUpdate(self):
        if self.yaml["checkoutSVN"]:
            svnVersion = self.getNewVersion()["svnVersion"]
            cmd = subprocess.Popen("svn revert -R .", shell=True, cwd=self.yaml["configPath"])
            status = cmd.wait() #等待子进程结束
            cmd = subprocess.Popen("svn update -r {}".format(svnVersion), shell=True, cwd=self.yaml["configPath"])
            status = cmd.wait()
            return True
        else:
            return False


    def tool(self):
        if self.projectName == "master":
            if self.svnUpdate() and self.yaml["mtool"]:
                cmd = subprocess.Popen("mtl cfg -auto autotest", shell=True)
                status = cmd.wait() #等待子进程结束
                copyFile(self.yaml["JsonPath"],"{}/tempFolder".format(self.yaml["QA_SCRIPT"]))
                return True
            else:
                copyFile(self.yaml["JsonPath"],"{}/tempFolder".format(self.yaml["QA_SCRIPT"]))
                return False
        elif self.projectName == "war":
            if self.svnUpdate() and self.yaml["convertCSV"]:
                from common import CsvToJson
                CsvToJson.Convert(self.yaml)

    def getApk(self):
        apkVersion = self.getNewVersion()["apkVersion"]
        print(apkVersion,"apkVersionapkVersionapkVersionapkVersion")
        """
        只接受集群包
        """
        url = "http://rc2.walle.playcrab-inc.com/walle/package/{}/full_package/{}-{}.apk".format(self.projectName,apkVersion,self.yaml["getType"]["clusterPrefix"])
        print(url,">>>")
        if os.path.exists("{}/{}.apk".format(self.yaml["APKPath"],"{}-{}".format(self.projectName,apkVersion))):
            print("已存在")
            # os.remove("{}/{}.apk".format(self.yaml["APKPath"],apkVersion))
        else:
            print("不存在")
            """
            暂时关闭清理apk方法
            """
            # for root,dirs,files in os.walk(test["APKPath"]):
            # 	for y in files:
            # 		if y[-3:] == "apk":
            # 			os.remove(os.path.join(root,y))
            urllib.request.urlretrieve(url,"{}/{}.apk".format(self.yaml["APKPath"],"{}-{}".format(self.projectName,apkVersion)))

        apkPath = "{}/{}.apk".format(self.yaml["APKPath"],"{}-{}".format(self.projectName,apkVersion))

        tempPath = os.path.join(self.yaml["QA_SCRIPT"],"newapk")
        if os.path.isdir(tempPath):
            shutil.rmtree(tempPath)
        os.makedirs(tempPath)
        shutil.copyfile(apkPath,os.path.join(tempPath,"newapk.apk"))

        return "{}/{}.apk".format(self.yaml["APKPath"],"{}-{}".format(self.projectName,apkVersion))

    # def installAPK(self,debug=False):
    #     """
    #     这里应当有2种准备模式,目前只支持debug模式，机柜模式需要等机柜部署完成后待定
    #     1.机柜，默认
    #     2.本地运行，debug=True
    #     """
    #     if self.yaml["install"]:
    #         tasks = []
    #         if os.path.exists(os.path.join(self.yaml["QA_SCRIPT"],"AirTest","install.air")):
    #             shutil.rmtree(os.path.join(self.yaml["QA_SCRIPT"],"AirTest","install.air"))
    #         shutil.copytree(self.yaml["install"],os.path.join(self.yaml["QA_SCRIPT"],"AirTest",self.yaml["install"].split("/")[-1]))
    #         import tempfile
    #         with tempfile.TemporaryDirectory() as tmpdirname:
    #             writeJsonFile([{"id":1,"scriptName":"{}".format(self.yaml["install"].split("/")[-1].replace(".air","")),"isRun":True}],os.path.join(tmpdirname,"tempTestCase.json"))
    #             try:
    #                 """
    #                 这里应当根据启动方式来决定，暂时使用debug配置
    #                 """
    #                 devicesList = []
    #                 if debug:
    #                     devicesTempList = ADB().devices()
    #                     # devicesDict = {}
    #                     # for x in range(len(devicesList)):
    #                     # 	devicesDict["devices" + str(x)] = devicesList[x][0]							
    #                     # devicesList = list(devicesDict.values())
    #                     for x in range(len(devicesTempList)):
    #                         devicesList.append("Android://127.0.0.1:5037/{}".format(devicesTempList[x][0]))
    #                         print("Android://127.0.0.1:5037/{}".format(devicesTempList[x][0]))
    #                 else:
    #                     headers = {"Authorization": "token f36a0961c25962fd6f0464ebf3b9d4c7f667f484"}
    #                     info = requests.get("http://10.2.146.116/v1/api/provider_device", headers=headers, timeout=3)
    #                     devicesInfo = info.json()
                    
    #                     for x in devicesInfo:
    #                         devicesList.append("Android://{}:5039/{}".format(x["ip"],x["serialno"]))
    #                         print("android://{}:5039/{}".format(x["ip"],x["serialno"]))

    #                 for x in devicesList:					
    #                     tasks.append({							
    #                         'process':subprocess.Popen("airtest run {} --device {}".format(os.path.join(self.yaml["QA_SCRIPT"],"AirTest",self.yaml["install"].split("/")[-1]), x), shell=True),
    #                         'dev':x})
    #                 for x in tasks:
    #                     status = x["process"].wait()
    #             except:
    #                 pass
    #         if os.path.exists(os.path.join(self.yaml["QA_SCRIPT"],"AirTest","install.air")):
    #             shutil.rmtree(os.path.join(self.yaml["QA_SCRIPT"],"AirTest","install.air"))


    def debug(self):	#本地测试环境准备
        self.tool()
        self.getApk()
        # 暂时关闭，请勿使用，如需要安装请手动连接设备执行install脚本
        # self.installAPK(debug=True) 暂时关闭,请勿使用


    def airlabPrepare(self):
        self.tool()
        self.getApk()






