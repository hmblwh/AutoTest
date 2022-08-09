# -*- encoding=utf8 -*-
from collections import namedtuple
import re
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
config_card: dict = config.getConfigByElement("Card.json","card")
config_target_buff: dict = config.getConfigByElement("TargetBuff.json","targetBuff")
config_tower_buff: dict = config.getConfigByElement("TowerBuff.json","towerBuff")



def runCard(deviceId):
    try:
        ResetArrRs()
        for fn in getFunctionNeedTest(fName):
            print("Running: " + fn)
            eval(fn)
    except Exception as e:
        WriteLogCrash(e, fName)
def del_text(num = 5):
    for _ in range(num):
        keyevent("KEYCODE_DEL")

class CardModel:
    def __init__(self, _id) -> None:
        self.id = _id
        self.config = self._config()
        self.config_type = self._config_type()
        self.energy = self._energy()
        self.name = self._name()

        pass

    def _config(self):
        return config_list_card[str(self.id)]

    def _energy(self):
        _type = self.config["type"]
        _id = str(self.config["id"])
        if _type == "tower" :
            return config_tower[_id]["energy"]
        elif _type == "spell":
            return config_spell[_id]["energy"]

        pass

    def __str__(self) -> str:
        return "card " + str((self.id, self.energy))
    
    def __repr__(self) -> str:
        return self.__str__()
        

    def _name(self):
        _type = self.config["type"]
        _id = str(self.config["id"])
        if _type == "tower" :
            return config_tower[_id]["name"]
        elif _type == "spell":
            return config_spell[_id]["name"]

        pass

    def _config_type(self):
        _type = self.config["type"]
        _id = str(self.config["id"])
        if _type == "tower":
            return config_tower[_id]
        elif _type == "spell":
            return config_spell[_id]

            
def check_energy_card(case_id,card_model : CardModel, pocoItem):
    if str(card_model.energy) != pocoItem.child("<no-name>")[0].offspring("energy").get_text():
            WriteLogRunning(case_id, f"Card energy error card id {card_model.id} card name {card_model.name}", "", False, False)
            return False
    return True

def cheat_card_item(card_id,level = 1, fragments=0):
    if 1 <= level <= 12 and  0 <= fragments <= 1000:
        poco(HEADER_BTN_CHEAT).click()
        poco(CHEAT_POPUP_CARD_ID_INPUT).click()
        del_text()
        text(str(card_id))   
        poco(CHEAT_POPUP_CARD_LEVEL_INPUT).click()
        del_text()
        text(str(level))
        poco(CHEAT_POPUP_CARD_FRAGMENTS_INPUT).click()
        del_text()
        text(str(fragments))
        poco(CHEAT_POPUP_BTN_SENT).click()
    else:
        raise Exception("error aguments")

def check_card_config_detail(case_id,card_model:CardModel,pocoItem,level):
    pocoItem.click()
    if card_model.config["type"] == 'tower':
        check_config_tower(case_id,card_model,level)
    elif card_model.config["type"] == "spell":
        check_config_spell(case_id,card_model,level)
    poco(CARD_DETAIL_BTN_CLOSE).click()



def check_config_tower (case_id,card_model: CardModel,level):
    def check_damage(damage):
        if float(poco("card_info_popup_damage").offspring("value").get_text()) != float(f"{damage:.1f}") :
            WriteLogRunning(case_id, f"Card detail info error damage {card_model.id} card name {card_model.name} expect {damage}", "", False, False)

    def check_range(_range):
        if float(poco("card_info_popup_range").offspring("value").get_text()) != float(f"{_range:.1f}") :
            WriteLogRunning(case_id,f"Card detail info error range {card_model.id} card name {card_model.name} expect {_range}", "", False, False)

    def check_attack_speed(attack_speed):
        attack_speed = attack_speed /1000
        if float(poco("card_info_popup_attack_speed").offspring("value").get_text()) != float(f"{attack_speed:.1f}") :
            WriteLogRunning(case_id,f"Card detail info error attack speed {card_model.id} card name {card_model.name} expect {attack_speed}", "", False, False)

    def check_bullet_type(bullet_type):
        if poco("card_info_popup_bullet_type").offspring("value").get_text() != bullet_type:
            WriteLogRunning(case_id,f"Card detail info error bullet type {card_model.id} card name {card_model.name} expect {bullet_type}", "", False, False)
            
    def check_duration(duration):
        duration /= 1000
        text = poco("card_info_popup_duration").offspring("value").get_text()
        text = text[:-1]
        if float(text) == float(f"{duration:.1f}"):
            WriteLogRunning(case_id, f"Card detail info error duration {card_model.id} card name {card_model.name} expect {duration}", "", False, False)
    
    def check_damage_up(value):
        if float(poco("card_info_popup_damage_up").offspring("value").get_text()) != float(f"{value:.1f}") :
            WriteLogRunning(case_id, f"Card detail info error damage up {card_model.id} card name {card_model.name} expect {value}", "", False, False)

    def check_attack_speed_up(value):
        if float(poco("card_info_popup_attack_speed_up").offspring("value").get_text()) != float(f"{value:.1f}") :
            WriteLogRunning(case_id, f"Card detail info error attack speed up {card_model.id} card name {card_model.name} expect {value}", "", False, False)


    for evolution in range(1,4):
        if evolution >= 2:
            poco("right_chevron").click()
        evolution = str(evolution)
        
        if card_model.config["id"] in {0,1,2,3,4}:
            damage = card_model.config_type["stat"][evolution]["damage"]
            damage *= 1.1 ** (level-1)
            attack_speed = card_model.config_type["stat"][evolution]["attackSpeed"]
            bullet_type = card_model.config_type["bulletType"]
            check_damage(damage=damage)
            check_attack_speed(attack_speed = attack_speed)
            check_bullet_type(bullet_type = bullet_type)
        

        if card_model.config["id"] in {0,1,2,3,4,5,6}:
            _range = card_model.config_type["stat"][evolution]["range"]
            check_range(_range= _range)


        if card_model.config["id"] in {3}:
            duration = config_target_buff["0"]["duration"][evolution]
            check_duration(duration=duration)

        if card_model.config["id"] in {4}:
            duration = config_target_buff["1"]["duration"][evolution]
            check_duration(duration=duration)

        if card_model.config["id"] in {5}:
            value = config_tower_buff["3"]["effects"][evolution][0]["value"]
            check_damage_up(value=value)
        
        if card_model.config["id"] in {6}:
            value = config_tower_buff["4"]["effects"][evolution][0]["value"]
            check_attack_speed_up(value=value)


            


            
        


def check_config_spell (case_id,card_model: CardModel,level):
    def check_radius(value):
        if float(poco("card_info_popup_radius").offspring("value").get_text()) != float(f"{value:.1f}"):
            WriteLogRunning(case_id, f"Card detail info error radius {card_model.id} card name {card_model.name} expect {damage}", "", False, False)
    def check_damage(damage):
        if float(poco("card_info_popup_damage").offspring("value").get_text()) != float(f"{damage:.1f}") :
            WriteLogRunning(case_id, f"Card detail info error damage {card_model.id} card name {card_model.name} expect {damage}", "", False, False)
    def check_duration(duration):
        duration /= 1000
        text = poco("card_info_popup_duration").offspring("value").get_text()
        text = text[:-1]
        if float(text) == float(f"{duration:.1f}"):
            WriteLogRunning(case_id, f"Card detail info error duration {card_model.id} card name {card_model.name} expect {duration}", "", False, False)
    if card_model.config["id"] in {0,1,2}:
        if card_model.config["id"] in {0}:
            damage = card_model.config_type["adjust"]["player"]["value"]
        elif card_model.config["id"] in {1,2}:
            damage = card_model.config_type["damage"]
        radius = card_model.config_type["radius"]
        check_damage(damage)
        check_radius(radius)
    
    if card_model.config["id"] in {1}:
        
        duration = config_target_buff["2"]["duration"]["1"]
        check_duration(duration)

    if card_model.config["id"] in {2}:
        duration =  card_model.config_type["action"]["duration"]
        check_duration(duration)




def get_list_battle_card():
    cardIds = [int(id) for id in config_list_card.keys()]
    list_battle_card = []
    for cardId in cardIds:
        if poco(f"card_desk_item_{cardId}").exists():
            list_battle_card.append((CardModel(cardId),poco(f"card_desk_item_{cardId}")))
    return list_battle_card


def get_list_nomal_card ():
    cardIds = [int(id) for id in config_list_card.keys()]
    list_normal_card = []
    for cardId in cardIds:
        if poco(f"card_collection_item_{cardId}").exists():
            list_normal_card.append((CardModel(cardId),poco(f"card_collection_item_{cardId}")))
    return list_normal_card


def check_card_config(case_id):
    poco(NAV_BAR_BTN_CARD).click()

    list_battle_card = get_list_battle_card()


    # check num battle card
    if list_battle_card.__len__() != 8:
        WriteLogRunning(case_id, f"Num battle card diff 8 ({len(list_battle_card)})", "", False, False)
        return

    # check energy battle card on 
    for item in list_battle_card:
        check_energy_card(case_id,*item)
    
    list_normal_card = get_list_nomal_card()
    

    for item in list_normal_card:
        check_energy_card(case_id,*item)
    
    for _level in {1,11}:
        for item in list_battle_card:
            cheat_card_item(item[0].id,_level)
            sleep(1.0)
            check_card_config_detail(case_id,*item,_level)

        for item in list_normal_card:
            cheat_card_item(item[0].id,_level)
            sleep(1.0)
            check_card_config_detail(case_id,*item,_level)


def change_card(case_id,card_id_in,card_id_out):
    poco(NAV_BAR_BTN_CARD).click()
    list_normal_card = get_list_nomal_card()
    list_battle_card = get_list_battle_card()

    for item in list_normal_card:
        if item[0].id == card_id_in:
            item_in = item
            break
    else:
        WriteLogRunning(case_id, f"Not exist card id {card_id_in} in normal card list ", "", False, False)
        return

    for item in list_battle_card:
        if item[0].id == card_id_out:
            item_out = item
            break
    else:
        WriteLogRunning(case_id, f"Not exist card id {card_id_out} in battle card list ", "", False, False)
        return

    item_in[1].click()
    poco("card_info_popup_btn_choose").click()
    item_out[1].click()
    sleep(1)

    list_normal_card = get_list_nomal_card()
    list_battle_card = get_list_battle_card()


    for item in list_normal_card:
        if item[0].id == card_id_out:
            item_in = item
            break
    else:
        WriteLogRunning(case_id, f"Not exist card id {card_id_out} in normal card list ", "", False, False)
        return

    for item in list_battle_card:
        if item[0].id == card_id_in:
            item_out = item
            break
    else:
        WriteLogRunning(case_id, f"Not exist card id {card_id_in} in battle card list ", "", False, False)
        return

    WriteLogRunning(case_id, f"Change card succeed", "", False, True)

    


# def upgrade_card

        






    







