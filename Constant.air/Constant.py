# -*- encoding=utf8 -*-
__author__ = "LinhDNA"

from airtest.core.api import *

auto_setup(__file__)

projectFolder = "D:\\LinhDNA\\Projects\\Git\\AutoSusun"
PKG = "com.zingplay.susun"    # Package name
APK = os.path.join(projectFolder, "Susun.apk")    # Apk name

startByOpening = False  # Start test từ step mở app
numViewedItems = 6 # Số item ném show cùng lúc
timeDelta = 60 # seconds, use in cheating time

ONE_HAND_MAX_TIME = 180 # seconds
API_PASS = 200 # Cheat success
COUNT_DOWN_TIME = 10 # Max time count down start game
SHOW_GUI_TIME = 2 # Max time show open GUI Effect

minGold = 1200000 # Min gold to play now

# ===================== Models Name =====================

USER_MODEL = "UProfileModel"
WC_MODEL = "event.weekly_challenge.UWeeklyChallengeModel"
FIRST_PAY_MODEL = "UFirstPayModel"
HC_MODEL = "event.home_coming.UHomeComingModel"

# ===================== Z Account Login =====================

passLogin = "123456"

# ===================== Cheat Admin Tool =====================

# CHEAT_TIME_VIP = "CHEAT_TIME_REMAIN_VIP"
# BUY_VIP = "CHEAT_PAYMENT_VIP"
# paramBuyVIP = "vip.pack_"

# BUY_GOLD_IAP = "CHEAT_PAYMENT_IAP"
# BUY_GOLD_LP = "CHEAT_LOCAL_PAYMENT"
# paramBuyIAP = "iap.pack_"
# paramBuyLP = "CCMX_"    # Element in Config PurchasePack.json

CHEAT_TIME = "CHEAT_SERVER_TIME"

# ===================== Config File Name =====================

VIP_JS = "VIP.json"
EXTRA_JS = "Extra.json"
EVENT_WC_JS = "EventWeeklyChallenge.json"
EVENT_HC_JS = "EventHomeComing.json"
PAYMENT_JS = "Payment.json"

# ===================== Popups Name =====================

DAILY_BONUS = "Daily Bonus"
GOLD_SUPPORT = "Gold Support"
ALMOST_EXPIRED_VIP = "Almost Expired VIP"
EXPIRED_VIP = "Expired VIP"
CLAIM_REWARD_NEW_USER = "Claim Reward New User" 
CLAIM_TRIBUTE_VIP = "Claim Tribute VIP" 
OFFER_CHEAP = "Offer Cheap" 
OFFER_WC = "Offer Weekly Challenge" 
TUTORIAL = "Turorial"
RANKING_REWARD = "Ranking Reward"
OFFER_1ST = "Offer 1st"
OFFER_NEW_USER = "Offer New User"

POPUP_EVENT_WC = "Popup Event WC"
EVENT_WC = "Event WC"
DEAL_WC = "Deal WC"

GOLD_SUPPORT = "Gold Support"
NOTI = "Notification"
JOIN_RANKING = "Join Ranking"
FINAL_RANING = "Final Raning"

NORMAL_OFFER_HC = "Popup Normal Deal Event HC"
NORMAL_OFFER_HC = "Popup Sale Deal Event HC"
WELCOME = "Welcome"

# ===================== Challenges =====================

PLAY_GAME = 0
WIN_IN_BOTTOM = 1
WIN_IN_MIDDLE = 2
WIN_IN_TOP = 3
CATCH_OTHER = 4
WIN_POINT = 5

# ===================== Event List =====================

EVENT_WEEKLY_CHALLENGE = "EventWC"
EVENT_HOME_COMING = "EventHC"
EVENT_BOARD_TRIP = "EventBT"

# ===================== Shop =====================

listPayment = ["SMS", "Wallet", "IAP"]
paymentType = ["SMS", "IAP", "Wallet"]
maxViewedPacks = 5

# ===================== Notifications =====================

NOT_ENOUGH_MONEY = "Not enough the min buy in,"
ENOUGH_MOVE_TO_GO_HOME = "Going Home now"
NOT_ENOUGH_MOVE_TO_GO_HOME = "You need at least"