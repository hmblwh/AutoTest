# -*- encoding=utf8 -*-
from collections import namedtuple
import re
from unittest import case
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
        damage *= 1.1**(level-1)
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


    # kiểm tra số thẻ battle card
    if list_battle_card.__len__() != 8:
        WriteLogRunning(case_id, f"Num battle card diff 8 ({len(list_battle_card)})", "", False, False)
        return

    # kiểm tra config năng lượng của tất cả các thẻ battle
    for item in list_battle_card:
        check_energy_card(case_id,*item)
    
    list_normal_card = get_list_nomal_card()
    
    # kiểm tra config năng lượng của tất cả các thẻ thường
    for item in list_normal_card:
        check_energy_card(case_id,*item)
    
    # cheat level các thẻ và dọc tất cả chỉ số
    for _level in range(1,11):
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

    # kiểm tra id thẻ in có nằm trong thẻ thường không
    for item in list_normal_card:
        if item[0].id == card_id_in:
            item_in = item
            break
    else:
        WriteLogRunning(case_id, f"Not exist card id {card_id_in} in normal card list ", "", False, False)
        return

    # kiểm tra id thẻ ra có nằm trong thẻ battle không
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

    # kiểm tra lại sau khi swap có đúng ko
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

    

def upgrade_card(case_id,card_id,level,n_frags,n_gold):
    # cheat thông số truyền vào
    card_ids = list(map(int,config_list_card.keys()))
    if card_id not in card_ids:
        WriteLogRunning(case_id, f"Card id error", "", False, False)
        return
    poco(HEADER_BTN_CHEAT).click()
    poco("gold_input").click()
    del_text()
    text(str(n_gold))
    poco("card_id_input").click()
    del_text()
    text(str(card_id))
    poco("card_level_input").click()
    del_text()
    text(str(level))
    poco("card_fragments_input").click()
    del_text()
    text(str(n_frags))

    poco(CHEAT_POPUP_BTN_SENT).click()
    if poco("resource_gold").offspring("value").get_text() != str(n_gold):
        WriteLogRunning(case_id, f"Can't cheat gold", "", False, False)
        return

    poco(NAV_BAR_BTN_CARD).click()

    list_battle_card = get_list_battle_card()
    list_normal_card = get_list_nomal_card()

    for item in list_battle_card:
        if item[0].id == card_id:
            find_item = item
            break

    for item in list_normal_card:
        if item[0].id == card_id:
            find_item = item
            break
    

    # nếu không tìm được card
    if "find_item" not in locals().keys():
        WriteLogRunning(case_id, f"can't find card", "", False, False)
        return
    

    # kiểm tra level sau khi cheat
    if find_item[1].child("<no-name>").offspring("level").get_text() != "Lv." + str(level):
        WriteLogRunning(case_id, f"error level card id {card_id}", "", False, False)
        return
    
    
    
    levels = list(map(int,config_card.keys()))


    if level >= max(levels):

        # số thẻ nâng cấp phải để max
        if find_item[1].child("card_progress_bar").offspring("text").get_text() != "MAX":
            WriteLogRunning(case_id, f"error frag card id {card_id}", "", False, False)
            return  

        find_item[1].click()

        if not poco("card_info_popup").exists():
            WriteLogRunning(case_id, f"not show card info popup card id {card_id}", "", False, False)
            return
        # không thể ấn vào nút nâng cấp
        poco("card_info_popup_btn_upgrade").click()
        sleep(0.5)
        if poco("card_info_popup").exists():
            poco("close_button").click()
            WriteLogRunning(case_id, f"upgrade card when card max level {card_id}", "", False, True)
            return
        else:
            WriteLogRunning(case_id, f"error upgrade card when card max level {card_id}", "", False, False)
            return
    else:
        # lấy config nâng cấp
        config_upgrade = config_card[str(level+1)]
        needed_frags = config_upgrade['fragments']
        needed_gold = config_upgrade["gold"]
        if find_item[1].child("card_progress_bar").offspring("text").get_text() != f"{n_frags}/{needed_frags}":
            WriteLogRunning(case_id, f"error frag card id {card_id}", "", False, False)
            return
        find_item[1].click()
        if not poco("card_info_popup").exists():
            WriteLogRunning(case_id, f"not show card info popup card id {card_id}", "", False, False)
            return
        poco("card_info_popup_btn_upgrade").click()

        # thiếu thẻ
        if n_frags < needed_frags:
            if not poco("notificationPanel").exists() or poco("notificationPanel").attr("visible") == False:
                WriteLogRunning(case_id, f"not show notification Panel card id {card_id}", "", False, False)
                return
            else:
                poco("close_button").click()
                WriteLogRunning(case_id,f"Upgrade when not enough frags card id {card_id}","",False,True)
                return
        else:
            # đủ thẻ thiếu vàng
            if n_gold < needed_gold:
                if not poco("notificationPanel").exists() or poco("notificationPanel").attr("visible") == False:
                    WriteLogRunning(case_id, f"not show notification Panel card id {card_id}", "", False, False)
                    return
                else:
                    poco("close_button").click()
                    WriteLogRunning(case_id,f"Upgrade when not enough gold card id {card_id}","",False,True)
                    return

            else:
                # đủ thẻ đủ vàng
                sleep(0.5)
                if poco("card_info_popup").exists():
                    WriteLogRunning(case_id, f"not show card info popup card id {card_id}", "", False, False)
                    return 
                if find_item[1].child("<no-name>").offspring("level").get_text() != f"Lv.{level+1}":
                    WriteLogRunning(case_id, f"upgrade error level {card_id}", "", False, False)
                    return 
                if level + 1 >= max(levels):
                    if find_item[1].child("card_progress_bar").offspring("text").get_text() != "MAX":
                        WriteLogRunning(case_id, f"error frag card id {card_id}", "", False, False)
                        return
                else:
                    remain_frag = n_frags-needed_frags
                    next_needed_frag = config_card[str(level+2)]["fragments"]
                    if find_item[1].child("card_progress_bar").offspring("text").get_text() != f"{remain_frag}/{next_needed_frag}":
                        WriteLogRunning(case_id, f"error frag card id {card_id}", "", False, False)
                        return
                
                WriteLogRunning(case_id,f"Upgrade succeed {card_id}","",False,True)
                return
                
    

                
                    

                

               



             
    

    
        


   
    




        






    







