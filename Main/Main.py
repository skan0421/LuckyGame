import time               # time 모듈: 일정 시간 대기할 때 사용
import pyautogui         # pyautogui: 마우스/키보드 자동화 라이브러리
from config import config_center
import cv2                # OpenCV: 이미지 처리 라이브러리
import numpy as np        # NumPy: 배열 처리를 위한 라이브러리
import mss                # mss: 화면 캡쳐 라이브러리
import pytesseract        # pytesseract: OCR(광학 문자 인식) 라이브러리
# ↑ config 폴더 내 config_center.py를 import

def click_sell():
    """
    이 함수는 1번부터 18번까지 각 셀의 SELL_CENTERS 좌표를 순차적으로 클릭합니다.

    1) for i in range(1, 19):
       - i를 1부터 18까지 순회
    2) x, y = config_center.SELL_CENTERS[i]
       - config_center.py의 SELL_CENTERS 딕셔너리에서 i번째 셀의 중앙 좌표를 가져옴
    3) pyautogui.click(x, y)
       - 해당 좌표를 마우스로 클릭
    4) time.sleep(1)
       - 1초간 대기
    """
    for i in range(1, 19):
        x, y = config_center.SELL_CENTERS[i]
        print(f"[SELL] {i}번 셀 중앙 클릭: ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(0.3)

def click_synthesis():
    """
    이 함수는 1번부터 18번까지 각 셀의 SYNTHESIS_CENTERS 좌표를 순차적으로 클릭합니다.

    동작 방식은 click_sell()과 동일하며,
    이번에는 config_center.SYNTHESIS_CENTERS를 사용합니다.
    """
    for i in range(1, 19):
        x, y = config_center.SYNTHESIS_CENTERS[i]
        print(f"[SYNTHESIS] {i}번 셀 중앙 클릭: ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(0.3)

def click_unit():
    """
    이 함수는 1번부터 18번까지 각 셀의 UNIT_CELL_CENTERS 좌표를 순차적으로 클릭합니다.

    동작 방식은 click_sell()과 동일하며,
    이번에는 config_center.UNIT_CELL_CENTERS 사용합니다.
    """
    for i in range(1, 19):
        x, y = config_center.UNIT_CELL_CENTERS[i]
        print(f"[UNIT_CELL_CENTERS] {i}번 셀 중앙 클릭: ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(0.3)


def click_unit_synthesis():

    for i in range(1, 19):
        unit_x, unit_y = config_center.UNIT_CELL_CENTERS[i]
        syn_x, syn_y = config_center.SYNTHESIS_CENTERS[i]
        pyautogui.click(unit_x, unit_y)
        pyautogui.click(syn_x, syn_y)
        time.sleep(0.5)


def capture_text_from_region(region):
    """
    주어진 영역(region)을 캡쳐한 후, OCR을 사용해 텍스트를 추출하는 함수.

    매개변수:
      region: {'left': 값, 'top': 값, 'width': 값, 'height': 값} 형식의 딕셔너리.

    반환:
      캡쳐된 이미지에서 추출한 텍스트 (문자열).
    """
    # mss를 사용하여 지정한 영역을 캡쳐합니다.
    with mss.mss() as sct:
        sct_img = sct.grab(region)  # 영역 캡쳐 (이미지는 BGRA 형식)
        img = np.array(sct_img)     # NumPy 배열로 변환
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # OpenCV 표준인 BGR로 변환
    # 그레이스케일 이미지로 변환 (OCR 성능 향상을 위해)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 이진화 처리 (임계값 150, 최대값 255)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # pytesseract를 이용하여 OCR 수행
    # '--psm 7' 옵션은 이미지가 한 줄의 텍스트라고 가정
    text = pytesseract.image_to_string(thresh, config='--psm 7')
    return text.strip()  # 추출한 텍스트에서 양쪽 공백 및 줄바꿈 제거 후 반환

def main():
    """
    메인 함수:
    1) SELL_CENTERS 좌표를 순차적으로 클릭
    2) SYNTHESIS_CENTERS 좌표를 순차적으로 클릭
    """
    print("===== UNIT 클릭 시작 =====")
    # click_unit()

    print("===== SYNTHESIS 클릭 시작 =====")
    # click_unit_synthesis()

    print("===== UNIT 클릭 시작 =====")
    # click_unit()

    print("===== SELL 클릭 시작 =====")
    # click_sell()


    print("===== UNIT 클릭 시작 =====")
    # click_unit()

    # 2. 캡쳐할 영역 지정 (UNIT_NAME 영역 예시 값)
    unit_name_region = {'left': 2642, 'top': 64, 'width': 88, 'height': 22}

    # 3. 지정된 영역을 캡쳐하고 OCR을 통해 텍스트 추출
    extracted_text = capture_text_from_region(unit_name_region)
    print("추출된 텍스트:", extracted_text)
    # 4. 추출된 텍스트를 배열(리스트)에 저장
    text_array = [extracted_text]
    print("텍스트 배열:", text_array)




# 파이썬에서는 아래와 같이 작성하면, 이 스크립트를 직접 실행했을 때만 main()을 호출함.
# 다른 모듈에서 import하면 실행되지 않음.
if __name__ == "__main__":
    main()
