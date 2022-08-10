# -*- encoding=utf8 -*-
__author__ = "HungDX"

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
CARD_ID = "cardId_"
CLOSE_BTN = "close_button"
TEXT_COLOR ="Color_"
RECEIVE_BTN = "Receive_btn"
OPEN_CHEST_ITEM = "open_chest_"
NAV_SHOP = "nav_bar_item_shop"
CHEAT_BTN = "header_btn_cheat"
CHEAT_GOLD_TF = "gold_input"
CHEAT_GEM_TF = "gem_input"
CHEAT_BTN_SEND = "cheat_popup_btn_send"
config = ConfigReader()
config_list_card: dict = config.getConfigByElement("ListCard.json", "listCard")
    
def runShop(deviceId):
    try:
        ResetArrRs()
        for fn in getFunctionNeedTest(fName):
            print("Running: " + fn)
            moveToShopScreen()
            eval(fn)
    except Exception as e:
        WriteLogCrash(e, fName)   
        
# --------------------------------------Shop---------------------------------------

# Cheat giá trị của gold và gem 
# gold: giá trị gold muốn cheat
# gem: giá trị gem muốn cheat
def cheatGoldAndGem(caseId, gold, gem):
    # kiểm tra xem nút cheat đã có chưa
    if not poco(CHEAT_BTN).exists():
        WriteLogRunning(caseId, "cheatGoldAndGem failed - Do not have cheat button", "", False, False)
        return
    poco(CHEAT_BTN).click()
    sleep(1)
    # nhập gem vào textfield gem
    if poco(CHEAT_GEM_TF).exists():
        poco(CHEAT_GEM_TF).click()
        for i in range(10):
            keyevent("KEYCODE_DEL")
        text(str(gem))
    # nhập gold vào textfield gold
    if poco(CHEAT_GOLD_TF).exists():
        poco(CHEAT_GOLD_TF).click()
        for i in range(10):
            keyevent("KEYCODE_DEL")
        text(str(gold))
    # kiểm tra nút cheat có chưa
    if poco(CHEAT_BTN_SEND).exists():
        poco(CHEAT_BTN_SEND).click()
        sleep(3)
    else:
        WriteLogRunning(caseId, "cheatGoldAndGem failed - do not have send", "", False, False)
        return
    resourceGold = getResourceGold()
    resourceGem = getResourceGem()
    # so sánh giá trị cheat của gold đã đúng chưa
    if resourceGold != gold:
        WriteLogRunning(caseId, "cheatGoldAndGem failed - update gold failed", "", False, False)
    # so sánh giá trị cheat của gem đã đúng chưa
    if resourceGem != gem:
        WriteLogRunning(caseId, "cheatGoldAndGem failed - update gem failed", "", False, False)
        
    WriteLogRunning(caseId, "cheatGoldAndGem Success", "", False, True)

# Kiểm tra xem giá vàng và giá trị vàng đã đúng trong config chưa
# position nằm trong phạm vi từ 0 -> 2
# valueTitle là giá trị vàng của gói ta cần kiểm tra
# valueGem là giá của gói ta cần kiểm tra
def checkBuyGoldGUI(caseId, position, valueTitle, valueGem):
    if position < 0 or position > 2: 
        return            
    gameTitleValue = poco("buy_gold_" + str(position))[0].child("Node").child("title").get_text()
    gameTitleValue = int(gameTitleValue.replace('.', ''))
    value = poco("buy_gold_" + str(position) + "_btn")[0].child("Node").child("value").get_text()
    # kiểm tra xem số lượng vàng và giá gem của shop đã đúng với config truyền vào chưa
    if int(value) != valueGem or int(gameTitleValue) != valueTitle:
        WriteLogRunning(caseId, "Shop Config failed - ", "", False, False)
    WriteLogRunning(caseId, "Shop Config Success", "", False, True)

    
# Kiểm tra việc mua rương
# Cập nhật vàng và thẻ sau khi mua đã đúng chưa
def checkBuyChest(caseId):
    gold = getResourceGold()
    chestPrice = getShopItemPrice(0)
    if chestPrice == -1:
        WriteLogRunning(caseId, "checkBuyChest failed - chest has been bought", "", False, False)
        return
    shopBtn = poco("buy_item_0_btn")
    # nếu không đủ tiền mua rương thì báo lỗi
    if gold < chestPrice:
        WriteLogRunning(caseId, "checkBuyChest failed - do not have enough money to open chest", "", False, False)
        return
    shopBtn.click([0.5, 0.5])
    sleep(2)
    poco(BUY_BTN).click([0.5, 0.5])
    sleep(4)
    if not poco(RECEIVE_BTN).exists:
        WriteLogRunning(caseId, "checkBuyChest failed - do not appear open chest popup", "", False, False)
        return
    itemList = []
    # lưu giá trị của 3 item nhận được khi mở rương
    for i in range(0, 3):
        if poco(OPEN_CHEST_ITEM + str(i)).exists():
           cardItem = poco(OPEN_CHEST_ITEM + str(i))
           cardId = getCardId(cardItem)
           num = getNumberOfCardUI(cardItem)
           itemDict = {"id": cardId, "num": num}
            # nếu không phải là thẻ vàng thì ta sẽ lưu số lượng thẻ cũ để sau này so sánh
           if cardId != -1:
                oldNum = getNumberOfCard(getInventoryCardName(cardId))
                itemDict["oldNum"] = oldNum
           itemList.append(itemDict)
    poco(RECEIVE_BTN).click([0.5, 0.5])
                   
    for item in itemList:
        cardId = item["id"]
        num = item["num"]
        # item là vàng, kiểm tra xem giá trị vàng đã được cập nhật đúng chưa
        if cardId == -1:
           if getResourceGold() != gold + num - chestPrice:
                WriteLogRunning(caseId, "checkBuyChest failed - gold update wrong", "", False, False)
                
        else:
            # item là thẻ, kiểm tra xem thẻ cộng số lượng đã đúng chưa
            inventoryCardName = getInventoryCardName(cardId)
            if getNumberOfCard(inventoryCardName) != item["oldNum"] + num:
                print("new numCard: " + str(getNumberOfCard(inventoryCardName)));
                print("old Num: " + str(item["oldNum"]));
                WriteLogRunning(caseId, "checkBuyChest failed - card update wrong", "", False, False)
                
    WriteLogRunning(caseId, "Check Buy Chest success", "", False, True)
 
    
    
    
# Kiểm tra xem giá thẻ đã đúng như config chưa
# position là vị trí của thẻ trong shop item, nằm trong khoảng 1->2
# goldMultiplier là giá vàng với mỗi thẻ có trong gói
def checkCardPrice(caseId, position, goldMultiplier):
    if position < 1 or position > 2: 
        return         
    # Lấy số lượng card của item
    cardNumber = poco("buy_item_" + str(position))[0].child(CARD_NUMBER)[0].offspring("num").get_text()
    cardNumber = int(cardNumber.replace('x', ''))
    # lấy giá của item
    cardBtnPrice = getShopItemPrice(position)
    if cardBtnPrice == -1:
        WriteLogRunning(caseId, "check Card Price Failed - card has been bought", "", False, False)
       
    # tính ra giá của item mà mình mong muốn
    priceExpect = goldMultiplier * cardNumber
    if cardBtnPrice != priceExpect:
        WriteLogRunning(caseId, "check Card Price Failed - card price not the same as config", "", False, False)
    WriteLogRunning(caseId, "check Card Price Success", "", False, True)

    
    
# Kiểm tra xem mua card có update tài nguyên đúng không
# position là vị trí thẻ ta muốn mua range 1 -> 2
def checkBuyCard(caseId, position):
    if position < 1 or position > 2:
        return
    # lấy tài nguyên vàng của người chơi ra
    goldOldValue = getResourceGold()
    
    # lấy giá thẻ ra
    cardBtn = poco("buy_item_" + str(position) + "_btn")
    cardBtnPrice = getShopItemPrice(position)
    if cardBtnPrice == -1:
        WriteLogRunning(caseId, "check Buy Card failed - card has been bought", "", False, False)
    cardId = getCardId(poco("buy_item_" + str(position))[0].child(CARD_NUMBER))
    shopCardNumber = poco("buy_item_" + str(position))[0].child(CARD_NUMBER)[0].offspring("num").get_text()
    shopCardNumber = int(shopCardNumber.replace('x', ''))
    
    # Card id không có
    if cardId == -1:
        WriteLogRunning(caseId, "check Buy Card failed - card do not have id", "", False, False)
    inventoryCardName = getInventoryCardName(cardId)
    print("inventoryCardName: " + inventoryCardName)
    if inventoryCardName == "":
        WriteLogRunning(caseId, "check Buy Card failed - do not have that card id in inventory", "", False, False)
    oldNumCard = getNumberOfCard(inventoryCardName)
    print("oldNumCard: " + str(oldNumCard))
    
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
        if getResourceGold() != goldOldValue - cardBtnPrice:
            print("new value: " + str(getResourceGold()))
            print("old value: " + str(goldOldValue))
            WriteLogRunning(caseId, "check Buy Card failed - gold update not correct", "", False, False)
        # kiểm tra lượng thẻ cập nhật đã đúng chưa
        if getNumberOfCard(inventoryCardName) != oldNumCard + shopCardNumber:
            print("new value: " + str(getNumberOfCard(inventoryCardName)))
            print("old value: " + str(oldNumCard))
            WriteLogRunning(caseId, "check Buy Card failed - card update not correct", "", False, False)
            
    else:
        if getResourceGold() != goldOldValue:
            WriteLogRunning(caseId, "check Buy Card failed - gold update not correct", "", False, False)
        if getNumberOfCard(inventoryCardName) != oldNumCard:
            print("new value: " + str(getNumberOfCard(inventoryCardName)))
            print("old value: " + str(oldNumCard))
            WriteLogRunning(caseId, "check Buy Card failed - card update not correct", "", False, False)
            
    WriteLogRunning(caseId, "check Buy Card Success", "", False, True)
    
    
    
    
# kiểm tra xem màu text của nút mua đã đúng chưa
# canBuyColor là màu khi người dùng đủ tài nguyên để mua
# cannotBuyColor là màu khi người dùng không đủ tài nguyên để mua
def checkBuyTextColor(caseId, canBuyColor, cannotBuyColor):
    gold = getResourceGold()
    gem = getResourceGem()
    
    for i in range(0, 3):
        buyGoldBtnValue = getShopGoldPrice(i)
        buyItemBtnValue = getShopItemPrice(i)
        buyGoldNode = poco("buy_gold_" + str(i))[0].child("Node")
        buyItemNode = poco("buy_item_" + str(i))[0].child("Node")
          
        if gem < buyGoldBtnValue:
            # trường hợp màu của text phải là cannotBuyColor
            if not buyGoldNode.child(TEXT_COLOR + cannotBuyColor).exists():
                WriteLogRunning(caseId, "checkBuyTextColor Failed - wrong cannot buy color", "", False, False)
        else:
            # trường hợp màu của text phải là canBuyColor
            if not buyGoldNode.child(TEXT_COLOR + canBuyColor).exists():
                WriteLogRunning(caseId, "checkBuyTextColor Failed - wrong can buy color", "", False, False)
        if gold < buyItemBtnValue:
            # trường hợp màu của text phải là cannotBuyColor
            if not buyItemNode.child(TEXT_COLOR + cannotBuyColor).exists():
                WriteLogRunning(caseId, "checkBuyTextColor Failed - wrong cannot buy color", "", False, False)
        else:
            # trường hợp màu của text phải là canBuyColor
            if not buyItemNode.child(TEXT_COLOR + canBuyColor).exists():
                WriteLogRunning(caseId, "checkBuyTextColor Failed - wrong can buy color", "", False, False)
    WriteLogRunning(caseId, "checkBuyTextColor Success", "", False, True)



# kiểm tra xem lúc mua chest có show GUI hoặc thông báo không và giá chest có đúng không
# chestPrice là giá rương theo config
def checkBuyChestShowGUI(caseId, chestPrice): 
    gold = getResourceGold()
    chestBtn = poco("buy_item_0_btn")
    chestBtnPrice = getShopItemPrice(0)
    if chestPrice != chestBtnPrice:
        WriteLogRunning(caseId, "checkBuyChestShowGUI Failed - Price not the same as config", "", False, False)
    shouldShowGui = True
    if gold < chestBtnPrice:
        shouldShowGui = False
    chestBtn.click([0.5, 0.5])
    sleep(2)
    if poco(BUY_BTN).exists():
        if not shouldShowGui:
            WriteLogRunning(caseId, "checkBuyChestShowGUI Failed - not enough gold but still show GUI", "", False, False)
    if poco(CLOSE_BTN).exists():
        poco(CLOSE_BTN).click([0.5, 0.5])
    WriteLogRunning(caseId, "checkBuyChestShowGUI Success", "", False, True)
   


# kiểm tra xem khi mua gold bằng gem thì gem đã bị trừ đúng và số gold đã được cộng đúng
def checkBuyGold(caseId): 
    # các thông tin về resource của người chơi
    for i in range(0, 3):
        isShouldUpdate = True
        buyGoldBtn = poco("buy_gold_" + str(i) + "_btn")
        # lấy giá tiền của item vàng
        buyGoldPrice = getShopGoldPrice(i)
        # lấy phần thưởng của item vàng
        buyGoldValue = poco("buy_gold_" + str(i))[0].child("Node").child("title").get_text()
        buyGoldValue = int(buyGoldValue.replace('.', ''))
        goldOldValue = getResourceGold()
        gemOldValue = getResourceGem()
        # nếu số lượng gem không đủ so với giá thì lúc mua xong các tài nguyên không nên được cập nhật
        if buyGoldPrice > gemOldValue:
            isShouldUpdate = False
        buyGoldBtn.click([0.5, 0.5])
        sleep(1)
        if poco(BUY_BTN).exists():
            poco(BUY_BTN).click([0.5, 0.5])
        sleep(5)
        if isShouldUpdate: 
            # mua gold đáng lẽ phải thành công
            if getResourceGold() != goldOldValue + buyGoldValue:
                print("old value: " + str(goldOldValue))
                WriteLogRunning(caseId, "Buy Gold Failed - gold update not correct", "", False, False)
            if getResourceGem() != gemOldValue - buyGoldPrice:
                print("old value: " + str(gemOldValue))
                WriteLogRunning(caseId, "Buy Gold Failed - gem update not correct", "", False, False)
        
        else:
            # mua gold  thất bại
            if getResourceGold() != goldOldValue:
                WriteLogRunning(caseId, "Buy Gold Failed - gold update not correct", "", False, False)
            if getResourceGem() != gemOldValue:
                WriteLogRunning(caseId, "Buy Gold Failed - gem update not correct", "", False, False)
    WriteLogRunning(caseId, "Buy Gold Success", "", False, True)

    
def moveToShopScreen():
    if poco(NAV_SHOP).exists():
        poco(NAV_SHOP).click([0.5, 0.5])

# lấy giá của gói mua vàng
def getShopGoldPrice(position):
    return int(poco("buy_gold_" + str(position) + "_btn")[0].child("Node").child("value").get_text())
              
# lấy giá của gói mua item
def getShopItemPrice(position):
    text = poco("buy_item_" + str(position) + "_btn")[0].child("Node").child("value").get_text()
    try:
        value = int(text)
        return value
    except ValueError:
        WriteLogRunning(0, "getNumberOfCardUI failed - price is not number", "", False, False)
    return -1
# lấy tài nguyên vàng của người chơi
def getResourceGold():
    return int(poco(RESOURCE_GOLD)[0].offspring("value").get_text().replace('.', ''))

# lấy tài nguyên gem của người chơi
def getResourceGem():
    return int(poco(RESOURCE_GEM)[0].offspring("value").get_text().replace('.', ''))
    
# lấy id của thẻ item trong shop
# cardNumber: CardUIWithNumber trong code
def getCardId(cardNumber):
    cardIds = [int(id) for id in config_list_card.keys()]
    for cardId in cardIds:
        if cardNumber[0].child(CARD_ID + str(cardId)).exists():
            return cardId
    return -1

# lấy số lượng thẻ có trong gói mua item
# cardNumber: CardUIWithNumber trong code
def getNumberOfCardUI(cardNumber):
   text = cardNumber[0].offspring("num").get_text()
   num = int(text.replace('x', ''))
    
   return num

# lấy name của thẻ trong inventory với cardId tương ứng
def getInventoryCardName(cardId):
    name = f"card_desk_item_{cardId}"
    if poco(name).exists():
        return name
    name = f"card_collection_item_{cardId}"
    if poco(name).exists():
        return name
    return ""

# trả về số lượng thẻ đang có của card trong inventory
# cardName là name của thẻ trong poco
def getNumberOfCard(cardName):
    if not poco(cardName).exists:
        return -1
    numberText = poco(cardName)[0].child("card_progress_bar").offspring("text").get_text()
    print("numberText: " + numberText)
    currentNumber = numberText.split("/")[0]
    return int(currentNumber)
