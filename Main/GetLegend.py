import cv2                # OpenCV: 이미지 처리 라이브러리
import numpy as np        # NumPy: 배열 처리를 위한 라이브러리
import mss                # mss: 화면 캡쳐 라이브러리
import pyautogui          # pyautogui: 마우스/키보드 자동화 라이브러리
import time               # time 모듈: 대기를 위해 사용
from config import config, config_center
from util.util import (capture_region_image, capture_text_from_region,
                       extract_number_from_region, find_image_on_screen,
                       click_regions)

def click_legend_area(threshold=0.8):
    """
    config.py의 'LEGEND_AREA' 영역에서 get_legendA, get_legendB, get_legendC 템플릿 중
    하나라도 매칭되면 해당 영역의 중앙 좌표를 계산하여 클릭하는 함수입니다.

    동작 과정:
      1. config.REGIONS['LEGEND_AREA']에 정의된 영역을 mss를 통해 캡쳐합니다.
      2. 캡쳐한 이미지를 그레이스케일로 변환합니다.
      3. 미리 준비된 템플릿 이미지들(get_legendA, get_legendB, get_legendC)을 각각 로드하고,
         템플릿 매칭을 수행합니다.
      4. 매칭 점수가 임계값(threshold) 이상이면, 매칭된 영역의 중앙 좌표(절대 좌표)를 계산하여 클릭합니다.
    """
    # 1. LEGEND_AREA 영역 정보 불러오기 (config.py에 정의됨)
    legend_region = config.REGIONS['LEGEND_AREA']  # 예: {'left': 2585, 'top': 96, 'width': 156, 'height': 386}

    # 2. mss를 사용하여 LEGEND_AREA 영역 캡쳐
    with mss.mss() as sct:
        sct_img = sct.grab(legend_region)
        img = np.array(sct_img)
        # BGRA -> 그레이스케일 변환 (템플릿 매칭 성능 향상)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    # 3. 템플릿 이미지 경로 지정 (경로는 실제 위치에 맞게 조정)
    legend_templates = {
        # "get_legendA": r"C:/Users/user/Desktop/LuckyG/config/unit_image/get_legendA.png",
        # "get_legendB": r"C:/Users/user/Desktop/LuckyG/config/unit_image/get_legendB.png",
        "get_legendC": r"C:/Users/user/Desktop/LuckyG/config/unit_image/get_legendC.png"
    }

    # 4. 각 템플릿에 대해 템플릿 매칭 수행
    for key, template_path in legend_templates.items():
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print(f"{key} 템플릿 이미지를 로드할 수 없습니다: {template_path}")
            continue

        # 템플릿 매칭 (정규화 상관 계수 방식)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        print(f"{key} 매칭 점수: {max_val}")

        # 임계값 이상이면 해당 템플릿과 유사하다고 판단
        if max_val >= threshold:
            # 템플릿 매칭 결과 max_loc는 LEGEND_AREA 영역 내 상대 좌표입니다.
            # 절대 좌표 계산: LEGEND_AREA 영역의 'left'와 'top' 오프셋을 더해주고,
            # 템플릿의 중앙으로 보정 (템플릿 width/2, height/2)
            template_h, template_w = template.shape
            abs_x = legend_region['left'] + max_loc[0] + template_w // 2
            abs_y = legend_region['top'] + max_loc[1] + template_h // 2
            print(f"{key}가 발견되었습니다. 절대 좌표: ({abs_x}, {abs_y}) 클릭합니다.")
            pyautogui.click(abs_x, abs_y)
            time.sleep(0.5)  # 클릭 후 잠시 대기
        else:
            print(f"{key} 템플릿과 유사한 영역을 찾지 못했습니다.")

if __name__ == "__main__":
    click_legend_area(threshold=0.7)
