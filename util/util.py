# util/util.py
import cv2
import numpy as np
import mss
import pytesseract
import pyautogui
import time

from config import config

# Tesseract 실행 파일 경로 지정 (설치된 경로에 맞게 수정)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# OCR 옵션 (예시: 한글+영어, OEM 3, PSM 7, 숫자만 인식하는 경우도 설정 가능)
ocr_config = '-l kor+eng --oem 3 --psm 7'


def capture_region_image(region):
    """
    주어진 영역(region)을 캡쳐한 후, OpenCV가 사용할 BGR 이미지로 반환합니다.
    region: {'left': 값, 'top': 값, 'width': 값, 'height': 값}
    """
    with mss.mss() as sct:
        sct_img = sct.grab(region)
        img = np.array(sct_img)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def capture_text_from_region(region):
    """
    주어진 영역(region)을 캡쳐하고, 전처리 후 pytesseract를 통해 텍스트를 추출합니다.
    반환: 추출된 텍스트 (문자열, 좌우 공백 제거)
    """
    img = capture_region_image(region)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh, config=ocr_config)
    return text.strip()


def extract_number_from_region(region):
    """
    주어진 영역(region)에서 OCR로 숫자 값을 추출하여 정수로 반환합니다.
    추출 실패 시 0 반환.
    """
    text = capture_text_from_region(region)
    try:
        return int(text)
    except:
        return 0


def find_image_on_screen(template_path, threshold=0.8):
    """
    전체 화면에서 주어진 템플릿 이미지를 찾고,
    매칭 성공 시 '중앙(x, y)' 좌표를 반환합니다.
    매칭 실패 시 None을 반환합니다.
    """
    # 1) 화면 전체 캡처
    with mss.mss() as sct:
        monitor = sct.monitors[0]  # 기본(전체) 모니터 영역
        screen_img = np.array(sct.grab(monitor))
    screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGRA2GRAY)

    # 2) 템플릿 이미지 로드 (그레이스케일)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print("템플릿 이미지 로드 실패:", template_path)
        return None

    # 3) 템플릿 매칭 수행
    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    # 4) 매칭 임계값(threshold) 이상인지 확인
    if max_val < threshold:
        return None  # 매칭 실패

    # 5) 템플릿의 너비(width)와 높이(height) 구하기
    template_height, template_width = template.shape[:2]

    # 6) 매칭된 좌측 상단 좌표(max_loc)에서 중앙 좌표 계산
    top_left_x, top_left_y = max_loc
    center_x = top_left_x + template_width // 2
    center_y = top_left_y + template_height // 2

    return (center_x, center_y)


def click_regions(sequence):
    """
    주어진 영역 이름(sequence 리스트)에 따라, config_center.REGION_CENTERS에 저장된 좌표를 순차적으로 클릭합니다.
    예: sequence = ['START', 'BUY_ENERGY_SURE', 'CB_BUY_ENERGY', 'START']
    """
    from config import config_center  # 동적으로 불러오기 (순환 참조 방지)
    for region_name in sequence:
        if region_name in config.REGION_CENTERS:
            x, y = config.REGION_CENTERS[region_name]
            print(f"{region_name} 클릭: ({x}, {y})")
            pyautogui.click(x, y)
            time.sleep(1)
        else:
            print(f"{region_name} 영역이 config_center에 존재하지 않습니다.")
