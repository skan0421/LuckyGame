import time               # 시간 지연을 위한 모듈
import pyautogui          # 마우스/키보드 자동화를 위한 모듈
from config import config, config_center
from util.util import extract_number_from_region

# ------------------------------------------------------------------
# UNIT_CHECK 영역 처리 함수 (commonB 유닛 처리)
# ------------------------------------------------------------------
def get_hero_unit():
    # 3. GET_LUCKY 버튼 클릭 (config_center.REGION_CENTERS['GET_LUCKY'])
    get_lucky_coord = config_center.REGION_CENTERS.get('GET_LUCKY')
    if get_lucky_coord:
        print("GET_LUCKY 버튼 클릭:", get_lucky_coord)
        pyautogui.click(*get_lucky_coord)
        time.sleep(0.5)
    else:
        print("GET_LUCKY 좌표가 없습니다.")

    # 4. GET_LUCKY_MIDDLE 버튼 10번 클릭, 1초 간격
    get_lucky_middle_coord = config_center.REGION_CENTERS.get('GET_LUCKY_MIDDLE')
    if get_lucky_middle_coord:
        print("GET_LUCKY_MIDDLE 버튼 10번 클릭 시작")
        for i in range(10):
            print(f"GET_LUCKY_MIDDLE 클릭 {i+1}번째:", get_lucky_middle_coord)
            pyautogui.click(*get_lucky_middle_coord)
            time.sleep(1)
    else:
        print("GET_LUCKY_MIDDLE 좌표가 없습니다.")

    # 5. CLOSE_LUCKY 버튼 클릭 (config_center.REGION_CENTERS['CLOSE_LUCKY'])
    close_lucky_coord = config_center.REGION_CENTERS.get('CLOSE_LUCKY')
    if close_lucky_coord:
        print("CLOSE_LUCKY 버튼 클릭:", close_lucky_coord)
        pyautogui.click(*close_lucky_coord)
        time.sleep(0.5)
    else:
        print("CLOSE_LUCKY 좌표가 없습니다.")
# ------------------------------------------------------------------
# 각 UNIT 셀에 대한 개별 처리 함수
# ------------------------------------------------------------------
def drag_unit(source_coord, dest_coord, duration=0.5):
    """
    source_coord에서 dest_coord로 드래그하는 함수입니다.
    duration은 드래그 동작의 지속 시간(초)입니다.
    pyautogui.dragTo()를 사용하여 드래그를 수행합니다.
    """
    print(f"드래그 시작: {source_coord} -> {dest_coord}")
    # 먼저 소스 좌표로 이동
    pyautogui.moveTo(*source_coord)
    # 소스 좌표에서 목적지까지 드래그 (마우스 왼쪽 버튼 사용)
    pyautogui.dragTo(*dest_coord, duration=duration, button='left')
    time.sleep(0.5)

def process_unit_check(current_cell, threshold=0.95):
    """
    UNIT_CHECK 영역에서 commonB 템플릿(commonB1, commonB2, commonB3) 중 하나가 발견되면,
    config.UNIT_CELL_STATUS를 참고하여 드래그 동작을 수행합니다.

    - 만약 1번 셀(인덱스 0)이 False이면, 현재 셀에서 1번 셀로 드래그하여 이동시키고,
      1번 셀 상태를 True로 변경합니다.
    - 만약 1번 셀 상태가 True이고 2번 셀(인덱스 1)이 False이면, 현재 셀에서 2번 셀로 드래그하여 이동시키고,
      2번 셀 상태를 True로 변경합니다.
    - 이미 1번과 2번 셀 모두 True이면, 별도 동작 없이 출력합니다.

    current_cell: 현재 드래그의 출발 셀 번호 (1~18)
    """
    # UNIT_CHECK 영역 정보 (config.py에 정의됨)
    unit_check_region = config.REGIONS['UNIT_CHECK']  # 예: {'left': 2633, 'top': -40, 'width': 107, 'height': 139}
    import mss, cv2, numpy as np
    with mss.mss() as sct:
        sct_img = sct.grab(unit_check_region)
        img = np.array(sct_img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    # commonB 템플릿 이미지 경로 리스트 (실제 경로에 맞게 조정)
    commonB_templates = [
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/commonB1.png",
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/commonB2.png",
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/commonB3.png"
    ]
    found = False
    for template_path in commonB_templates:
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print("commonB 템플릿 로드 실패:", template_path)
            continue
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        print(f"{template_path} 매칭 점수: {max_val}")
        if max_val >= threshold:
            found = True
            break

    if found:
        # 현재 셀에서 드래그해서 이동할 대상 셀 결정 (목표: 7번 셀, 그 다음 13번 셀)
        if not config.UNIT_CELL_STATUS[12]:
            # 7번 셀로 드래그 (config.UNIT_CELL_STATUS[6]는 7번 셀 상태)
            source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
            dest_coord = config_center.UNIT_CELL_CENTERS.get(13)
            if source_coord and dest_coord:
                drag_unit(source_coord, dest_coord)
                config.UNIT_CELL_STATUS[12] = True
            else:
                print("7번 셀 또는 현재 셀 좌표가 없습니다.")
        elif config.UNIT_CELL_STATUS[12] and not config.UNIT_CELL_STATUS[6]:
            # 13번 셀로 드래그 (config.UNIT_CELL_STATUS[12]는 13번 셀 상태)
            source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
            dest_coord = config_center.UNIT_CELL_CENTERS.get(7)
            if source_coord and dest_coord:
                drag_unit(source_coord, dest_coord)
                config.UNIT_CELL_STATUS[6] = True
            else:
                print("13번 셀 또는 현재 셀 좌표가 없습니다.")
        else:
            print("7번과 13번 셀 모두 이미 점유됨.")
    else:
        print("UNIT_CHECK 영역에서 commonB 템플릿을 찾지 못했습니다.")


def process_cell(cell):
    """
    주어진 cell 번호(예: 1~18)에 대해 다음 작업을 수행합니다.
      1. config_center.UNIT_CELL_CENTERS에서 해당 셀의 좌표를 클릭.
      2. UNIT_CHECK 처리 (commonB 템플릿 검사 및 해당 셀 이동)
      3. GET_LUCKY 버튼 클릭.
      4. GET_LUCKY_MIDDLE 버튼을 1초 간격으로 10번 클릭.
      5. CLOSE_LUCKY 버튼 클릭.
    """
    # 1. 해당 UNIT 셀 클릭
    cell_coord = config_center.UNIT_CELL_CENTERS.get(cell)
    if cell_coord:
        print(f"Unit Cell {cell} 클릭: {cell_coord}")
        pyautogui.click(*cell_coord)
        time.sleep(0.5)
    else:
        print(f"Unit Cell {cell} 좌표가 없습니다.")
        return

    # 2. UNIT_CHECK 처리: 현재 셀 번호를 인자로 전달
    process_unit_check(current_cell=cell, threshold=0.95)
    time.sleep(0.5)



# ------------------------------------------------------------------
# Before Start Game 동작 처리: 각 셀마다 개별 처리
# ------------------------------------------------------------------
def process_before7Round_game():
    """
    'ROUND' 영역에서 추출한 숫자가 7 미만이면, 각 UNIT 셀(지정된 셀 목록)에 대해
    아래 동작을 개별적으로 수행합니다.
      - GET_UNIT 버튼 20번 클릭 (전체 동작 전에 한 번 수행)
      - 각 셀마다 process_cell() 함수를 호출하여,
        UNIT_CELL_CENTER 클릭 → UNIT_CHECK 처리 → GET_LUCKY 클릭 → GET_LUCKY_MIDDLE 10회 클릭 → CLOSE_LUCKY 클릭
    """
    # 0. ROUND 영역에서 숫자 추출
    round_region = config.REGIONS['ROUND']  # 예: {'left': 2884, 'top': -46, 'width': 26, 'height': 17}
    round_number = extract_number_from_region(round_region)
    print("ROUND 숫자:", round_number)
    if round_number >= 7:
        print("ROUND 숫자가 7 이상이므로 동작을 실행하지 않습니다.")
        return
    else:
        print("ROUND 숫자가 7 미만입니다. 동작을 실행합니다.")

    # 1. GET_UNIT 버튼 20번 클릭 (예: config_center.REGION_CENTERS['GET_UNIT'] = (2862, 801))
    get_unit_coord = config_center.REGION_CENTERS.get('GET_UNIT')
    if get_unit_coord:
        print("GET_UNIT 버튼 20번 클릭 시작")
        for _ in range(20):
            pyautogui.click(*get_unit_coord)
            time.sleep(0.1)
    else:
        print("GET_UNIT 좌표가 없습니다.")

    # 2. 각 UNIT 셀을 개별적으로 처리
    cells_to_process = [1, 2, 3, 7, 8, 9, 13, 14, 15]
    for cell in cells_to_process:
        print(f"==== Unit Cell {cell} 처리 시작 ====")
        process_cell(cell)
        print(f"==== Unit Cell {cell} 처리 종료 ====")
        time.sleep(1)

    print("Before Start Game 동작 완료.")

def main():
    process_before7Round_game()
    # get_hero_unit()

    print("프로세스 종료.")

if __name__ == "__main__":
    main()
