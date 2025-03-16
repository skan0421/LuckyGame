import time
import pyautogui
from config import config

def main():
    # config.py에 저장된 UNIT_RANGE 영역 정보
    unit_region = config.REGIONS['UNIT_RANGE']
    offset_left = unit_region['left']
    offset_top = unit_region['top']

    # UNIT_CELL_CENTERS는 UNIT_RANGE 내부(로컬) 좌표입니다.
    # 절대 좌표는 영역의 offset을 더해 계산합니다.
    for i, center in enumerate(config.UNIT_CELL_CENTERS, start=1):
        abs_x = offset_left + center[0]
        abs_y = offset_top + center[1]
        print(f"{i}번 셀 클릭: 절대 좌표 ({abs_x}, {abs_y})")
        pyautogui.click(abs_x, abs_y)
        time.sleep(0.3)  # 1초 대기

if __name__ == '__main__':
    main()
