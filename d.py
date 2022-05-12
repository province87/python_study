#!/usr/bin/env python3
#encoding=utf-8
import unittest
import os
import sys
import unicodedata
sys.path.append(os.getcwd())
from ddt import ddt,data,unpack
from a_2_package.sun_class import Test1
# sta="½"
# print(sta.isdigit())
# print(sta.isnumeric())
@ddt
class Test(unittest.TestCase):
    @data(*([1, 2],[4,5]))
    def test_02(self, value):
        print(value)

    #多组数据，拆分
#    @unpac拆分，相当于把数据的最外层结构去掉
    # @data(*testdata)：*号意为解包，ddt会按逗号分隔，将数据拆分（不需要@unpack方法装饰器了）
    testdata = [{1:{"name": "peter", "age": 23, "addr": "chengdu"},2:{"name": "peter", "age": 23, "addr": "chengdu"}}, {"a_1":{"name": "lily", "age": 24, "addr": "chengdu"},"a_2":{"name": "lily", "age": 24, "addr": "chengdu"}}]

    @data(*testdata)
    def test_09(self,aa):
        print(aa)
        # print(value22)
    # @data([[1,2,3], [3,4,5]])
    # def test_02(self, a):
    #     for i in a:
    #         print(i)
    # def test_2(self):
    #     a=1
    #     b=1
    #     self.assertGreaterEqual(a,b,"a不大于b")
    # def test_3(self):
    #     a=1
    #     b=1
    #     self.assertGreaterEqual(a,b,"a不大于b")

# @ddt
# class MyddtTest(unittest.TestCase):
#
#     # @data方法装饰器
#     # 单组元素
#     @data(self.bi())
#     def test_01(self,value):   # value用来接受data的数据
#         print("samo",value)
if __name__ == "__main__":
    unittest.main()