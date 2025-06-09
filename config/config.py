# config.py (자동 생성)
import os

GAME_STATED = False
# ─── 프로젝트 루트 & 이미지 폴더 경로 ────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UNIT_IMAGE_DIR = os.path.join(BASE_DIR, "config", "unit_image")

# ─── StartGame.py 에서 사용 ──────────────────────────────────────────
MAIN_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "main.png")
BUY_ENERGY_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "buy_energy.png")

# ─── CheckSpeed 스크립트에서 사용 ────────────────────────────────────
SPEED1_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "speed1.png")
SPEED2_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "speed2.png")
SPEED = (3030, 827)
# ─── BossClearThread 에서 사용 ──────────────────────────────────────
BOSS_CLEAR_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "bossClear.png")
# 보상 선택
BOSS_CLEAR_POS1 = (3050, 463)
# 보상 받기
BOSS_CLEAR_POS2 = (2879, 735)

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
BOSS_CHALLENGE_CHECK_POS = (2863, 645)
# 땅바닥
BOSS_CHALLENGE_CLOSE_POS = (3092, 472)

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
MORE_REWARD_TEMPLATE = os.path.join(UNIT_IMAGE_DIR, "more_reward.png")
GO_LOBBY = (2977, 920)
ReGame = ()
GAME_STARTED = False


# GameFunctions
summon_button_template = os.path.join(UNIT_IMAGE_DIR, "summon.png")
empty_template_path1 = os.path.join(UNIT_IMAGE_DIR, "emptyCell1.png")
empty_template_path2 = os.path.join(UNIT_IMAGE_DIR, "emptyCell2.png")
closeRoulette = (3080, 726)
closeEnhance = (11, 11)
heroRoulette = (2862, 843)
epicRoulette = (2991, 846)

REGION_CENTERS = {
    'BUY_ENERGY': (2972, 617),
    'BUY_ENERGY_SURE': (2861, 669),
    'CB_BUY_ENERGY': (3092, 369),
    'START': (2863, 847),
}

UNIT_CELL_CENTERS = {
    1: (2691, 533),
    2: (2759, 533),
    3: (2827, 533),
    4: (2896, 533),
    5: (2964, 533),
    6: (3032, 533),
    7: (2691, 590),
    8: (2759, 590),
    9: (2827, 590),
    10: (2896, 590),
    11: (2964, 590),
    12: (3032, 590),
    13: (2691, 637),
    14: (2759, 637),
    15: (2827, 637),
    16: (2896, 637),
    17: (2964, 637),
    18: (3032, 637),
}
SELL_CENTERS = {
    1: (2710, 471),
    2: (2759, 471),
    3: (2827, 471),
    4: (2896, 471),
    5: (2964, 471),
    6: (3032, 471),
    7: (2691, 525),
    8: (2759, 525),
    9: (2827, 525),
    10: (2896, 525),
    11: (2964, 525),
    12: (3032, 525),
    13: (2691, 579),
    14: (2759, 579),
    15: (2827, 579),
    16: (2896, 579),
    17: (2964, 579),
    18: (3032, 579),
}

SYNTHESIS_CENTERS = {
    1: (2691, 607),
    2: (2759, 607),
    3: (2827, 607),
    4: (2896, 607),
    5: (2964, 607),
    6: (3032, 607),
    7: (2663, 678),
    8: (2759, 678),
    9: (2827, 678),
    10: (2896, 678),
    11: (2964, 678),
    12: (3032, 678),
    13: (2691, 712),
    14: (2759, 712),
    15: (2827, 712),
    16: (2896, 712),
    17: (2964, 712),
    18: (3032, 712),
}

DUNGEON = {
    1: (2730, 331),
    2: (2705, 367),
    3: (2728, 406),
}

REGIONS = {
    # 'ENERGY': {'left': 2898, 'top': 33, 'width': 122, 'height': 39},
    'BUY_ENERGY': {'left': 2870, 'top': 594, 'width': 204, 'height': 46},
    # 'BUY_ENERGY_SURE': {'left': 2750, 'top': 631, 'width': 223, 'height': 76},
    # 'CB_BUY_ENERGY': {'left': 3073, 'top': 352, 'width': 39, 'height': 34},
    # 'START': {'left': 2748, 'top': 796, 'width': 231, 'height': 103},
    # 'ROUND': {'left': 2881, 'top': 61, 'width': 29, 'height': 19},
    # 'SPEED': {'left': 3051, 'top': 796, 'width': 57, 'height': 52},
    # 'GET_UNIT': {'left': 2763, 'top': 859, 'width': 199, 'height': 91},
    # 'GET_BOSS': {'left': 3039, 'top': 230, 'width': 76, 'height': 78},
    # 'UPGRADE': {'left': 2763, 'top': 973, 'width': 198, 'height': 43},
    # 'CB_UPGRADE': {'left': 3090, 'top': 712, 'width': 41, 'height': 32},
    # 'GET_LUCKY': {'left': 3009, 'top': 874, 'width': 85, 'height': 69},
    # 'GET_LUCKY_MIDDLE': {'left': 2810, 'top': 897, 'width': 105, 'height': 38},
    # 'CLOSE_LUCKY': {'left': 3057, 'top': 697, 'width': 45, 'height': 41},
    # 'UPGRADE_LUCKY': {'left': 2999, 'top': 763, 'width': 115, 'height': 171},
    # 'LEGEND_AREA': {'left': 2640, 'top': 194, 'width': 110, 'height': 300},
    # 'UNIT_RANGE': {'left': 2658, 'top': 497, 'width': 408, 'height': 168},
    # 'POPULATION': {'left': 2790, 'top': 701, 'width': 60, 'height': 31},
    # 'REAL_POPULATION': {'left': 2886, 'top': 704, 'width': 32, 'height': 23},
    'BOSS_CHALLENGE': {'left': 3009, 'top': 103, 'width': 330, 'height': 400},
    # 'BOSS_CHALLENGE_CHECK': {'left': 2759, 'top': 604, 'width': 207, 'height': 83},
    # 'GO_LOBBY': {'left': 2871, 'top': 881, 'width': 212, 'height': 78},
    'UNIT_CHECK': {'left': 2609, 'top': 43, 'width': 156, 'height': 203},
    # 'UNIT_NAME': {'left': 2642, 'top': 167, 'width': 88, 'height': 22},
    # 'MATCH_FAILED_CHECK': {'left': 2758, 'top': 618, 'width': 207, 'height': 78},
    'legendEnforce': {'left': 2879, 'top': 896, 'width': 98, 'height': 37},
    'luckyEnforce': {'left': 3008, 'top': 895, 'width': 98, 'height': 35},
    'enforceClose': {'left': 3088, 'top': 719, 'width': 41, 'height': 32},
}

UNIT_CELL_STATUS = [False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                    False, False, False, False]
