#!/usr/bin/env python3
#encoding=utf-8
import unittest
import json
class json_data(unittest.TestCase):
    def test_revert_files(self):
        with open(r"E:\venom\temp_json\ability.json","r") as load_f:
            print("打开写入load_f的数据：",load_f)
            load_dict=json.load(load_f)
            print("转换数据类型后的数据",load_dict)
            print("输出所有key",load_dict.keys())
            print("输出所有key的值",load_dict.values())
            return load_dict
    def test_case_1(self):
        self.assertIn(4,[5,4],"2不在表中")
    def test_case_2(self):
        self.assertIn(2,[5,4],"2不在表中")
if __name__ == "__main__":
    unittest.main()

