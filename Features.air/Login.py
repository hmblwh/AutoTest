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
fName = "Login"

# config = ConfigReader()
# configUser = config.getConfigByElement(EXTRA_JS, "User")

def runLogin(deviceId):
    try:
        ResetArrRs()
        for fn in getFunctionNeedTest(fName):
            print("Running: " + fn)
            eval(fn)
    except Exception as e:
        WriteLogCrash(e, fName)   
        
# --------------------------------------Login---------------------------------------

# Start game với accName được truyền vào (trên 6 kí tự). 
# Nếu accName chưa có trong list thì sẽ check Register account đó



def StartGame(caseId, accName): 
    isShouldBeLobby = True
    errorStr = ""
    # số lượng ký tự không có
    if len(accName) < 1: 
        error = "Account name is too short"
        isShouldBeLobby = False
    # số lượng ký tự quá nhiều - Fix nên dữ liệu nhập vào bị dừng ở 15 ký tự
    elif len(accName) >= 16: 
        errorStr = "Account name is too long"
        isShouldBeLobby = True
    # có chứa ký tự đặc biệt
    elif IsSpecialCharacter(accName):
        errorStr = "Account name has special character"
        isShouldBeLobby = False
        
    if poco("fightButton").exists(): 
        LogOut()
        sleep(2)
    Login(accName)
    sleep(2)
    
    if poco("fightButton").exists(): 
        if not isShouldBeLobby:
            WriteLogRunning(caseId, "Login Fail - " + errorStr, "", False, False)
            return
    WriteLogRunning(caseId, "Login Success ", "", False, True)

#     if len(accName) < 6:
#         WriteLogRunning(caseId, "Login Fail - Account name is too short", "", False, False)
#         return
#     isRegister = False
#     idAccLogin = -1
#     for i in range(len(configUser)):
#         if configUser[i]["nameLogin"] == accName: # Có sẵn trong list
#             idAccLogin = i
#             break
#     if idAccLogin < 0:  # Không có trong list thì check đăng kí
#         isRegister = True
#     if poco(BTN_PLAY).exists(): # Đã login từ trước
#         ClosePopups()
#         print("Already logged in game")
#         curId = GetCurUId()
#         if isRegister:  # Register account mới
#             LogOut()
#             LoginZAcc(caseId, accName, isRegister)
#             ClosePopups()
#             CheckImgExists(caseId, "Register account %s" %accName, poco(BTN_VIP), True)
#         else: # Login account được chỉ dịnh    
#             if curId != configUser[idAccLogin]["userId"]:
#                 LogOut()
#                 LoginZAcc(caseId, accName, isRegister)
#                 ClosePopups()
#             CheckImgExists(caseId, "Login game by account %s" %accName, poco(BTN_VIP), True)
#     else:
#         if exists(loginFB): # Chưa login, đang show form login FB
#             keyevent("BACK")
#             sleep(10)
#         CheckImgExists(caseId, "At scene login", poco(BTN_GUEST), True)
#         if poco(BTN_GUEST).exists():
#             LoginZAcc(caseId, accName, isRegister)
#             ClosePopups()
#             CheckImgExists(caseId, "Log into game", poco(BTN_VIP), True, True, 3)
    
def LogOut():
    poco("btnLogout").click([0.5, 0.5])

def Login(accName):
    poco("tfUserName").click([0.5, 0.5])
    for i in range(10):
        keyevent("KEYCODE_DEL")
    text(accName)
    poco("btnLogin").click([0.5, 0.5])
    
def IsSpecialCharacter(accName):
  regex= re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
  if(regex.search(accName) == None): 
    res = False
  else: 
    res = True
  return(res)
    
def LoginZAcc(caseId, accName, isRegister): #Chưa check new user có tutorial
    if not poco(BTN_ZACC).exists():
        poco(BTN_CHEAT).click([0.5,0.5])
    poco(BTN_ZACC).click([0.5,0.5])
    poco(BOX_NAME).click([0.5,0.5])
    for i in range(10):
        keyevent("KEYCODE_DEL")
    text(accName)
    poco(BOX_PASS).click([0.5,0.5])
    for i in range(10):
        keyevent("KEYCODE_DEL")
    text(passLogin)
    if isRegister: 
        poco(BTN_REGISTER).click([0.5,0.5])
    else: 
        poco(BTN_LOGINZ).click([0.5,0.5])
    sleep(15)
    if poco(text = NOTIFICATION).exists():
        poco(BTN_OK).click()
        if poco(text = TXT_ACC_EXISTS).exists():
            WriteLogRunning(caseId, "Register Fail - Account %s already exists" %accName, "", False, False)
        if poco(text = TXT_ACC_INCORRECT).exists():
            WriteLogRunning(caseId, "Login Fail - Username/Pass is invalid", "", False, False)  
        poco(BTN_OUT_LOGINZ).click([0.5,0.5])
