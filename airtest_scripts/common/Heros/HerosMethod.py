#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : chenfengwu@playcrab.com
# @Desc    :

from common.CommonMethod import *
import json


class HerosMethod:
    def __init__(self, QAPath, jsonName):
        if "lang" in jsonName:#如果是lang表，先把已知的lang表合并，查询lang表相关的内容是无需传入“_和序号”
            self.jsonData = {}
            json_list = []
            for x in range(0,9):
                json_list.append("lang_{}".format(x))
            for x in json_list:
                self.jsonData.update(loadFile("{}/herojson/{}.json".format(QAPath, x)))
        else:
            self.jsonData = loadFile("{}/herojson/{}.json".format(QAPath, jsonName))


    def get_all_data(self):
        return self.jsonData

    def key_query(self, keyName):
        for x in self.jsonData:
            if keyName == x:
                return self.jsonData[x]

class ToolJson:
    def __init__(self,QAPath):
        self.QAPath = QAPath
        self.json_data = HerosMethod(self.QAPath,"tool")
        self.lang_json = HerosMethod(self.QAPath,"lang")
        self.team_json = HerosMethod(self.QAPath,"team")

    def name_query(self,name,art = False):#根据中文名字获取道具id,消耗时间长
        tool_data = self.json_data.get_all_data()
        for x in tool_data:
            if tool_data[x].get("name"):#获取lang表中的x
                language_name = tool_data[x]["name"]
                if self.lang_json.key_query(language_name):
                    name_date = self.lang_json.key_query(language_name).get("cn")
                    if art:
                        if name == name_date or ("#"+ name) == name_date and art == tool_data[x].get("art1"):
                            return x
                            break
                    else:
                        if name == name_date or ("#"+ name) == name_date and not tool_data[x].get("art1"):
                            return x
                            break
                else:
                    pass


    def noet_bag_name_query(self,name):#根据中文名字获取道具id,消耗时间长
        tool_data = self.json_data.get_all_data()
        bag_list = []
        for x in tool_data:
            if tool_data[x].get("name"):#获取lang表中的x
                language_name = tool_data[x]["name"]
                if self.lang_json.key_query(language_name):
                    name_date = self.lang_json.key_query(language_name).get("cn")
                    if name == name_date or ("#"+ name) == name_date:
                        bag_list.append(int(x))
                        continue
                else:
                    pass
        return max(bag_list)        

    def team_name_query(self,name):#根据中文名字获取兵营id,消耗时间长
        team_data = self.team_json.get_all_data()
        for x in team_data:
            if team_data[x].get("name"):#获取lang表中的x
                language_name = team_data[x]["name"]
                if self.lang_json.key_query(language_name):
                    name_date = self.lang_json.key_query(language_name).get("cn")
                    if name == name_date or ("#"+ name) == name_date:
                        return x

    def tool_name(self,name):#根据道具表中name获取中文名称
        if self.lang_json.get_all_data().get(name):
            if "#" in self.lang_json.get_all_data()[name].get("cn"):
                return self.lang_json.get_all_data()[name].get("cn").replace("#","")
            else:
                return self.lang_json.get_all_data()[name].get("cn")

    def id_tool_name(self,tool_id):#根据id获取道具表中name
        tool_data = self.json_data.get_all_data()
        for x in tool_data:
            if x == tool_id:
                lang_name = tool_data[x].get("name")
                return lang_name

    def tool_name_id(self,name):#道具表中name获取id
        tool_data = self.json_data.get_all_data()
        for x in tool_data:
            if tool_data[x].get("name"):
                if tool_data[x]["name"] == name:
                    return x