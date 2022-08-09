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

RESOURCE_GEM = "resource_gem"
RESOURCE_GOLD = "resource_gold"
BUY_BTN = "Buy_btn"
CARD_NUMBER = "card_number"
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

# Kiểm tra xem giá vàng và giá trị vàng đã đúng trong config chưa
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

# Kiểm tra xem giá thẻ đã đúng như config chưa
def checkCardPrice(caseId, position, goldMultiplier):
    if position < 1 or position > 2: 
        return         
    # Lấy số lượng card của item
    cardNumber = poco("buy_item_" + str(position))[0].child(CARD_NUMBER)[0].offspring("num").get_text()
    cardNumber = int(cardNumber.replace('x', ''))
    # lấy giá của item
    cardBtnPrice = poco("buy_item_" + str(position) + "_btn")[0].child("Node").child("value").get_text()
    cardBtnPrice = int(cardBtnPrice)
    # tính ra giá của item mà mình mong muốn
    priceExpect = goldMultiplier * cardNumber
    if cardBtnPrice != priceExpect:
        WriteLogRunning(caseId, "check Card Price Failed - card price not the same as config", "", False, False)
        return
    WriteLogRunning(caseId, "check Card Price Success", "", False, True)

# Kiểm tra xem mua card có update tài nguyên đúng không
def checkBuyCard(caseId, position):
    if position < 0 or position > 2:
        return
    # lấy tài nguyên vàng của người chơi ra
    goldResource = poco(RESOURCE_GOLD)[0].offspring("value").get_text()
    goldOldValue = int(goldResource.replace('.', ''))
    
    # lấy giá thẻ ra
    cardBtn = poco("buy_item_" + str(position) + "_btn")
    cardBtnPrice = int(cardBtn[0].child("Node").child("value").get_text())
    shouldBeUpdate = True
    # nếu vàng hiện tại còn ít hơn giá thẻ thì mua nên không thành công
    if cardBtnPrice > goldOldValue:
        shouldBeUpdate = False
    cardBtn.click([0.5, 0.5])
    sleep(1)
    if poco(BUY_BTN).exists():
        poco(BUY_BTN).click([0.5, 0.5])
    sleep(5)
    
    if shouldBeUpdate:
        # kiểm tra lượng vàng cập nhật đã đúng chưa
        if int(poco(RESOURCE_GOLD)[0].offspring("value").get_text().replace('.', '')) != goldOldValue - cardBtnPrice:
            print("new value: " + poco(RESOURCE_GOLD)[0].offspring("value").get_text().replace('.', ''))
            print("old value: " + str(goldOldValue))
            WriteLogRunning(caseId, "check Buy Card failed - gold update not correct", "", False, False)
            return
    else:
        if int(poco(RESOURCE_GOLD)[0].offspring("value").get_text().replace('.', '')) != goldOldValue:
            WriteLogRunning(caseId, "check Buy Card failed - gold update not correct", "", False, False)
            return
    WriteLogRunning(caseId, "check Buy Card Success", "", False, True)
    
# def checkBuyTextColor(caseId):
#     gold = poco("resource_gold")
#     gem = poco("resource_gem")
#     for i in range(0, 3):
#         buyGoldBtnValue =  poco("buy_gold_" + str(i) + "_btn")[0].child("Node").child("value")
#         buyItemBtnValue =  poco("buy_item_" + str(i) + "_btn")[0].child("Node").child("value")
#         if gem < int(buyGoldBtnValue.get_text()):
#             # TODO: working here, can't get color
#             if buyGoldBtnValue


# kiểm tra xem lúc mua chest có show GUI hoặc thông báo không và giá chest có đúng không
def checkBuyChestShowGUI(caseId, chestPrice): 
    gold = poco("resource_gold")[0].offspring("value")
    gold = int(gold.get_text().replace('.', ''))
    chestBtn = poco("buy_item_0_btn")
    chestBtnPrice = chestBtn[0].child("Node").child("value").get_text()
    chestBtnPrice = int(chestBtnPrice)
    if chestPrice != chestBtnPrice:
        WriteLogRunning(caseId, "checkBuyChestShowGUI Failed - Price not the same as config", "", False, False)
        return
    shouldShowGui = True
    if gold < chestBtnPrice:
        shouldShowGui = False
    chestBtn.click([0.5, 0.5])
    sleep(2)
    if poco(BUY_BTN).exists():
        if not shouldShowGui:
            WriteLogRunning(caseId, "checkBuyChestShowGUI Failed - not enough gold but still show GUI", "", False, False)
            return
    WriteLogRunning(caseId, "checkBuyChestShowGUI Success", "", False, True)
   
# kiểm tra xem khi mua gold bằng gem thì gem đã bị trừ đúng và số gold đã được cộng đúng
def checkBuyGold(caseId): 
    # các thông tin về resource của người chơi
    for i in range(0, 3):
        gold = poco(RESOURCE_GOLD)[0].offspring("value")
        gem = poco(RESOURCE_GEM)[0].offspring("value")
        isShouldUpdate = True
        buyGoldBtn = poco("buy_gold_" + str(i) + "_btn")
        # lấy giá tiền của item vàng
        buyGoldPrice = buyGoldBtn[0].child("Node").child("value").get_text()
        buyGoldPrice = int(buyGoldPrice)
        # lấy phần thưởng của item vàng
        buyGoldValue = poco("buy_gold_" + str(i))[0].child("Node").child("title").get_text()
        buyGoldValue = int(buyGoldValue.replace('.', ''))
        goldOldValue = int(gold.get_text().replace('.', ''))
        gemOldValue = int(gem.get_text().replace('.', ''))
        # nếu số lượng gem không đủ so với giá thì lúc mua xong các tài nguyên không nên được cập nhật
        if int(buyGoldPrice) > gemOldValue:
            isShouldUpdate = False
        buyGoldBtn.click([0.5, 0.5])
        sleep(1)
        if poco(BUY_BTN).exists():
            poco(BUY_BTN).click([0.5, 0.5])
        sleep(5)
        if isShouldUpdate: 
            # mua gold đáng lẽ phải thành công
            if int(poco(RESOURCE_GOLD)[0].offspring("value").get_text().replace('.', '')) != goldOldValue + buyGoldValue:
                print("new value: " + poco(RESOURCE_GOLD)[0].offspring("value").get_text().replace('.', ''))
                print("old value: " + str(goldOldValue))
                WriteLogRunning(caseId, "Buy Gold Failed - gold update not correct", "", False, False)
                return
            if int (poco(RESOURCE_GEM)[0].offspring("value").get_text().replace('.', '')) != gemOldValue - buyGoldPrice:
                print("new value: " + poco(RESOURCE_GEM)[0].offspring("value").get_text().replace('.', ''))
                print("old value: " + str(gemOldValue))
                WriteLogRunning(caseId, "Buy Gold Failed - gem update not correct", "", False, False)
                return
        
        else:
            # mua gold  thất bại
            if int(poco(RESOURCE_GOLD)[0].offspring("value").get_text().replace('.', '')) != goldOldValue:
                WriteLogRunning(caseId, "Buy Gold Failed - gold update not correct", "", False, False)
                return
            if int(poco(RESOURCE_GEM)[0].offspring("value").get_text().replace('.', '')) != gemOldValue:
                WriteLogRunning(caseId, "Buy Gold Failed - gem update not correct", "", False, False)
                return
    WriteLogRunning(caseId, "Buy Gold Success", "", False, True)

    

