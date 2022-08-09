# -*- encoding=utf8 -*-
__author__ = "LinhDNA"

from airtest.core.api import *
import traceback
from airtest.cli.parser import cli_setup
import datetime
from airtest.core.api import using
using("Constant.air")
from Constant import *
using("Features.air")
from Features import *
from Login import *
from Shop import *
from DropTower import *
using("Content.air")
from Content import *
using("Main.air")
from ExcelUtility import *

auto_setup(__file__)
extraData = json.loads(args.extraData)
print("extraData: ", extraData)
deviceId = extraData["Device"]
extraData.pop("Device")
# print("listTC: ", extraData)

init(deviceId)   

if startByOpening:
    if PKG not in device().list_app():
        install(APK)
    stop_app(PKG)
    start_app(PKG)
    sleep(20)

timeNow = datetime.datetime.now()   
reportName = "Report\Device %s_%s%s_%s%s%s.xlsx" %(deviceId, timeNow.strftime("%d"), timeNow.strftime("%m"), timeNow.strftime("%H"), timeNow.strftime("%M"), timeNow.strftime("%S"))
getFileLogWriter(reportName)

for caseName in extraData:
    if extraData[caseName]:
        timeNow = datetime.datetime.now()    
        setStartTime(timeNow)
        
        try:
            fn = "run%s(%s)" %(caseName, deviceId)
            print("Run Test: " + fn)
            eval(fn)
        except Exception as e:
            traceback.print_exc()
            print("Error when play %s on Device %s" %(caseName, deviceId))
        
        timeNow = datetime.datetime.now()
        testEnd = str(timeNow)[:str(timeNow).find('.')]
        setEndTime(testEnd)
        
        WriteReport(caseName)

closeFileLog(reportName)