# -*- encoding=utf8 -*-
__author__ = "Administrator"
auto_setup(__file__)
from airtest.core.api import *
from poco.drivers.std import StdPoco
poco = StdPoco()
#获取购买前金币数量
buy_before_gold=poco("board2").offspring("lab").get_text()
#获取购买前钻石数量
buy_before_diamond=poco("board3").offspring("lab").get_text()
#打开交易所
poco("board2").child("btn").click()
sleep(0.7)
#获取单次购买单价
buy_pice=int(poco("costLab").get_text())
#获取单次购买数量
buy_number=int(poco("goalLab").get_text())
#获取当前可购买次数
buy_times=int(poco("canBuyNum").get_text().split("/",1)[0])
#如果有购买次数，进行单次购买
if buy_times > 0:
    poco("buyBtn").click()
    sleep(1.5)
    #断言购买次数是否减1
    try:
        assert_equal(int(poco("canBuyNum").get_text().split("/",1)[0]),buy_times - 1,"购买次数减1成功")
    except:
        log("购买次数未扣除：购买前为:%d;购买后为:%d"%(buy_times,int(poco("canBuyNum").get_text().split("/",1)[0])))
    #退出交易所
    poco("closeBtn").click()
else:
    log("当前已经没有购买次数")
    poco("closeBtn").click()
#购买后黄金获得是否正确的断言判断
if "万" in buy_before_gold:
    #黄金购买前带万的处理
    gold=int(buy_before_gold.split(".",1)[0])
    #之前已有黄金10以上断言购买后获得是否正确
    try:
        assert_equal(int(poco("board2").offspring("lab").get_text().split(".",1)[0]),int(gold+buy_number/10000),"金币购买获得数量正确")
    except:
        log("金币购买后获得数量异常：购买前为：%d;本次购买数量为：%d"%(gold,buy_number))
else:
    #黄金购买前不带万的处理
    gold=int(buy_before_gold)
        #购买后金币数量未到10万和达到10万的处理
    if gold + buy_number >= 100000:
        try:
            assert_equal(int(poco("board2").offspring("lab").get_text().split(".",1)[0]),int((gold + buy_number)/10000),"金币购买获得数量正确")
        except:
            log("金币购买后获得数量异常：购买前为：%d;购买数量为：%d"%(gold,buy_number))
    else:
        try:
            assert_equal(int(poco("board2").offspring("lab").get_text()),gold + buy_number,"金币购买获得数量正确")       
        except:
            log("金币购买后获得数量异常：购买前为：%d;购买数量为：%d"%(gold,buy_number))
#购买后钻石消耗是否正确的断言判断
if "万" in buy_before_diamond:
    #身上钻石带万字的处理
    diamond=int(buy_before_diamond.split(".",1)[0])
    #todo断言存在一个bug，在购买时小数点后面不够扣时按现在算法会出问题（购买单价不大，另一个可能身上钻石没有这么多，暂时还好）
    try:
        assert_equal(int(poco("board3").offspring("lab").get_text().split(".",1)[0]),diamond - int(buy_pice/10000),"钻石扣除正确")
    except:
        log("钻石扣除数量异常：购买前为：%d;购买价格为：%d"%(diamond,buy_pice))
else:
    diamond=int(buy_before_diamond)
    try:
        assert_equal(int(poco("board3").offspring("lab").get_text()),diamond - buy_pice,"钻石扣除正确")
    except:
        log("钻石扣除数量异常：购买前为：%d;购买价格为：%d"%(diamond,buy_pice))
