import sys, os
import cv2
import numpy as np
import mss

from config import config


def capture_full_desktop():
    """
    mss를 사용하여 전체 데스크탑(모니터0)을 캡쳐하고,
    캡쳐된 이미지와 전체 모니터 정보를 반환합니다.
    """
    with mss.mss() as sct:
        monitor = sct.monitors[0]  # monitors[0]: 전체 데스크탑
        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img, monitor

def draw_regions(image):
    """
    config.py의 REGIONS에 저장된 각 영역을 이미지에 사각형과 라벨로 표시합니다.
    UNIT_RANGE인 경우, UNIT_CELL_CENTERS를 사용하여 각 셀 중앙점도 표시합니다.
    """
    for name, region in config.REGIONS.items():
        left   = region['left']
        top    = region['top']
        width  = region['width']
        height = region['height']
        right  = left + width
        bottom = top + height

        # 영역 이름에 따라 색상 지정 (UNIT_RANGE는 노란색, 그 외는 초록색)
        if name.upper() == "UNIT_RANGE":
            color = (0, 255, 255)   # 노란색
        else:
            color = (0, 255, 0)     # 초록색

        # 사각형 그리기 및 영역 이름 표시
        cv2.rectangle(image, (left, top), (right, bottom), color, 2)
        cv2.putText(image, name, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # UNIT_RANGE인 경우, 내부에 각 셀 중앙점을 표시 (빨간색 원)
        if name.upper() == "UNIT_RANGE":
            for center in config.UNIT_CELL_CENTERS:
                abs_center = (left + center[0], top + center[1])
                cv2.circle(image, abs_center, 3, (0, 0, 255), -1)
    return image

def main():
    # 전체 데스크탑 캡쳐
    img, monitor = capture_full_desktop()
    # config.py에 저장된 영역들을 이미지에 그리기
    marked_img = draw_regions(img)

    # 결과 이미지 출력
    cv2.imshow("Config Regions Display", marked_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
