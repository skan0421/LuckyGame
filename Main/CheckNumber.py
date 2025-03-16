import cv2               # OpenCV: 이미지 처리 라이브러리
import numpy as np       # NumPy: 배열 처리를 위한 라이브러리
import mss               # mss: 화면 캡쳐 라이브러리
import pytesseract       # pytesseract: OCR(광학 문자 인식) 라이브러리
import time              # time 모듈: 대기를 위해 사용
from pynput import mouse # pynput: 마우스 이벤트 처리 라이브러리

# 필요 시 Tesseract 실행 파일 경로를 지정 (설치된 경로에 맞게 수정)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# OCR 설정 옵션: 한글과 영어, OEM 3, PSM 7 (한 줄의 텍스트 인식), 숫자만 인식하도록 whitelist 설정
ocr_config = '-l kor+eng --oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'

# 전역 변수: 사용자가 클릭한 좌표(전체 화면 기준)를 저장할 리스트
click_points = []

def on_click(x, y, button, pressed):
    """
    마우스 클릭 이벤트 콜백 함수.
    버튼이 눌릴 때마다 클릭한 좌표를 click_points 리스트에 저장합니다.
    두 번 클릭하면 리스너를 종료합니다.
    """
    if pressed:
        print(f"클릭 위치: ({x}, {y})")
        click_points.append((x, y))
        if len(click_points) == 2:
            return False  # 두 번 클릭하면 리스너 종료

def get_region_from_clicks():
    """
    click_points 리스트에 저장된 두 좌표를 이용하여,
    MSS에서 사용할 영역 딕셔너리({"left": 값, "top": 값, "width": 값, "height": 값})를 생성하여 반환합니다.
    """
    if len(click_points) < 2:
        print("두 개의 좌표가 입력되지 않았습니다.")
        return None
    (x1, y1), (x2, y2) = click_points
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    region = {"left": left, "top": top, "width": width, "height": height}
    print("설정된 영역:", region)
    return region

def capture_text_from_region(region):
    """
    주어진 영역(region)을 캡쳐한 후, OCR을 이용해 텍스트를 추출하는 함수입니다.

    매개변수:
      region: {'left': 값, 'top': 값, 'width': 값, 'height': 값} 형태의 딕셔너리.

    반환:
      추출된 텍스트 (문자열, 양쪽 공백 및 줄바꿈 제거)
    """
    with mss.mss() as sct:
        sct_img = sct.grab(region)             # 지정한 영역 캡쳐 (이미지는 BGRA 형식)
        img = np.array(sct_img)                # NumPy 배열로 변환
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # BGR 형식으로 변환

    # 그레이스케일 변환 (OCR 성능 향상을 위해)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 이진화 처리 (임계값 150, 최대값 255)
    ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    # OCR 수행, 설정 옵션 사용
    text = pytesseract.image_to_string(thresh, config=ocr_config)
    return text.strip()

def click_twice_and_extract_number():
    """
    마우스로 두 번 클릭하여 영역을 지정한 후,
    해당 영역을 캡쳐하고 OCR을 통해 숫자 값을 추출하여 바로 출력하는 함수입니다.
    """
    print("영역을 설정하려면 화면에서 두 번 클릭하세요.")
    # 마우스 리스너 실행 (두 번 클릭할 때까지 대기)
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    # 클릭된 좌표로부터 영역을 생성합니다.
    region = get_region_from_clicks()
    if region is None:
        return

    # 지정된 영역을 캡쳐하고 OCR을 통해 텍스트(숫자)를 추출합니다.
    extracted_text = capture_text_from_region(region)
    print("추출된 텍스트:", extracted_text)

    # 숫자 변환 시도 (실패 시 0 반환)
    try:
        number = int(extracted_text)
    except:
        number = 0
    print("최종 추출된 숫자:", number)
    return number

if __name__ == "__main__":
    # 이 파일이 직접 실행될 때 click_twice_and_extract_number() 함수를 호출합니다.
    click_twice_and_extract_number()
    time.sleep(1)
