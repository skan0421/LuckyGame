import time
import pyautogui
from config import config, config_center
from util.util import extract_number_from_region
import mss, cv2, numpy as np

class UnitAutomation:
    def __init__(self):
        # 필요시 초기화 작업 수행
        pass

    # ------------------------------
    # 공통 기능: 드래그 동작
    # ------------------------------
    def drag_unit(self, source_coord, dest_coord, duration=0.5):
        print(f"드래그 시작: {source_coord} -> {dest_coord}")
        pyautogui.moveTo(*source_coord)
        pyautogui.dragTo(*dest_coord, duration=duration, button='left')
        time.sleep(0.5)

    # ------------------------------
    # 전투 시작 전 동작 (Before7Round)
    # commonB 템플릿 검사
    # ------------------------------
    def process_unit_check_before(self, current_cell, threshold=0.95):
        print("process_unit_check_before 실행 - commonB 템플릿 검사")
        unit_check_region = config.REGIONS['UNIT_CHECK']
        with mss.mss() as sct:
            sct_img = sct.grab(unit_check_region)
            img = np.array(sct_img)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
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
            # 조건에 따라 7번 셀(인덱스 12) 또는 13번 셀(인덱스 6)로 드래그
            if not config.UNIT_CELL_STATUS[12]:
                source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
                dest_coord = config_center.UNIT_CELL_CENTERS.get(13)
                if source_coord and dest_coord:
                    self.drag_unit(source_coord, dest_coord)
                    config.UNIT_CELL_STATUS[12] = True
                else:
                    print("7번 셀 또는 현재 셀 좌표가 없습니다.")
            elif config.UNIT_CELL_STATUS[12] and not config.UNIT_CELL_STATUS[6]:
                source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
                dest_coord = config_center.UNIT_CELL_CENTERS.get(7)
                if source_coord and dest_coord:
                    self.drag_unit(source_coord, dest_coord)
                    config.UNIT_CELL_STATUS[6] = True
                else:
                    print("13번 셀 또는 현재 셀 좌표가 없습니다.")
            else:
                print("7번과 13번 셀 모두 이미 점유됨.")
        else:
            print("UNIT_CHECK 영역에서 commonB 템플릿을 찾지 못했습니다.")

    def process_cell_before(self, cell):
        print(f"==== Unit Cell {cell} 처리 시작 (Before) ====")
        cell_coord = config_center.UNIT_CELL_CENTERS.get(cell)
        if cell_coord:
            print(f"Unit Cell {cell} 클릭: {cell_coord}")
            pyautogui.click(*cell_coord)
            time.sleep(0.5)
        else:
            print(f"Unit Cell {cell} 좌표가 없습니다.")
            return
        self.process_unit_check_before(current_cell=cell, threshold=0.95)
        time.sleep(0.5)
        print(f"==== Unit Cell {cell} 처리 종료 (Before) ====")

    def process_before7Round_game(self):
        round_region = config.REGIONS['ROUND']
        round_number = extract_number_from_region(round_region)
        print("ROUND 숫자:", round_number)
        if round_number >= 7:
            print("ROUND 숫자가 7 이상이므로 Before7Round 동작을 실행하지 않습니다.")
            return
        else:
            print("ROUND 숫자가 7 미만입니다. Before7Round 동작을 실행합니다.")

        # GET_UNIT 버튼 20회 클릭
        get_unit_coord = config_center.REGION_CENTERS.get('GET_UNIT')
        if get_unit_coord:
            print("GET_UNIT 버튼 20번 클릭 시작")
            for _ in range(20):
                pyautogui.click(*get_unit_coord)
                time.sleep(0.1)
        else:
            print("GET_UNIT 좌표가 없습니다.")

        # 특정 셀만 처리 (예: 1, 2, 3, 7, 8, 9, 13, 14, 15)
        cells_to_process = [1, 2, 3, 7, 8, 9, 13, 14, 15]
        for cell in cells_to_process:
            self.process_cell_before(cell)
            time.sleep(0.3)
        print("Before7Round 동작 완료.")

    def get_hero_unit(self):
        print("GET_LUCKY 버튼 클릭")
        get_lucky_coord = config_center.REGION_CENTERS.get('GET_LUCKY')
        if get_lucky_coord:
            print("GET_LUCKY 버튼 클릭:", get_lucky_coord)
            pyautogui.click(*get_lucky_coord)
            time.sleep(0.5)
        else:
            print("GET_LUCKY 좌표가 없습니다.")

        get_lucky_middle_coord = config_center.REGION_CENTERS.get('GET_LUCKY_MIDDLE')
        if get_lucky_middle_coord:
            print("GET_LUCKY_MIDDLE 버튼 10번 클릭 시작")
            for i in range(10):
                print(f"GET_LUCKY_MIDDLE 클릭 {i+1}번째:", get_lucky_middle_coord)
                pyautogui.click(*get_lucky_middle_coord)
                time.sleep(0.5)
        else:
            print("GET_LUCKY_MIDDLE 좌표가 없습니다.")

        close_lucky_coord = config_center.REGION_CENTERS.get('CLOSE_LUCKY')
        if close_lucky_coord:
            print("CLOSE_LUCKY 버튼 클릭:", close_lucky_coord)
            pyautogui.click(*close_lucky_coord)
            time.sleep(0.5)
        else:
            print("CLOSE_LUCKY 좌표가 없습니다.")

    # ------------------------------
    # 전투 시작 후 동작 (After7Round)
    # rareA, heroA, legendA 템플릿 검사
    # ------------------------------
    def process_unit_check_after(self, current_cell, threshold=0.91):
        print("process_unit_check_after 실행 - rareA, heroA, legendA 템플릿 검사")
        unit_check_region = config.REGIONS['UNIT_CHECK']
        with mss.mss() as sct:
            sct_img = sct.grab(unit_check_region)
            img = np.array(sct_img)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
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

        # rareA 처리
        if rareA_found:
            if not config.UNIT_CELL_STATUS[3]:
                source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
                dest_coord = config_center.UNIT_CELL_CENTERS.get(4)
                if source_coord and dest_coord:
                    self.drag_unit(source_coord, dest_coord)
                    config.UNIT_CELL_STATUS[3] = True
                else:
                    print("4번 셀 또는 현재 셀 좌표가 없습니다.")
            elif config.UNIT_CELL_STATUS[3] and not config.UNIT_CELL_STATUS[9]:
                source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
                dest_coord = config_center.UNIT_CELL_CENTERS.get(10)
                if source_coord and dest_coord:
                    self.drag_unit(source_coord, dest_coord)
                    config.UNIT_CELL_STATUS[9] = True
                else:
                    print("10번 셀 또는 현재 셀 좌표가 없습니다.")
            else:
                print("rareA 처리: 4번과 10번 셀 모두 이미 점유됨.")

        # heroA 처리
        if heroA_found:
            if not config.UNIT_CELL_STATUS[2]:
                source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
                dest_coord = config_center.UNIT_CELL_CENTERS.get(3)
                if source_coord and dest_coord:
                    self.drag_unit(source_coord, dest_coord)
                    config.UNIT_CELL_STATUS[2] = True
                else:
                    print("3번 셀 또는 현재 셀 좌표가 없습니다.")
            else:
                print("heroA 처리: 3번 셀 이미 점유됨.")

        # legendA 처리
        if legendA_found:
            if not config.UNIT_CELL_STATUS[5]:
                source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
                dest_coord = config_center.UNIT_CELL_CENTERS.get(6)
                if source_coord and dest_coord:
                    self.drag_unit(source_coord, dest_coord)
                    config.UNIT_CELL_STATUS[5] = True
                else:
                    print("6번 셀 또는 현재 셀 좌표가 없습니다.")
            elif config.UNIT_CELL_STATUS[5] and not config.UNIT_CELL_STATUS[11]:
                source_coord = config_center.UNIT_CELL_CENTERS.get(current_cell)
                dest_coord = config_center.UNIT_CELL_CENTERS.get(12)
                if source_coord and dest_coord:
                    self.drag_unit(source_coord, dest_coord)
                    config.UNIT_CELL_STATUS[11] = True
                else:
                    print("12번 셀 또는 현재 셀 좌표가 없습니다.")
            else:
                print("legendA 처리: 6번과 12번 셀 모두 이미 점유됨.")

        if not (rareA_found or heroA_found or legendA_found):
            print("UNIT_CHECK 영역에서 해당 템플릿들을 찾지 못했습니다.")

    def process_cell_after(self, cell):
        print(f"==== Unit Cell {cell} 처리 시작 (After) ====")
        cell_coord = config_center.UNIT_CELL_CENTERS.get(cell)
        if cell_coord:
            print(f"Unit Cell {cell} 클릭: {cell_coord}")
            pyautogui.click(*cell_coord)
            time.sleep(0.5)
        else:
            print(f"Unit Cell {cell} 좌표가 없습니다.")
            return
        # after 동작에서는 약간 다른 threshold 사용 (예: 0.96)
        self.process_unit_check_after(current_cell=cell, threshold=0.96)
        time.sleep(0.3)
        print(f"==== Unit Cell {cell} 처리 종료 (After) ====")

    def process_after7Round_game(self):
        round_region = config.REGIONS['ROUND']
        round_number = extract_number_from_region(round_region)
        print("ROUND 숫자:", round_number)
        if round_number < 7:
            print("ROUND 숫자가 7 미만이므로 After7Round 동작을 실행하지 않습니다.")
            return
        else:
            print("ROUND 숫자가 7 이상입니다. After7Round 동작을 실행합니다.")

        get_unit_coord = config_center.REGION_CENTERS.get('GET_UNIT')
        if get_unit_coord:
            print("GET_UNIT 버튼 20번 클릭 시작")
            for _ in range(20):
                pyautogui.click(*get_unit_coord)
                time.sleep(0.1)
        else:
            print("GET_UNIT 좌표가 없습니다.")

        cells_to_process = []
        for cell in range(1, 19):
            if not config.UNIT_CELL_STATUS[cell - 1]:
                cells_to_process.append(cell)
            else:
                print(f"Unit Cell {cell} 이미 점유되어 건너뜁니다.")

        for cell in cells_to_process:
            self.process_cell_after(cell)
            time.sleep(0.5)
        print("After7Round 동작 완료.")

    # ------------------------------
    # 판매 및 합성 동작
    # ------------------------------
    def process_sell_and_synthesis(self, cell):
        print(f"==== Cell {cell} 판매 및 합성 처리 시작 ====")
        unit_coord = config_center.UNIT_CELL_CENTERS.get(cell)
        if unit_coord:
            print(f"Cell {cell}: 유닛 클릭 {unit_coord}")
            pyautogui.click(*unit_coord)
            time.sleep(0.2)
        else:
            print(f"Cell {cell}: UNIT_CELL_CENTERS 좌표가 없습니다.")
            return

        synthesis_coord = config_center.SYNTHESIS_CENTERS.get(cell)
        if synthesis_coord:
            print(f"Cell {cell}: 합성 버튼 클릭 {synthesis_coord}")
            pyautogui.click(*synthesis_coord)
            time.sleep(0.2)
        else:
            print(f"Cell {cell}: SYNTHESIS_CENTERS 좌표가 없습니다.")
            return

        # 다시 유닛 클릭
        if unit_coord:
            print(f"Cell {cell}: 다시 유닛 클릭 {unit_coord}")
            pyautogui.click(*unit_coord)
            time.sleep(0.2)

        sell_coord = config_center.SELL_CENTERS.get(cell)
        if sell_coord:
            for i in range(3):
                print(f"Cell {cell}: 판매 버튼 {i+1}번째 클릭 {sell_coord}")
                pyautogui.click(*sell_coord)
                time.sleep(0.2)
        else:
            print(f"Cell {cell}: SELL_CENTERS 좌표가 없습니다.")
            return

        config.UNIT_CELL_STATUS[cell - 1] = True
        print(f"Cell {cell} 판매 및 합성 처리 완료. 상태 업데이트됨.")

    def process_sell_synthesis_all(self):
        print("전체 셀에 대한 판매 및 합성 동작 실행 시작.")
        for cell in range(1, 19):
            if not config.UNIT_CELL_STATUS[cell - 1]:
                print(f"==== Cell {cell} 처리 시작 ====")
                self.process_sell_and_synthesis(cell)
                print(f"==== Cell {cell} 처리 종료 ====")
                time.sleep(0.3)
            else:
                print(f"Cell {cell} 이미 처리되어 건너뜁니다.")
        print("전체 판매 및 합성 동작 완료.")

    # ------------------------------
    # 전체 실행 흐름 조정
    # ------------------------------
    def run(self):
        round_region = config.REGIONS['ROUND']
        round_number = extract_number_from_region(round_region)
        print("전체 실행 시작. 현재 ROUND 숫자:", round_number)

        if round_number < 7:
            self.process_before7Round_game()
            self.get_hero_unit()
        else:
            # ROUND가 7 이상이면 3, 6, 10, 12번 셀이 모두 True가 될 때까지 반복 실행
            while not (config.UNIT_CELL_STATUS[2] and config.UNIT_CELL_STATUS[3] and config.UNIT_CELL_STATUS[5] and config.UNIT_CELL_STATUS[11]):
                print("조건 미충족: 3, 6, 10, 12번 셀 중 하나 이상이 아직 False입니다.")
                print(f"현재 상태 - Cell 3: {config.UNIT_CELL_STATUS[2]}, "
                      f"Cell 6: {config.UNIT_CELL_STATUS[3]}, "
                      f"Cell 10: {config.UNIT_CELL_STATUS[5]}, "
                      f"Cell 12: {config.UNIT_CELL_STATUS[11]}")
                self.process_after7Round_game()
                self.process_sell_synthesis_all()
                self.get_hero_unit()
                self.get_hero_unit()


        print("전체 프로세스 종료.")

if __name__ == "__main__":
    automation = UnitAutomation()
    automation.run()
