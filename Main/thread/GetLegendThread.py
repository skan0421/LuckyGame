import os

import cv2
import numpy as np
import pyautogui
import time
import threading

from config import config
from util.util import find_image_on_screen


def click_legend_area(threshold=0.8):
    """
    전설 룰렛(legend) 감지 및 셀 상태 업데이트
    - config.LEGEND_A_TEMPLATE, config.LEGEND_C_TEMPLATE 사용
    - 찾으면 해당 셀 인덱스 리스트만큼 상태를 False로 변경
    """
    # config.py에 정의된 템플릿-셀 매핑 사용
    for tpl_path, cell_list in config.LEGEND_TEMPLATES.items():
        loc = find_image_on_screen(tpl_path, threshold=threshold)
        if not loc:
            continue

        # 템플릿 크기 읽어서 클릭 중앙 계산
        x, y = loc
        template_img = cv2.imread(tpl_path, cv2.IMREAD_GRAYSCALE)
        h, w = template_img.shape
        center_x = x + w // 2
        center_y = y + h // 2
        # threshold 점수도 확인
        screen_img = pyautogui.screenshot(region=(loc[0], loc[1], w, h))
        screen_img = cv2.cvtColor(np.array(screen_img), cv2.COLOR_RGB2GRAY)
        template = cv2.imread(tpl_path, cv2.IMREAD_GRAYSCALE)
        res = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        print(f"🎯 매칭 성공: {os.path.basename(tpl_path)} @ ({center_x}, {center_y}), 점수={max_val}")

        print(f"템플릿 '{os.path.basename(tpl_path)}' 발견 → 클릭 ({center_x}, {center_y})")
        pyautogui.click(center_x, center_y)
        time.sleep(1)

        # 매칭된 셀들 상태 업데이트
        for idx in cell_list:
            config.UNIT_CELL_STATUS[idx - 1] = False
            print(f"[유닛 상태 업데이트] 셀 {idx} → False")
        break  # 한 번 찾으면 루프 탈출


def legend_thread(stop_event):
    """
    전설 룰렛 감시 스레드
    - stop_event가 set되면 종료
    """
    print("[legend_thread] ● 시작")
    while not stop_event.is_set():
        click_legend_area(threshold=0.7)
        time.sleep(1)
    print("[legend_thread] ✖ 종료")


if __name__ == "__main__":
    stop_event = threading.Event()
    t = threading.Thread(target=legend_thread, args=(stop_event,), daemon=True)
    t.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        print("테스트 중지")
