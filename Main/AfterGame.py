import cv2
import numpy as np
import mss
import pytesseract
import pyautogui
import time
from config import config, config_center
from util.util import find_image_on_screen  # util.py에서 템플릿 매칭 함수 불러오기

# Tesseract 실행 파일 경로 지정 (설치된 경로에 맞게 수정)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ocr_config = '-l kor+eng --oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'


# 1. 2배 체크
def check_speed_region(threshold=0.8):
    """
    config.py의 'SPEED' 영역을 캡쳐한 후,
    speed1.png와 speed2.png 템플릿과 비교하여 어느 템플릿과 유사한지 판별합니다.

    반환:
      "speed1" -> speed1.png와 유사 (임계값 이상)
      "speed2" -> speed2.png와 유사 (임계값 이상)
      None -> 어느 템플릿과도 유사하지 않음
    """
    speed_region = config.REGIONS['SPEED']
    with mss.mss() as sct:
        sct_img = sct.grab(speed_region)
        img = np.array(sct_img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    # 템플릿 이미지 경로 (절대 경로 사용)
    speed1_path = r"C:/Users/user/Desktop/LuckyG/config/unit_image/speed1.png"
    speed2_path = r"C:/Users/user/Desktop/LuckyG/config/unit_image/speed2.png"

    speed1_template = cv2.imread(speed1_path, cv2.IMREAD_GRAYSCALE)
    if speed1_template is None:
        print("speed1.png 템플릿 이미지를 로드할 수 없습니다.")
        return None

    speed2_template = cv2.imread(speed2_path, cv2.IMREAD_GRAYSCALE)
    if speed2_template is None:
        print("speed2.png 템플릿 이미지를 로드할 수 없습니다.")
        return None

    res1 = cv2.matchTemplate(img_gray, speed1_template, cv2.TM_CCOEFF_NORMED)
    res2 = cv2.matchTemplate(img_gray, speed2_template, cv2.TM_CCOEFF_NORMED)

    _, max_val1, _, _ = cv2.minMaxLoc(res1)
    _, max_val2, _, _ = cv2.minMaxLoc(res2)

    print("speed1 매칭 점수:", max_val1)
    print("speed2 매칭 점수:", max_val2)

    if max_val1 >= threshold:
        return "speed1"
    elif max_val2 >= threshold:
        return "speed2"
    else:
        return None

def main():
    result = check_speed_region(threshold=0.9)
    if result == "speed1":
        new_speed_coord = config_center.REGION_CENTERS.get('SPEED')
        if new_speed_coord is not None:
            x, y = new_speed_coord
            print("speed1 템플릿과 일치. 새로운 SPEED 좌표 클릭:", (x, y))
            pyautogui.click(x, y)
        else:
            print("config_center에 'SPEED' 좌표가 없습니다.")
    elif result == "speed2":
        print("speed2 템플릿과 일치. 아무 동작 없이 진행합니다.")
    else:
        print("SPEED 영역에서 유효한 템플릿을 찾지 못했습니다.")

if __name__ == "__main__":
    main()
