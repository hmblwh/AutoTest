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

# Start game với accName được truyền vào (). 

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
    
