# -*- encoding=utf8 -*-
__author__ = "LinhDNA"

from airtest.core.api import *
from poco.drivers.cocosjs import CocosJsPoco

auto_setup(__file__)
poco = CocosJsPoco()

# Battle
FIGHT_BTN = Template(r"tpl1659674195465.png", record_pos=(-0.001, 0.302), resolution=(900, 1600))