# -*- encoding=utf8 -*-
__author__ = "LinhDNA"

import datetime 
import traceback
#import pandas as pd
from airtest.core.api import *
from poco.drivers.cocosjs import CocosJsPoco
poco = CocosJsPoco()
from airtest.core.api import using
using("Constant.air")
from Constant import *
using("Content.air")
from Content import *
using("Api.air")
from Api import *
using("Main.air")
from ExcelUtility import *
using("ConfigReader")
from ConfigReader import ConfigReader
auto_setup(__file__)

lastCheckPoint, tcPass = True, True
countPass, countFail = 0, 0
arrRs, popups = [], []
# config = ConfigReader()

def init(v1):
    global runningDevice
    runningDevice = v1
    
# ========================== Common Function ==========================     
    
# Reload lobby bằng cách bấm chọn bàn rồi thoát
def ReloadLobby(isReload = False, isClose = True):
    poco(BTN_SELECT_TABLE).click([0.5,0.5])
    sleep(1)
    poco(BTN_EXIT).click()
    sleep(1)
    ClosePopups(isReload, isClose)

# Ở Lobby đóng các loại Popups có thể có, xếp theo thứ tự ưu tiên
# Sau khi gọi hàm này, có thể dùng data trong popups để check nếu cần
# isReload: Có reload lần nữa không? Nhiều game cheat time xong phải reload Lobby 2 lần 
# isClose: Click btn Close không? Nhiều GUI có thể check click btn khác để close
def ClosePopups(isReload = False, isClose = True):
    global popups
    if not isReload:
        popups = []
    if poco(TXT_CLAIM_WELCOME).exists() and poco(TXT_CLAIM_WELCOME).get_text() == CLAIM_WELCOME_GOLD:
        popups.append(WELCOME)
        poco(TXT_CLAIM_WELCOME).click()
        sleep(1)
    # Popup Claim Ranking Reward
    if poco(TXT_CLAIM).exists() and poco(TXT_CLAIM).get_text() == TOP_CONGRAT:
        popups.append(RANKING_REWARD)
        poco(BTN_CLAIM_REWARD).click()
        poco(BTN_CLOSE).click()
        sleep(1)
    # Popup Final Ranking
    if poco(GUI_END_RANKING).exists():
        popups.append(FINAL_RANING)
        poco(BTN_CONFIRM).click()
        sleep(1)
    # Popup Daily Bonus
    if poco(text = TXT_TODAY).exists():
        popups.append(DAILY_BONUS)
        poco(BTN_CLAIM_BONUS).click()
        sleep(1)
    # Tutorial        
    if poco(IMG_HAND).exists():
        popups.append(TUTORIAL)
        poco(BTN_PLAY).click()
        poco(BTN_LEAVE_GAME).click()
        sleep(1)
    # Popup Event WC
    if poco(POPUP_WC).exists():
        popups.append(POPUP_EVENT_WC)
        if isClose:
            poco(BTN_CLOSE).click()
        else:
            poco(BTN_ACTION).click()
            CheckImgExists(0, "Click Join Now In Popup Event, Open Event WC", poco(TITLE_GUI, text = TITLE_WC))
            if lastCheckPoint:
                poco(BTN_CLOSE).click()
                popups.append(EVENT_WC)
        sleep(1)
    # Event WC
    if poco(TITLE_GUI, text = TITLE_WC).exists():
        popups.append(EVENT_WC)
        poco(BTN_CLOSE).click()
        sleep(1)
    # Popup Final Ranking - Show after GUI Event when next day
    if poco(GUI_END_RANKING).exists():
        popups.append(FINAL_RANING)
        poco(BTN_CONFIRM).click()
        sleep(1)
    print("Popups List: %s" % popups)
    # Popup Deal Event WC
    if poco(TITLE_GUI, text = TITLE_DEAL).exists():
        popups.append(DEAL_WC)
        poco(BTN_CLOSE).click()
        sleep(1)
    # Popup Normal Deal Event HC
    if poco(GUI_OFFER_HC).exists():
        popups.append(NORMAL_OFFER_HC)
        poco(BTN_CLOSE).click()
        sleep(1)
    # Popup Normal Deal Event HC
    if poco(GUI_SALE_OFFER_HC).exists():
        popups.append(SALE_OFFER_HC)
        poco(BTN_CLOSE).click()
        sleep(1)
    # Popup Daily Bonus
    if poco(text = TXT_TODAY).exists():
        popups.append(DAILY_BONUS)
        poco(BTN_CLAIM_BONUS).click()
        sleep(1)
    # Notifications
    if poco(TITLE_GUI, text = NOTIFICATION).exists():
        popups.append(NOTI)
        poco(BTN_CLOSE).click()
        sleep(1)
    # Shop - receive gold support
    if poco(GUI_SHOP).exists():
        if poco(BTN_RECEIVE).exists():
            poco(BTN_RECEIVE).click()
            poco(BTN_BACK).click() # Touch out to receive
        poco(BTN_BACK).click()
        popups.append(GOLD_SUPPORT)
        sleep(1)
    # Popup Offer 1st
    if poco(GUI_OFFER_1ST).exists():
        popups.append(OFFER_1ST)
        poco(BTN_CLOSE).click()
        sleep(1)
    # Join Ranking
    if poco(text = GUI_RANKING).exists():
        popups.append(JOIN_RANKING)
        poco(BTN_CLOSE).click()
        sleep(1)

def CheckPopupVisible(popupName):
    hasPopupName = False
    for i in range(len(popups)):
        if popups[i] == popupName:
            hasPopupName = True
            break
    return hasPopupName
    
def RestartGame(caseId, timeWait=20):
    stop_app(PKG)
    start_app(PKG)
    sleep(timeWait)
    ReloadLobby()

# ========================== Get User Current Data ========================== 

def GetCurUId():
    poco(NODE_AVATAR).offspring(AVATAR).click()
    uId = poco(TXT_USER_ID).get_text()
    print("---------Current ID: %s" % uId)
    poco(BTN_CLOSE).click()
    return uId

# ========================== Write log ========================== 

# Kiểm tra xem show hình ảnh đúng mong đợi hay không rồi ghi log
# isExist: Check hình A có đang show không
# Nếu mong đợi là CÓ SHOW thì để isExists = True
# Nếu mong đợi là KHÔNG show thì để isExists = False
def CheckImgExists(caseId, step, content, isPoco = True, isExists = True, timeWait = 1):
    ST.FIND_TIMEOUT_TMP = timeWait
    isEx = False
    if isPoco:
        isEx = content.exists()
    else:
        isEx = exists(content)
    if isEx:
#         print("Found %s" % content)
        WriteLogRunning(caseId, step, content, True, isExists)
    else:
#         print("Not Found %s" % content)
        WriteLogRunning(caseId, step, content, True, not isExists)

# Kiểm tra text hiển thị đúng hay sai rồi ghi log
def CheckTxtExists(txtInGame, txtCompare, caseId, step):
    if txtCompare in txtInGame:
        WriteLogRunning(caseId, step, txtCompare, False, True)
    else:
        WriteLogRunning(caseId, step, txtCompare, False, False, txtInGame)     
        
# Ghi log, áp dụng cho check Image, Gold
def WriteLogRunning(caseId, step, content, isImg, isPass, txtInGame = ""):
    global tcPass, lastCheckPoint
    global arrRs
    des = step
    img = ""
    reason = ""
    timeFail = ""
    timeInterval = ""
    if isPass:
        if not isImg:
            des = "%s %s" %(step, content)
        stt = "Pass"
        lastCheckPoint = True
    else:
        failTime = datetime.datetime.now()
        if isImg:
            print("\n%s   |   %s   |   [FAIL]\n" % (caseId, step))
            content = "%s" % content
            if content[:2] == "P(":
                content = content[2:content.find(')')]
            print("\n   |   Find: %s\n" % content)
            url = generateScreenshotName(runningDevice, failTime)
            screenShot = snapshot(url)
            print("\n   |   Actual: %s\n" % (screenShot))
            img = url 
            reason = "Image --#-- Ingame"
        else:
            des = "%s %s" %(step, content)
            if txtInGame == "":
                print("\n%s   |   %s:   |   [FAIL]\n" % (caseId, des))
                url = generateScreenshotName(runningDevice, failTime)
                screenShot = snapshot(url)
                img = url
            else:
                url = generateScreenshotName(runningDevice, failTime)
                screenShot = snapshot(url)
                img = url
                print("\n%s   |   %s --#-- In Game: %s   |   [FAIL]\n" % (caseId, des, txtInGame))
                reason = "Expect: %s --#-- In Game: %s" %  (content, txtInGame)
        timeFail = str(failTime)[:str(failTime).find('.')]
        print('\n   |   Fail time: %s\n' %timeFail)
        stt = "Fail"
        periodTime = int(failTime.timestamp()) - int(timeStart.timestamp())
        timeInterval = "Phút " + str(periodTime // 60) + ":" + str(periodTime % 60)
        lastCheckPoint = False
        tcPass = False
        
    arrRs.append({
        'content': str(caseId) + " - " + des,
        'status': stt,
        'image': img,
        'reason': reason,
        'time': timeFail,
        'interval': timeInterval
    })
    #print("---------%s" %arrRs)

def ResetArrRs():
    global arrRs
    arrRs = []
    
def WriteLogCrash(exeption, fName):
    global arrRs
    crashTime = datetime.datetime.now()
    url = generateScreenshotName(runningDevice, crashTime)
    img = snapshot(filename = url)
    timeCrash = str(crashTime)[:str(crashTime).find('.')]
    periodTime = int(crashTime.timestamp()) - int(timeStart.timestamp())
    timeInterval = "Phút " + str(periodTime // 60) + ":" + str(periodTime % 60)
    arrRs.append({
        'content': "Crash when check " + fName,
        'status': "CRASH",
        'image': url,
        'reason': repr(exeption),
        'time': timeCrash,
        'interval': timeInterval
    })
    traceback.print_exc() 
    
def WriteReport(caseName):
    global arrRs
    writeLogTest(arrRs, caseName)