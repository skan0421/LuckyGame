import cv2                # OpenCV: 이미지 처리 라이브러리
import numpy as np        # NumPy: 배열 처리를 위한 라이브러리
import mss                # mss: 화면 캡쳐 라이브러리
import pytesseract        # pytesseract: OCR(광학 문자 인식) 라이브러리
import time               # time 모듈: 대기를 위해 사용
from config import config



# 필요 시 Tesseract 실행 파일 경로를 지정 (설치된 경로에 맞게 수정)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
configTesseract = ('-l kor+eng --oem 3 --psm 6')
expected_list = config.expected_unit_names

def match_expected(text, expected_list):
    """
    OCR 결과 text와 예상 문자열 목록을 비교하여 가장 유사한 문자열을 반환합니다.
    (여기서는 간단히 text가 예상 문자열 중 포함되어 있으면 해당 문자열 반환하는 방식)
    """
    for expected in expected_list:
        if expected.lower() in text.lower():
            return expected
    return f"미등록 유닛: {text}"



def capture_text_from_region(region):
    """
    주어진 영역(region)을 캡쳐한 후, OCR을 이용해 텍스트를 추출하는 함수입니다.

    매개변수:
      region: {'left': 값, 'top': 값, 'width': 값, 'height': 값} 형태의 딕셔너리.

    반환:
      추출된 텍스트 (문자열, 양쪽 공백 및 줄바꿈 제거)
    """
    # mss를 사용하여 지정한 영역 캡쳐 (이미지는 BGRA 형식)
    with mss.mss() as sct:
        sct_img = sct.grab(region)
        img = np.array(sct_img)
        # BGRA 이미지를 OpenCV 표준인 BGR로 변환
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # 그레이스케일로 변환 (OCR 성능 향상을 위해)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 이진화 처리 (임계값 150, 최대값 255)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # pytesseract를 이용해 OCR 수행 ('--psm 7': 한 줄의 텍스트로 인식)
    text = pytesseract.image_to_string(thresh, config=configTesseract)
    return text.strip()

def print_unit_name():
    """
    UNIT_NAME 영역의 좌표를 사용하여 해당 영역을 캡쳐한 후,
    OCR로 유닛 이름을 추출하여 출력하는 함수입니다.

    제공된 UNIT_NAME 영역 좌표:
      {'left': 2642, 'top': 64, 'width': 88, 'height': 22}
    """
    # UNIT_NAME 영역 지정 (제공해주신 좌표 사용)
    unit_name_region = {'left': 2642, 'top': 64, 'width': 88, 'height': 22}
    # 영역 캡쳐 후 OCR로 텍스트 추출
    unit_name = capture_text_from_region(unit_name_region)
    final_text  = match_expected(unit_name, expected_list)
    # 추출된 유닛 이름 출력
    print("유닛 이름:", final_text)

if __name__ == "__main__":
    # 이 파일이 직접 실행될 때만 print_unit_name() 함수를 호출합니다.
    print_unit_name()
    time.sleep(1)
