#!/usr/bin/env python3
#coding=utf_8
class review_class:
    def __init__(self,name,sex,age):
        self.name=name
        self.sex=sex
        self.age=age
    def count(self):
        print(self.name,self.sex,self.age)
r_name=review_class("小明","男",16)
r_name.count()