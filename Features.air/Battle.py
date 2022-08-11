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
import enum
import random

config = ConfigReader()
configListCard: dict = config.getConfigByElement("ListCard.json", "listCard")
configTower: dict = config.getConfigByElement("Tower.json", "tower")
configSpell: dict = config.getConfigByElement("Potion.json","potion")

CARD_ID = "cardId_"
CARD_VIEW = "cardView_"
FIGHT_BUTTON = "fightButton"
PLAYER_LAYER = "player_layer"
OPPONENT_LAYER = "opponent_layer"
MAP_NODE = "mapNode"
MAP_NODE_UNDER_TREE = "mapNodeUnderTree"
MAP_NODE_UNDER_HOLE = "mapNodeUnderHole"
MAP_NODE_UNDER_HOME = "mapNodeUnderHome"
MAP_NODE_UNDER_ATTACK_SPEED = "mapNodeUnderAttackSpeed"
MAP_NODE_UNDER_DAMAGE = "mapNodeUnderDamage"
MAP_NODE_UNDER_RANGE = "mapNodeUnderRange"
BATTLE_NOTIFICATION = "battleNotification"
SURRENDER_BUTTON = "battle_btn_chat_1"
RETURN_BUTTON = "return_btn"
TOWER = "tower_"
MONSTER_PATH_NODE = "monsterPathNode"
TOWER_CHOOSE_TARGET = "chooseTarget"
SPELL_VIEW = "spellView"

auto_setup(__file__)
fName = "Battle"

class Obstacle(enum.Enum):
    tree = 0
    hole = 1
    home = 2

class Spell(enum.Enum):
    fireball = 0
    frozen = 1
    trap = 2

def runBattle(deviceId):
    try:
        ResetArrRs()
        for fn in getFunctionNeedTest(fName):
            print("Running: " + fn)
            eval(fn)
    except Exception as e:
        WriteLogCrash(e, fName)

def getCardId(cardView):
    cardIds = [int(id) for id in configListCard.keys()]
    for cardId in cardIds:
        if cardView.child(CARD_ID + str(cardId)).exists():
            return cardId
    return -1

def startBattle(caseId):
    if poco(FIGHT_BUTTON).exists():
        poco(FIGHT_BUTTON).click()
    else:
        WriteLogRunning(caseId, "Không tìm thấy nút chiến đấu", "", False, False)
        return False

    playerLayer = poco(PLAYER_LAYER)
    opponentLayer = poco(OPPONENT_LAYER)

    poco.wait_for_all([playerLayer, opponentLayer])
    sleep(4)
    return True

def quitBattle(caseId):
    if poco(SURRENDER_BUTTON).exists():
        poco(SURRENDER_BUTTON).click()

        backHomeButton = poco(RETURN_BUTTON)
        poco.wait_for_all([backHomeButton])
        backHomeButton.click()

        sleep(3)

def checkEnityInMap(caseId):
    startBattle(caseId)

    isFullEnity = True
    for player in [poco(PLAYER_LAYER), poco(OPPONENT_LAYER)]:
        if not player.child(MAP_NODE_UNDER_RANGE).exists():
            isFullEnity = False
            break
        else:
            holes = player.child(MAP_NODE_UNDER_RANGE)
            if len(holes) != 1:
                isFullEnity = False
                break
        if not player.child(MAP_NODE_UNDER_ATTACK_SPEED).exists():
            isFullEnity = False
            break
        else:
            holes = player.child(MAP_NODE_UNDER_ATTACK_SPEED)
            if len(holes) != 1:
                isFullEnity = False
                break
        if not player.child(MAP_NODE_UNDER_DAMAGE).exists():
            isFullEnity = False
            break
        else:
            holes = player.child(MAP_NODE_UNDER_DAMAGE)
            if len(holes) != 1:
                isFullEnity = False
                break
        if not player.child(MAP_NODE_UNDER_HOLE).exists():
            isFullEnity = False
            break
        else:
            holes = player.child(MAP_NODE_UNDER_HOLE)
            if len(holes) != 1:
                isFullEnity = False
                break
        if not player.child(MAP_NODE_UNDER_TREE).exists():
            isFullEnity = False
            break
        else:
            trees = player.child(MAP_NODE_UNDER_TREE)
            if len(trees) < 1 or len(trees) > 2:
                isFullEnity = False
                break
    if isFullEnity:
        WriteLogRunning(caseId, "Hiển thị các thành phần trong map (cây, hố, ô sức mạnh)", "", False, True)
    else:
        WriteLogRunning(caseId, "Hiển thị các thành phần trong map (cây, hố, ô sức mạnh)", "", False, False)

    quitBattle(caseId)


def checkEnergyCardView(caseId):
    if not startBattle(caseId):
        return

    for i in range(0, 4):
        cardView = poco(CARD_VIEW + str(i))
        cardId = getCardId(cardView)
        cardViewEnergy = int(cardView.child("cardViewEnergy").offspring("num_energy").get_text())
        isTrueEnergy = True
        if configListCard[str(cardId)]["type"] == "tower":
            if configTower[str(configListCard[str(cardId)]["id"])]["energy"] != cardViewEnergy:
                isTrueEnergy = False
        else:
            if configSpell[str(configListCard[str(cardId)]["id"])]["energy"] != cardViewEnergy:
                isTrueEnergy = False
    if isTrueEnergy:
        WriteLogRunning(caseId, "Hiển thị năng lượng của thẻ theo config", "", False, True)
    else:
        WriteLogRunning(caseId, "Hiển thị năng lượng của thẻ theo config", "", False, False)

    quitBattle(caseId)

def dropTower(goalNode):
    for i in range(0, 4):
        cardView = poco(CARD_VIEW + str(i))
        cardId = getCardId(cardView)
        if configListCard[str(cardId)]["type"] == "tower":
            cardView.drag_to(goalNode)
            return cardId

def dropTowerOnObstacleTile(caseId, type):
    if not startBattle(caseId):
        return

    playerLayer = poco(PLAYER_LAYER)

    goalNode = None
    nodes = None
    typeName = ""

    if type == Obstacle.tree.value:
        nodes = playerLayer.child(MAP_NODE_UNDER_TREE)
        typeName = "cây"
    elif type == Obstacle.hole.value:
        nodes = playerLayer.child(MAP_NODE_UNDER_HOLE)
        typeName = "hố"
    elif type == Obstacle.home.value:
        nodes = playerLayer.child(MAP_NODE_UNDER_HOME)
        typeName = "nhà chính"

    index = random.randint(0, len(nodes) - 1)
    goalNode = nodes[index]

    dropTower(goalNode)

    sleep(0.2)

    battleNotification = poco(BATTLE_NOTIFICATION)
    if battleNotification.attr("visible") == False:
        WriteLogRunning(caseId, "Đặt trụ lên chướng ngại vật %s" %typeName, "", False, False)
    else:
        WriteLogRunning(caseId, "Đặt trụ lên chướng ngại vật %s" %typeName, "", False, True)

    quitBattle(caseId)

def dropTowerOnNormalTile(caseId, isMonsterPath = False):
    if not startBattle(caseId):
        return

    playerLayer = poco(PLAYER_LAYER)

    if isMonsterPath:
        if poco(MONSTER_PATH_NODE).exists():
            monsterPath = poco(MONSTER_PATH_NODE)
            index = random.randint(0, len(monsterPath) - 1)

            energyBar = poco("energy_bar")
            oldEnergy = int(energyBar.child("energy").offspring("num_energy").get_text())

            cardId = dropTower(monsterPath[index])

            cardEnergy = None

            if configListCard[str(cardId)]["type"] == "tower":
                cardEnergy = configTower[str(configListCard[str(cardId)]["id"])]["energy"]
            else:
                cardEnergy = configSpell[str(configListCard[str(cardId)]["id"])]["energy"]

            sleep(2)

            if playerLayer.child(TOWER + str(cardId)).exists():
                if playerLayer.child(TOWER + str(cardId)).get_position() == monsterPath[index].get_position():
                    if poco(MONSTER_PATH_NODE).exists():
                        newMonsterPath = poco(MONSTER_PATH_NODE)
                        hasUpdatedMonsterPath = True
                        for node in newMonsterPath:
                            if node.get_position() == monsterPath[index].get_position():
                                hasUpdatedMonsterPath = False
                                break
                        if hasUpdatedMonsterPath:
                            if oldEnergy - cardEnergy == int(energyBar.child("energy").offspring("num_energy").get_text()):
                                WriteLogRunning(caseId, "Đặt trụ lên ô trống là đường đi của quái", "", False, True)
                            else:
                                WriteLogRunning(caseId, "Đặt trụ lên ô trống là đường đi của quái, trừ năng lượng sai", "", False, True)
                        else:
                            WriteLogRunning(caseId, "Đặt trụ lên ô trống là đường đi của quái, không update đường đi", "", False, False)
                    else:
                        WriteLogRunning(caseId, "Đặt trụ lên ô trống là đường đi của quái, không có UI đường đi của quái", "", False, False)
                else:
                    WriteLogRunning(caseId, "Đặt trụ lên ô trống là đường đi của quái, vị trí xây trụ khác với vị trí đặt trụ", "", False, False)
            else:
                WriteLogRunning(caseId, "Đặt trụ lên ô trống là đường đi của quái", "", False, False)
        else:
            WriteLogRunning(caseId, "Đặt trụ lên ô trống là đường đi của quái, không có UI đường đi của quái", "", False, False)
    else:
        nodes = playerLayer.child(MAP_NODE)
        monsterPath = poco(MONSTER_PATH_NODE)
        tmp = []

        for node in nodes:
            isMonsterPathNode = False
            for monsterPathNode in monsterPath:
                if node.get_position() == monsterPathNode.get_position():
                    isMonsterPathNode = True
            if not isMonsterPathNode:
                tmp.append(node)

        nodes = tmp
        index = random.randint(0, len(nodes) - 1)

        energyBar = poco("energy_bar")
        oldEnergy = int(energyBar.child("energy").offspring("num_energy").get_text())

        cardId = dropTower(nodes[index])

        cardEnergy = None
        if configListCard[str(cardId)]["type"] == "tower":
            cardEnergy = configTower[str(configListCard[str(cardId)]["id"])]["energy"]
        else:
            cardEnergy = configSpell[str(configListCard[str(cardId)]["id"])]["energy"]

        sleep(2)

        if playerLayer.child(TOWER + str(cardId)).exists():
            if playerLayer.child(TOWER + str(cardId)).get_position() == nodes[index].get_position():
                if oldEnergy - cardEnergy == int(energyBar.child("energy").offspring("num_energy").get_text()):
                    WriteLogRunning(caseId, "Đặt trụ lên ô trống không phải đường đi của quái", "", False, True)
                else:
                    WriteLogRunning(caseId, "Đặt trụ lên ô trống không phải đường đi của quái, trừ năng lượng sai", "", False, True)
            else:
                WriteLogRunning(caseId, "Đặt trụ lên ô trống không phải đường đi của quái, vị trí xây trụ khác với vị trí đặt trụ", "", False, False)
        else:
            WriteLogRunning(caseId, "Đặt trụ lên ô trống không phải đường đi của quái", "", False, False)


    quitBattle(caseId)

def cancelTower(caseId):
    if not startBattle(caseId):
        return

    playerLayer = poco(PLAYER_LAYER)

    nodes = playerLayer.child(MAP_NODE)
    monsterPath = poco(MONSTER_PATH_NODE)
    tmp = []

    for node in nodes:
        isMonsterPathNode = False
        for monsterPathNode in monsterPath:
            if node.get_position() == monsterPathNode.get_position():
                isMonsterPathNode = True
        if not isMonsterPathNode:
            tmp.append(node)

    nodes = tmp
    index = random.randint(0, len(nodes) - 1)

    cardId = dropTower(nodes[index])

    sleep(2)

    if playerLayer.child(TOWER + str(cardId)).exists():
        tower = playerLayer.child(TOWER + str(cardId))
        tower.click()
        if poco(TOWER_CHOOSE_TARGET).offspring("remove").exists():
            poco(TOWER_CHOOSE_TARGET).offspring("remove").click()
            sleep(1)
            if playerLayer.child(TOWER + str(cardId)).exists():
                WriteLogRunning(caseId, "Huỷ trụ, trụ không biến mất", "", False, False)
            else:
                WriteLogRunning(caseId, "Huỷ trụ", "", False, True)
        else:
            WriteLogRunning(caseId, "Huỷ trụ, không có nút huỷ trụ", "", False, False)
    else:
        WriteLogRunning(caseId, "Huỷ trụ, xây trụ không thành công", "", False, False)

    quitBattle(caseId)

def isExistCardWithId(id):
    for i in range(0, 4):
        cardView = poco(CARD_VIEW + str(i))
        cardId = getCardId(cardView)
        if configListCard[str(cardId)]["type"] == "spell":
            if int(configListCard[str(cardId)]["id"]) == id:
                return True
    return False

def dropSpellCard(caseId, id, isOpponentLayer = False):
    startBattle(caseId)

    layer = None
    if isOpponentLayer:
        layer = poco(OPPONENT_LAYER)
    else:
        layer = poco(PLAYER_LAYER)

    isFirstClick = True

    while not isExistCardWithId(id):
        cardView = poco(CARD_VIEW + str(0))
        if isFirstClick:
            cardView.click()
            isFirstClick = False
        sleep(0.5)
        if cardView.offspring("removeButton").exists():
            cardView.offspring("removeButton").click()
            sleep(0.5)
        else:
            WriteLogRunning(caseId, "Thả thẻ phép", "", False, False)
            break

    for i in range(0, 4):
        cardView = poco(CARD_VIEW + str(i))
        cardId = getCardId(cardView)
        if configListCard[str(cardId)]["type"] == "spell":
            if int(configListCard[str(cardId)]["id"]) == id:
                nodes = layer.child(MAP_NODE)
                index = random.randint(0, len(nodes) - 1)
                cardView.drag_to(nodes[index])
                if not(isOpponentLayer and not poco(SPELL_VIEW)) or (not isOpponentLayer and poco(SPELL_VIEW)):
                    WriteLogRunning(caseId, "Thả thẻ phép", "", False, True)
                else:
                    WriteLogRunning(caseId, "Thả thẻ phép", "", False, False)

    quitBattle(caseId)