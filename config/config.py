# config.py (자동 생성)
import os
GAME_STARTED = False
# ─── 프로젝트 루트 & 이미지 폴더 경로 ────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UNIT_IMAGE_DIR = os.path.join(BASE_DIR, "config", "unit_image")

# ─── StartGame.py 에서 사용 ──────────────────────────────────────────
MAIN_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "main.png")
BUY_ENERGY_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "buy_energy.png")

# ─── CheckSpeed 스크립트에서 사용 ────────────────────────────────────
SPEED1_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "speed1.png")
SPEED2_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "speed2.png")
SPEED = (1103, 817)
# ─── BossClearThread 에서 사용 ──────────────────────────────────────
BOSS_CLEAR_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "bossClear.png")
# 보상 선택
BOSS_CLEAR_POS1 = (1099, 448)
# 보상 받기
BOSS_CLEAR_POS2 = (939, 728)

# ─── BossChallenge 스크립트에서 사용할 보스 목록 템플릿 & 버튼 좌표 ───
BOSS_TEMPLATES = {
    "bossA": os.path.join(UNIT_IMAGE_DIR, "bossA.png"),
    "bossB": os.path.join(UNIT_IMAGE_DIR, "bossB.png"),
    "bossC": os.path.join(UNIT_IMAGE_DIR, "bossC.png"),
    "bossD": os.path.join(UNIT_IMAGE_DIR, "bossD.png"),
    "bossE": os.path.join(UNIT_IMAGE_DIR, "bossE.png"),
    "bossF": os.path.join(UNIT_IMAGE_DIR, "bossF.png"),
}

# 보스 챌린지 후 확인 버튼 & 팝업 닫기 버튼 좌표
# 보스 소환
BOSS_CHALLENGE_CHECK_POS = (941, 636)
# 땅바닥
BOSS_CHALLENGE_CLOSE_POS = (1166, 468)

# GetLegendThread
LEGEND_A_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "get_legendA.png")
LEGEND_C_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "get_legendC.png")
LEGEND_TEMPLATES = {
    LEGEND_A_TEMPLATE: [14, 16, 18],
    LEGEND_C_TEMPLATE: [4, 15, 17],
}

# GameStateThread
# ─── 스크립트에서 실제로 사용 중인 이미지 템플릿 경로 ────────────────────────
ERROR_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "matchingfailed.png")
GAME_END_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "GameEnd.png")
PACKAGE_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "package.png")
CLOSE_PACKAGE_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "back.png")
MORE_REWARD_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "moreReward.png")
GO_LOBBY = (1050, 911)
REGAME = (829,908)


#GameFunctions
summon_button_template = os.path.join(UNIT_IMAGE_DIR, "summon.png")
empty_template_path1 = os.path.join(UNIT_IMAGE_DIR, "emptyCell1.png")
empty_template_path2 = os.path.join(UNIT_IMAGE_DIR, "emptyCell2.png")
closeRoulette = (1148, 710)
closeEnhance = (1178,722)
heroRoulette = (936, 837)
epicRoulette = (1067, 830)
luckyEnforce = (1131, 897)
legendEnforce = (1010, 897)
roulette = (1123,896)
enforce = (944,980)

REGION_CENTERS = {
    'BUY_ENERGY': (891, 65),
    'BUY_ENERGY_SURE': (1049, 530),
    'CB_BUY_ENERGY': (944, 667),
    'START': (949, 838),
}

UNIT_DRAG_CELL = {
    1: (778, 524),
    2: (842, 524),
    3: (906, 524),
    4: (964, 524),
    5: (1031, 524),
    6: (1100, 524),
    7:  (778,  571),
    8:  (842,  571),
    9:  (906,  571),
    10: (964,  571),
    11: (1031, 571),
    12: (1100, 571),
    13: (778, 628),
    14: (842, 628),
    15: (906, 628),
    16: (964, 628),
    17: (1031, 628),
    18: (1100, 628),
}


UNIT_CELL_CENTERS = {
    1: (802, 487),
    2: (863, 487),
    3: (924, 487),
    4: (985, 487),
    5: (1046, 487),
    6: (1106, 487),
    7:  (802,  540),
    8:  (863,  540),
    9:  (924,  540),
    10: (985,  540),
    11: (1046, 540),
    12: (1106, 540),
    13: (778, 591),
    14: (844, 591),
    15: (904, 591),
    16: (965, 591),
    17: (1038, 591),
    18: (1099, 591),
}
SELL_CENTERS = {
    1: (800,  467),
    2: (844,  467),
    3: (904,  467),
    4: (965,  467),
    5: (1038, 467),
    6: (1099, 467),
    7:  (778,  519),
    8:  (844,  519),
    9:  (904,  519),
    10: (965,  519),
    11: (1038, 519),
    12: (1099, 519),
    13: (778,  568),
    14: (844,  568),
    15: (904,  568),
    16: (965,  568),
    17: (1038, 568),
    18: (1099, 568),
}

SYNTHESIS_CENTERS = {
    1: (778,  598),
    2: (844,  598),
    3: (904,  598),
    4: (965,  598),
    5: (1038, 598),
    6: (1099, 598),
    7:  (778, 647),
    8:  (844, 647),
    9:  (904, 647),
    10: (965,  647),
    11: (1038, 647),
    12: (1099, 647),
    13: (778,  701),
    14: (844,  701),
    15: (904,  701),
    16: (965,  701),
    17: (1038, 701),
    18: (1099, 701),
}


REGIONS = {
    'BUY_ENERGY': {'left': 1030, 'top': 595, 'width': 68, 'height': 31},
    'UNIT_CHECK': {'left': 698, 'top': 60, 'width': 127, 'height': 179},
    'BOSS_CHALLENGE': {'left': 1096, 'top': 220, 'width': 110, 'height': 114},
    # 'legendEnforce': {'left': 2879, 'top': 896, 'width': 98, 'height': 37},
    # 'luckyEnforce': {'left': 3008, 'top': 895, 'width': 98, 'height': 35},
    # 'enforceClose': {'left': 3088, 'top': 719, 'width': 41, 'height': 32},
}

UNIT_CELL_STATUS = [False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                    False, False, False, False]
