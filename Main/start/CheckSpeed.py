import pytesseract
import pyautogui
import time

from config import config

from util.util import find_image_on_screen
from Main.thread.ThreadManager import ThreadManager
from Main.thread import ChallengeThread, GetLegendThread, GameActionThread, BossClearThread

# Tesseract 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
ocr_config = '-l kor+eng --oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'


thread_manager = ThreadManager()


def start_all_threads():
    """
    필요한 스레드를 한 번에 시작합니다.
    """
    thread_manager.start_thread("ChallengeThread", ChallengeThread.boss_thread)
    thread_manager.start_thread("GetLegendThread", GetLegendThread.legend_thread)
    thread_manager.start_thread("GameActionThread", GameActionThread.action_thread)
    thread_manager.start_thread("BossClearThread", BossClearThread.clear_thread)


def check_speed_region(threshold=0.7):
    found_speed1 = find_image_on_screen(config.SPEED1_TEMPLATE, threshold=threshold)
    found_speed2 = find_image_on_screen(config.SPEED2_TEMPLATE, threshold=threshold)

    if found_speed1 is not None:
        print("speed1 템플릿 발견. 좌상단 좌표:", found_speed1)
        return "speed1"
    elif found_speed2 is not None:
        print("speed2 템플릿 발견. 좌상단 좌표:", found_speed2)
        return "speed2"
    else:
        print("speed 템플릿을 찾지 못했습니다.")
        return None


def main():
    while True:
        result = check_speed_region(threshold=0.7)
        if result == "speed1":
            speed_coord = config.SPEED
            if speed_coord:
                print("SPEED 클릭:", speed_coord)
                pyautogui.click(*speed_coord)
            else:
                print("SPEED 좌표 없음")
            break
        elif result == "speed2":
            print("speed2 감지 -> 그냥 진행")
            break
        else:
            print("재시도 중...")
            time.sleep(2)

    time.sleep(1)

    start_all_threads()
    print("모든 스레드 시작 완료")

if __name__ == "__main__":
    main()
    while True:
        time.sleep(1)
