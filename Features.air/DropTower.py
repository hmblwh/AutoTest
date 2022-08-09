# -*- encoding=utf8 -*-
__author__ = "TriTN2"

from airtest.core.api import *
from airtest.core.api import using
using("Content.air")
from Content import *
from Features import *
using("Main.air")
from ExcelUtility import *
using("ConfigReader")
from ConfigReader import ConfigReader

auto_setup(__file__)
fName = "DropTower"

def runDropTower(deviceId):
    try:
        ResetArrRs()
        for fn in getFunctionNeedTest(fName):
            print("Running: " + fn)
            eval(fn)
    except Exception as e:
        WriteLogCrash(e, fName)

def Test(caseId):
	click(FIGHT_BTN)
	playerLayer = poco('player_layer')
	opponentLayer = poco('opponent_layer')

	poco.wait_for_all([playerLayer, opponentLayer])
	sleep(5)
    