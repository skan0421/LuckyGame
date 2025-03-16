import cv2
import numpy as np
import mss
import pyautogui
import time
import threading

from config import config


def click_boss_area(threshold=0.7):
    boss_challenge = config.REGIONS['BOSS_CHALLENGE']
    with mss.mss() as sct:
        sct_img = sct.grab(boss_challenge)
        img = np.array(sct_img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    # config_center.BOSS_TEMPLATES에서 일괄 처리
    for key, tpl_path in config.BOSS_TEMPLATES.items():
        template = cv2.imread(tpl_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print(f"{key}: 템플릿 로드 실패({tpl_path})")
            continue

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val >= threshold:
            h, w = template.shape
            abs_x = boss_challenge['left'] + max_loc[0] + w // 2
            abs_y = boss_challenge['top'] + max_loc[1] + h // 2
            print(f"{key} 발견 → 클릭 ({abs_x}, {abs_y})")
            pyautogui.click(abs_x, abs_y)
            time.sleep(0.5)

            # 확인 버튼 클릭
            print(f"'BOSS_CHALLENGE_CHECK' 클릭 {config.BOSS_CHALLENGE_CHECK_POS}")
            pyautogui.click(*config.BOSS_CHALLENGE_CHECK_POS)
            time.sleep(0.5)

            # 팝업 닫기 버튼 클릭(땅바닥)
            print(f"'BOSS_CHALLENGE_CLOSE' 클릭 {config.BOSS_CHALLENGE_CLOSE_POS}")
            pyautogui.click(*config.BOSS_CHALLENGE_CLOSE_POS)
            time.sleep(5)
            break


def boss_thread(stop_event):
    print("[boss_thread] ● 시작")
    while not stop_event.is_set():
        click_boss_area(threshold=0.7)
        time.sleep(1)
    print("[boss_thread] ✖ 종료")


if __name__ == '__main__':
    stop_event = threading.Event()
    t = threading.Thread(target=boss_thread, args=(stop_event,), daemon=True)
    t.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        print("테스트 종료")
