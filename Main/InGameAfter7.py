import time               # 시간 지연을 위한 모듈
import pyautogui          # 마우스/키보드 자동화를 위한 모듈
from config import config, config_center
from util.util import extract_number_from_region

# ------------------------------------------------------------------
# UNIT_CHECK 영역 처리 함수 (commonB 유닛 처리)
# ------------------------------------------------------------------
def process_unit_check(current_cell, threshold=0.95):
    """
    UNIT_CHECK 영역에서 rareA, heroA, legendA 템플릿 중 하나가 발견되면,
    config.UNIT_CELL_STATUS를 참고하여 드래그 동작을 수행합니다.

    동작 규칙:
      1. rareA 템플릿(rareA1, rareA2, rareA3)이 감지되면:
         - 만약 4번 셀(인덱스 3)이 False이면, 현재 셀에서 4번 셀로 드래그 후 4번 셀 상태를 True로 변경.
         - 만약 4번 셀이 True이면, 10번 셀(인덱스 9)이 False인 경우 현재 셀에서 10번 셀로 드래그 후 10번 셀 상태를 True로 변경.
      2. heroA 템플릿(heroA1, heroA2, heroA3)이 감지되면:
         - 만약 3번 셀(인덱스 2)이 False이면, 현재 셀에서 3번 셀로 드래그 후 3번 셀 상태를 True로 변경.
      3. legendA 템플릿(legendA1)이 감지되면:
         - 만약 6번 셀(인덱스 5)이 False이면, 현재 셀에서 6번 셀로 드래그 후 6번 셀 상태를 True로 변경.
         - 만약 6번 셀이 True이면, 12번 셀(인덱스 11)이 False인 경우 현재 셀에서 12번 셀로 드래그 후 12번 셀 상태를 True로 변경.

    이 동작은 위의 대상 셀들이 모두 True가 될 때까지 반복됩니다.

    current_cell: 현재 드래그 출발 셀 번호 (1~18)
    """
    # UNIT_CHECK 영역 정보 (config.py에 정의됨)
    unit_check_region = config.REGIONS['UNIT_CHECK']  # 예: {'left': 2633, 'top': -40, 'width': 107, 'height': 139}
    import mss, cv2, numpy as np
    with mss.mss() as sct:
        sct_img = sct.grab(unit_check_region)
        img = np.array(sct_img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    # 템플릿 그룹별 경로 리스트 (실제 경로에 맞게 조정)
    rareA_templates = [
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/rareA1.png",
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/rareA2.png",
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/rareA3.png"
    ]
    heroA_templates = [
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/heroA1.png",
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/heroA2.png",
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/heroA3.png"
    ]
    legendA_templates = [
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/legendA1.png"
    ]

    rareA_found = False
    heroA_found = False
    legendA_found = False

    # rareA 검사
    for template_path in rareA_templates:
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print("rareA 템플릿 로드 실패:", template_path)
            continue
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        print(f"{template_path} rareA 매칭 점수: {max_val}")
        if max_val >= threshold:
            rareA_found = True
            break

    # heroA 검사
    for template_path in heroA_templates:
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print("heroA 템플릿 로드 실패:", template_path)
            continue
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        print(f"{template_path} heroA 매칭 점수: {max_val}")
        if max_val >= threshold:
            heroA_found = True
            break

    # legendA 검사
    for template_path in legendA_templates:
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print("legendA 템플릿 로드 실패:", template_path)
            continue
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        print(f"{template_path} legendA 매칭 점수: {max_val}")
        if max_val >= threshold:
            legendA_found = True
            break

    # rareA 처리: 만약 rareA가 발견되면
    if rareA_found:
        # 4번 셀: 인덱스 3
        if not config.UNIT_CELL_STATUS[3]:
            source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
            dest_coord = config_center.UNIT_CELL_CENTERS.get(4)
            if source_coord and dest_coord:
                drag_unit(source_coord, dest_coord)
                config.UNIT_CELL_STATUS[3] = True
            else:
                print("4번 셀 또는 현재 셀 좌표가 없습니다.")
        # 4번 셀이 이미 True이면, 10번 셀: 인덱스 9
        elif config.UNIT_CELL_STATUS[3] and not config.UNIT_CELL_STATUS[9]:
            source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
            dest_coord = config_center.UNIT_CELL_CENTERS.get(10)
            if source_coord and dest_coord:
                drag_unit(source_coord, dest_coord)
                config.UNIT_CELL_STATUS[9] = True
            else:
                print("10번 셀 또는 현재 셀 좌표가 없습니다.")
        else:
            print("rareA 처리: 4번과 10번 셀 모두 이미 점유됨.")

    # heroA 처리
    if heroA_found:
        # 3번 셀: 인덱스 2
        if not config.UNIT_CELL_STATUS[2]:
            source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
            dest_coord = config_center.UNIT_CELL_CENTERS.get(3)
            if source_coord and dest_coord:
                drag_unit(source_coord, dest_coord)
                config.UNIT_CELL_STATUS[2] = True
            else:
                print("3번 셀 또는 현재 셀 좌표가 없습니다.")
        else:
            print("heroA 처리: 3번 셀 이미 점유됨.")

    # legendA 처리
    if legendA_found:
        # 6번 셀: 인덱스 5
        if not config.UNIT_CELL_STATUS[5]:
            source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
            dest_coord = config_center.UNIT_CELL_CENTERS.get(6)
            if source_coord and dest_coord:
                drag_unit(source_coord, dest_coord)
                config.UNIT_CELL_STATUS[5] = True
            else:
                print("6번 셀 또는 현재 셀 좌표가 없습니다.")
        elif config.UNIT_CELL_STATUS[5] and not config.UNIT_CELL_STATUS[11]:
            # 6번 셀이 이미 True이면, 12번 셀: 인덱스 11
            source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
            dest_coord = config_center.UNIT_CELL_CENTERS.get(12)
            if source_coord and dest_coord:
                drag_unit(source_coord, dest_coord)
                config.UNIT_CELL_STATUS[11] = True
            else:
                print("12번 셀 또는 현재 셀 좌표가 없습니다.")
        else:
            print("legendA 처리: 6번과 12번 셀 모두 이미 점유됨.")

    if not (rareA_found or heroA_found or legendA_found):
        print("UNIT_CHECK 영역에서 해당 템플릿들을 찾지 못했습니다.")

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

def process_unit_check(current_cell, threshold=0.91):
    """
    UNIT_CHECK 영역에서 rareA, heroA, legendA 템플릿 중 하나가 발견되면,
    config.UNIT_CELL_STATUS를 참고하여 드래그 동작을 수행합니다.

    동작 규칙:
      1. rareA 템플릿(rareA1, rareA2, rareA3)이 감지되면:
         - 만약 4번 셀(인덱스 3)이 False이면, 현재 셀에서 4번 셀로 드래그 후 4번 셀 상태를 True로 변경.
         - 만약 4번 셀이 True이면, 10번 셀(인덱스 9)이 False인 경우 현재 셀에서 10번 셀로 드래그 후 10번 셀 상태를 True로 변경.
      2. heroA 템플릿(heroA1, heroA2, heroA3)이 감지되면:
         - 만약 3번 셀(인덱스 2)이 False이면, 현재 셀에서 3번 셀로 드래그 후 3번 셀 상태를 True로 변경.
      3. legendA 템플릿(legendA1)이 감지되면:
         - 만약 6번 셀(인덱스 5)이 False이면, 현재 셀에서 6번 셀로 드래그 후 6번 셀 상태를 True로 변경.
         - 만약 6번 셀이 True이면, 12번 셀(인덱스 11)이 False인 경우 현재 셀에서 12번 셀로 드래그 후 12번 셀 상태를 True로 변경.

    이 동작은 위의 대상 셀들이 모두 True가 될 때까지 반복됩니다.

    current_cell: 현재 드래그 출발 셀 번호 (1~18)
    """
    # UNIT_CHECK 영역 정보 (config.py에 정의됨)
    unit_check_region = config.REGIONS['UNIT_CHECK']  # 예: {'left': 2633, 'top': -40, 'width': 107, 'height': 139}
    import mss, cv2, numpy as np
    with mss.mss() as sct:
        sct_img = sct.grab(unit_check_region)
        img = np.array(sct_img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    # 템플릿 그룹별 경로 리스트 (실제 경로에 맞게 조정)
    rareA_templates = [
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/rareA1.png",
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/rareA2.png",
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/rareA3.png"
    ]
    heroA_templates = [
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/heroA1.png",
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/heroA2.png",
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/heroA3.png"
    ]
    legendA_templates = [
        r"C:/Users/user/Desktop/LuckyG/config/unit_image/legendA1.png"
    ]

    rareA_found = False
    heroA_found = False
    legendA_found = False

    # rareA 검사
    for template_path in rareA_templates:
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print("rareA 템플릿 로드 실패:", template_path)
            continue
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        print(f"{template_path} rareA 매칭 점수: {max_val}")
        if max_val >= threshold:
            rareA_found = True
            break

    # heroA 검사
    for template_path in heroA_templates:
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print("heroA 템플릿 로드 실패:", template_path)
            continue
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        print(f"{template_path} heroA 매칭 점수: {max_val}")
        if max_val >= threshold:
            heroA_found = True
            break

    # legendA 검사
    for template_path in legendA_templates:
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print("legendA 템플릿 로드 실패:", template_path)
            continue
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        print(f"{template_path} legendA 매칭 점수: {max_val}")
        if max_val >= threshold:
            legendA_found = True
            break

    # rareA 처리: 만약 rareA가 발견되면
    if rareA_found:
        # 4번 셀: 인덱스 3
        if not config.UNIT_CELL_STATUS[3]:
            source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
            dest_coord = config_center.UNIT_CELL_CENTERS.get(4)
            if source_coord and dest_coord:
                drag_unit(source_coord, dest_coord)
                config.UNIT_CELL_STATUS[3] = True
            else:
                print("4번 셀 또는 현재 셀 좌표가 없습니다.")
        # 4번 셀이 이미 True이면, 10번 셀: 인덱스 9
        elif config.UNIT_CELL_STATUS[3] and not config.UNIT_CELL_STATUS[9]:
            source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
            dest_coord = config_center.UNIT_CELL_CENTERS.get(10)
            if source_coord and dest_coord:
                drag_unit(source_coord, dest_coord)
                config.UNIT_CELL_STATUS[9] = True
            else:
                print("10번 셀 또는 현재 셀 좌표가 없습니다.")
        else:
            print("rareA 처리: 4번과 10번 셀 모두 이미 점유됨.")

    # heroA 처리
    if heroA_found:
        # 3번 셀: 인덱스 2
        if not config.UNIT_CELL_STATUS[2]:
            source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
            dest_coord = config_center.UNIT_CELL_CENTERS.get(3)
            if source_coord and dest_coord:
                drag_unit(source_coord, dest_coord)
                config.UNIT_CELL_STATUS[2] = True
            else:
                print("3번 셀 또는 현재 셀 좌표가 없습니다.")
        else:
            print("heroA 처리: 3번 셀 이미 점유됨.")

    # legendA 처리
    if legendA_found:
        # 6번 셀: 인덱스 5
        if not config.UNIT_CELL_STATUS[5]:
            source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
            dest_coord = config_center.UNIT_CELL_CENTERS.get(6)
            if source_coord and dest_coord:
                drag_unit(source_coord, dest_coord)
                config.UNIT_CELL_STATUS[5] = True
            else:
                print("6번 셀 또는 현재 셀 좌표가 없습니다.")
        elif config.UNIT_CELL_STATUS[5] and not config.UNIT_CELL_STATUS[11]:
            # 6번 셀이 이미 True이면, 12번 셀: 인덱스 11
            source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
            dest_coord = config_center.UNIT_CELL_CENTERS.get(12)
            if source_coord and dest_coord:
                drag_unit(source_coord, dest_coord)
                config.UNIT_CELL_STATUS[11] = True
            else:
                print("12번 셀 또는 현재 셀 좌표가 없습니다.")
        else:
            print("legendA 처리: 6번과 12번 셀 모두 이미 점유됨.")

    if not (rareA_found or heroA_found or legendA_found):
        print("UNIT_CHECK 영역에서 해당 템플릿들을 찾지 못했습니다.")

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
    process_unit_check(current_cell=cell, threshold=0.96)
    time.sleep(0.5)



# ------------------------------------------------------------------
# Before Start Game 동작 처리: 각 셀마다 개별 처리
# ------------------------------------------------------------------
def process_After7Round_game():
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
    if round_number <= 6:
        print("ROUND 숫자가 7 이상이므로 동작을 실행하지 않습니다.")
        return
    else:
        print("ROUND 숫자가 7 이상입니다. 동작을 실행합니다.")

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
    cells_to_process = []
    for cell in range(1, 19):
        # UNIT_CELL_STATUS 리스트의 인덱스는 cell-1
        if not config.UNIT_CELL_STATUS[cell - 1]:
            cells_to_process.append(cell)
        else:
            print(f"Unit Cell {cell} 이미 점유되어 건너뜁니다.")

    for cell in cells_to_process:
        print(f"==== Unit Cell {cell} 처리 시작 ====")
        process_cell(cell)
        print(f"==== Unit Cell {cell} 처리 종료 ====")
        time.sleep(1)

    print("Before Start Game 동작 완료.")

def main():
    process_After7Round_game()
    # get_hero_unit()

    print("프로세스 종료.")

if __name__ == "__main__":
    main()
