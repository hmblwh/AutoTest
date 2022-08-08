# -*- encoding=utf8 -*-
__author__ = "LinhDNA"
from collections import namedtuple
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
fName = "Card"

config = ConfigReader()
config_list_card: dict = config.getConfigByElement("ListCard.json", "listCard")
config_tower: dict = config.getConfigByElement("Tower.json", "tower")
config_spell: dict = config.getConfigByElement("Potion.json","potion")


def runCard(deviceId):
    try:
        ResetArrRs()
        for fn in getFunctionNeedTest(fName):
            print("Running: " + fn)
            eval(fn)
    except Exception as e:
        WriteLogCrash(e, fName)

class CardModel:
    def __init__(self, _id) -> None:
        self.id = _id
        self.energy = self._energy(); 
        pass

    def config(self):
        return config_list_card[str(self.id)]

    def _energy(self):
        _type = self.config()["type"]
        _id = str(self.config()["id"])
        if _type == "tower" :
            return config_tower[_id]["energy"]
        elif _type == "spell":
            return config_spell[_id]["energy"]

        pass

    def __str__(self) -> str:
        return "card " + str((self.id, self.energy))
    
    def __repr__(self) -> str:
        return self.__str__()
        pass

            
        
            
def check_card_config(caseId):
    poco(NAV_BAR_BTN_CARD).click()

    cardIds = [int(id) for id in config_list_card.keys()]


    list_battle_card = []
    for cardId in cardIds:
        if poco(f"card_desk_item_{cardId}").exists():
            list_battle_card.append((CardModel(cardId),poco(f"card_desk_item_{cardId}")))


    # check num battle card
    if list_battle_card.__len__() != 8:
        WriteLogRunning(caseId, f"Num battle card diff 8 ({len(list_battle_card)})", "", False, False)
        return

    # check energy battle card on 
    for item in list_battle_card:
        card: CardModel = item[0]
        if str(item[0].energy) != item[1].child("<no-name>")[0].offspring("energy").get_text():
            WriteLogRunning(caseId, f"Card energy diff card id {item[0].id}", "", False, False)
            return

    
        
    

    
    print("List bt card",list_battle_card)


    







