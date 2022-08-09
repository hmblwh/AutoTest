# -*- encoding=utf8 -*-
__author__ = "LinhDNA"

from airtest.core.api import *
from airtest.core.api import using
using("Content.air")
from Content import *
from Features import *
using("Main.air")
from ExcelUtility import *
using("ConfigReader")
from ConfigReader import ConfigReader
import re

auto_setup(__file__)
fName = "Shop"

# config = ConfigReader()
# configUser = config.getConfigByElement(EXTRA_JS, "User")

def runShop(deviceId):
    try:
        ResetArrRs()
        for fn in getFunctionNeedTest(fName):
            print("Running: " + fn)
            eval(fn)
    except Exception as e:
        WriteLogCrash(e, fName)   
        
# --------------------------------------Shop---------------------------------------

# range position from 0 - 2
# valueTitle is the gold title we need to check
# valueGem is the gem value we need to check
def checkBuyGoldGUI(caseId, position, valueTitle, valueGem):
    if position < 0 or position > 2: 
        return            
    gameTitleValue = poco("buy_gold_" + str(position))[0].child("Node").child("title").get_text()
    gameTitleValue = int(gameTitleValue.replace('.', ''))
    value = poco("buy_gold_" + str(position) + "_btn")[0].child("Node").child("value").get_text()
    # kiểm tra xem số lượng vàng và giá gem của shop đã đúng với config truyền vào chưa
    if int(value) != valueGem or int(gameTitleValue) != valueTitle:
        WriteLogRunning(caseId, "Shop Config failed - " + str(i), "", False, False)
        return              
    WriteLogRunning(caseId, "Shop Config Success", "", False, True)

# def checkBuyTextColor(caseId):
#     gold = poco("resource_gold")
#     gem = poco("resource_gem")
#     for i in range(0, 3):
#         buyGoldBtnValue =  poco("buy_gold_" + str(i) + "_btn")[0].child("Node").child("value")
#         buyItemBtnValue =  poco("buy_item_" + str(i) + "_btn")[0].child("Node").child("value")
#         if gem < int(buyGoldBtnValue.get_text()):
#             # TODO: working here, can't get color
#             if buyGoldBtnValue

# kiểm tra xem khi mua gold bằng gem thì gem đã bị trừ đúng và số gold đã được cộng đúng
def checkBuyGold(caseId): 
    # các thông tin về resource của người chơi
    gold = poco("resource_gold")[0].offspring("value")
    gem = poco("resource_gem")[0].offspring("value")
    for i in range(0, 3):
        isShouldUpdate = True
        buyGoldBtn = poco("buy_gold_" + str(i) + "_btn")
        # lấy giá tiền của item vàng
        buyGoldPrice = buyGoldBtn[0].child("Node").child("value").get_text()
        buyGoldPrice = int(buyGoldPrice)
        # lấy phần thưởng của item vàng
        buyGoldValue = poco("buy_gold_" + str(i))[0].child("Node").child("title").get_text()
        buyGoldValue = int(buyGoldValue.replace('.', ''))
        goldOldValue = int(gold.get_text().replace('.', ''))
        gemOldValue = int(gold.get_text().replace('.', ''))
        # nếu số lượng gem không đủ so với giá thì lúc mua xong các tài nguyên không nên được cập nhật
        if int(buyGoldPrice) < gemOldValue:
            isShouldUpdate = False
        buyGoldBtn.click([0.5, 0.5])
        sleep(1)
        if poco("Buy_btn").exists():
            poco("Buy_btn").click([0.5, 0.5])
        sleep(2)
        # mua gold thành công và gold resource cập nhật thêm số gold được thông báo lên
        if int(gold.get_text().replace('.', '')) == goldOldValue + buyGoldValue:
            # nếu mua đáng lẽ không thành công
            if not isShouldUpdate:
                WriteLogRunning(caseId, "Buy Gold Failed - Gold should not be update", "", False, False)
            if int(gem.get_text().replace('.', '')) != gemOldValue - buyGoldPrice:
                WriteLogRunning(caseId, "Buy Gold Failed - Gem did not update", "", False, False)
        else:
            # mua gold thất bại
            # nếu mua đáng lẽ thành công
            if isShouldUpdate:
                WriteLogRunning(caseId, "Buy Gold Failed - Gold should be update", "", False, False)
            if int(gem.get_text().replace('.', '')) == gemOldValue - buyGoldPrice:
                WriteLogRunning(caseId, "Buy Gold Failed - buy fail but gem still update", "", False, False)

    WriteLogRunning(caseId, "Buy Gold Success", "", False, True)

    

