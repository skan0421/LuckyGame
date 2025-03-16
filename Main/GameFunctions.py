from math import dist

from config import config
from util.util import find_image_on_screen
import pyautogui
import time
import cv2, numpy as np, mss

from Main.thread.ThreadManager import ThreadManager

thread_manager = ThreadManager()  # ThreadManager 인스턴스 생성


class GameFunctions:
    def summon(self, stop_event=None):
        print("소환 시작")

        found = find_image_on_screen(config.summon_button_template, threshold=0.8)
        if found:
            x, y = found
            print(f"소환 버튼 위치: {x}, {y}")

            for i in range(20):
                pyautogui.click(x, y)
                print(f"{i + 1}회 클릭 완료")
                time.sleep(0.05)

            print("소환 20회 클릭 완료")
        else:
            print("소환 버튼을 찾지 못했습니다.")

    def is_cell_empty(self, cell, threshold=0.8):
        coord = config.UNIT_DRAG_CELL.get(cell)
        if not coord:
            print(f"[오류] 셀 {cell} 좌표 없음")
            return False

        pyautogui.click(*coord)

        # emptyCell 이미지 리스트 생성
        empty_template_paths = [
            config.empty_template_path1,
            config.empty_template_path2,
            # 필요하면 더 추가
        ]

        for template_path in empty_template_paths:
            found = find_image_on_screen(template_path, threshold=threshold)
            if found:
                print(f"[DEBUG] 셀 {cell} 비어있음 ({template_path} 이미지 발견)")
                return True

        # 하나도 발견 못 하면 False
        print(f"[DEBUG] 셀 {cell} 채워짐 (emptyCell 이미지 없음)")
        return False

    def placement(self, stop_event=None):
        """
        자리배치 로직 수정:
        - 드래그 시 source와 dest가 교환(swap)되므로
          source 셀을 다시 확인하도록 while 루프로 구현
        """
        print("자리배치 시작")
        # 배치 전 상태 출력
        print("🔍 배치 전 UNIT_CELL_STATUS 상태:")
        for idx, status in enumerate(config.UNIT_CELL_STATUS, start=1):
            print(f"셀 {idx}: {'True' if status else 'False'}")

        # 유닛 타입별 목적지 맵
        unit_routing_map = {
            'commonA': [16], 'commonB': [13], 'commonD': [17],
            'rareA': [4, 10], 'rareD': [18],
            'heroA': [3, 2],
            'epicA': [14], 'epicB': [15],
            'legendA': [5, 11], 'legendB': [1, 7]
        }

        threshold = 0.88
        click_delay = 0.2

        cell = 1
        # 1번 셀부터 18번 셀까지 while 루프
        while cell <= 18:
            # 이미 채워진 셀이면 건너뛰고 다음 셀로
            if config.UNIT_CELL_STATUS[cell - 1]:
                cell += 1
                continue

            # 셀 클릭
            print(f"[셀 선택] 셀 {cell} 클릭")
            coord = config.UNIT_CELL_CENTERS[cell]
            pyautogui.click(*coord)
            pyautogui.moveTo(config.BOSS_CHALLENGE_CLOSE_POS)
            time.sleep(click_delay)

            # 셀이 비어있으면 매칭 불필요 → 다음 셀로
            if self.is_cell_empty(cell):
                print(f"[건너뜀] 셀 {cell}은 비어있음")
                cell += 1
                continue

            # 매칭 시도
            matched = self.attempt_match(cell, unit_routing_map, threshold)
            if matched:
                # 매칭·드래그 후 source 셀에 새로운 유닛이 들어왔으므로
                # 해당 셀을 다시 확인하기 위해 cell 증가는 하지 않음
                print(f"[재확인 대기] 셀 {cell} 에 새 유닛이 들어왔으니 재검사")
                continue

            # 매칭 실패 → 합성 시도
            print(f"[매칭 실패] 셀 {cell}: 합성 시도")
            self.try_synthesis(cell)
            time.sleep(click_delay)

            # 셀 재선택 후 합성 결과 확인
            print(f"[셀 재선택] 셀 {cell} 클릭")
            pyautogui.click(*coord)
            time.sleep(click_delay)

            if self.is_cell_empty(cell):
                print(f"[재매칭 실패] 셀 {cell}: 비어있음 → 판매 스킵")
                cell += 1
                continue

            # 재매칭 시도
            matched_after = self.attempt_match(cell, unit_routing_map, threshold)
            if matched_after:
                # 재매칭 성공 시에도 source 셀에 교환 생김 → 재검사
                print(f"[재매칭 성공] 셀 {cell}: 교환 후 재검사")
                continue
            else:
                # 판매 시도
                print(f"[재매칭 실패] 셀 {cell}: 판매 시도")
                self.try_sale(cell)
                # 판매 후에는 해당 셀 비어있다고 간주 → 다음 셀로
                cell += 1
                continue

        # 배치 후 상태 출력
        print("🔍 배치 후 UNIT_CELL_STATUS 상태:")
        for idx, status in enumerate(config.UNIT_CELL_STATUS, start=1):
            print(f"셀 {idx}: {'True' if status else 'False'}")

    # 헬퍼 함수들
    def attempt_match(self, cell, unit_routing_map, threshold):
        for unit_type, destinations in unit_routing_map.items():
            template_group = [
                f"{config.UNIT_IMAGE_DIR}/{unit_type}1.png",
                f"{config.UNIT_IMAGE_DIR}/{unit_type}2.png",
                f"{config.UNIT_IMAGE_DIR}/{unit_type}3.png"
            ]
            if self.match_unit_type(template_group, threshold):
                print(f"[매칭 성공] 셀 {cell} → 유닛 타입 {unit_type}")
                for dest in destinations:
                    if not config.UNIT_CELL_STATUS[dest - 1]:
                        if self.drag_unit(cell, dest):
                            config.UNIT_CELL_STATUS[dest - 1] = True
                            # config.UNIT_CELL_STATUS[cell - 1] = True
                            print(f"[배치 완료] {cell} → {dest}")
                            return True
                print(f"[배치 실패] {cell}: {unit_type}의 목적지가 모두 점유됨")
        return False

    def try_synthesis(self, cell):
        synthesis_coord = config.SYNTHESIS_CENTERS.get(cell)
        if synthesis_coord:
            pyautogui.moveTo(config.BOSS_CHALLENGE_CLOSE_POS)
            pyautogui.click(*synthesis_coord)
            time.sleep(0.5)
            pyautogui.moveTo(config.BOSS_CHALLENGE_CLOSE_POS)
            print(f"[합성 클릭] 셀 {cell}")
        else:
            print(f"[합성 실패] 셀 {cell}: 합성 좌표 없음")

    def try_sale(self, cell):
        coord = config.UNIT_CELL_CENTERS.get(cell)
        sell_coord = config.SELL_CENTERS.get(cell)
        if sell_coord:
            pyautogui.moveTo(config.BOSS_CHALLENGE_CLOSE_POS)
            pyautogui.click(*coord)
            time.sleep(0.2)
            pyautogui.moveTo(config.BOSS_CHALLENGE_CLOSE_POS)
            print(f"[판매 클릭 준비] 셀 {cell}")
            for i in range(2):
                pyautogui.click(*sell_coord)
                print(f"[판매 클릭] 셀 {cell}: {i + 1}회")
            # config.UNIT_CELL_STATUS[cell - 1] = True
            print(f"[판매 완료] 셀 {cell}: 상태 업데이트")
        else:
            print(f"[판매 실패] 셀 {cell}: 판매 좌표 없음")

    def match_unit_type(self, template_group, threshold=0.92):
        unit_check_region = config.REGIONS['UNIT_CHECK']
        region = (unit_check_region['left'], unit_check_region['top'],
                  unit_check_region['width'], unit_check_region['height'])
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            abs_region = (
                monitor["left"] + region[0],
                monitor["top"] + region[1],
                region[2],
                region[3]
            )
            sct_img = sct.grab({
                "left": abs_region[0],
                "top": abs_region[1],
                "width": abs_region[2],
                "height": abs_region[3]
            })
            screen_img = np.array(sct_img)
            screen_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGRA2GRAY)
        for template_path in template_group:
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template is None:
                print(f"[오류] 템플릿 로드 실패: {template_path}")
                continue
            res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            # print(f"{template_path} 매칭 점수: {max_val}")
            if max_val >= threshold:
                return True
        return False

    def drag_unit(self, source_cell, dest_cell):
        source_coord = config.UNIT_DRAG_CELL.get(source_cell)
        dest_coord = config.UNIT_DRAG_CELL.get(dest_cell)
        if source_coord and dest_coord:
            print(f"[드래그] {source_cell} → {dest_cell} 이동")
            # 거리 계산
            distance = dist(source_coord, dest_coord)
            duration = max(0.5, distance / 400)  # 거리 500px 당 최소 1초
            print(f"[드래그 거리]: {distance:.2f}px, duration={duration:.2f}초")
            pyautogui.moveTo(config.BOSS_CHALLENGE_CLOSE_POS)
            pyautogui.moveTo(*source_coord)
            pyautogui.dragTo(*dest_coord, duration=duration, button='left')
            time.sleep(0.5)
            pyautogui.moveTo(config.BOSS_CHALLENGE_CLOSE_POS)
            return True
        else:
            print(f"[오류] 셀 좌표 누락: source={source_cell}, dest={dest_cell}")
            return False

    def hero_roulette(self, elapsed_time=None, stop_event=None):
        print("영웅 룰렛 소환 시작")

        #룰렛 닫기 강화 닫기
        pyautogui.click(config.closeRoulette)
        pyautogui.click(config.closeEnhance)

        # 1. roulette 이미지 클릭
        pyautogui.click(config.roulette)
        print("룰렛 클릭 완료")
        time.sleep(1)

        # 2. heroRoulette or epicRoulette 클릭 (조건 분기)
        if elapsed_time is not None and elapsed_time >= 500:
            # epicRoulette 클릭
            x, y = config.epicRoulette
            print("500초 경과: epicRoulette 클릭 시작")
        else:
            # heroRoulette 클릭
            x, y = config.heroRoulette
            print("heroRoulette 클릭 시작")

        for i in range(12):
            pyautogui.click(config.epicRoulette)
            pyautogui.click(x,y)
            print(f"룰렛 클릭 {i + 1}회 완료")
            time.sleep(0.3)

        # 3. closeButton 영역 클릭 (좌표 클릭)
        pyautogui.click(config.closeRoulette)
        print("closeButton 클릭 완료")

    def enforce(self, is_first_call=False, stop_event=None):
        print("강화 시작")

        pyautogui.click(config.closeRoulette)
        pyautogui.click(config.closeEnhance)

        pyautogui.click(config.enforce)
        print(f"enforce 중앙 클릭 완료 ")
        time.sleep(1)

        # 조건 분기
        if is_first_call:
            target_cells = [1, 5, 7, 11]
            true_count = sum(1 for cell in target_cells if config.UNIT_CELL_STATUS[cell - 1])
            print(f"첫 호출: 1,5,7,11 중 {true_count}개 True")
            if true_count >= 2:
                print("조건 만족 → legendEnforce 클릭")
                for i in range(10):
                    pyautogui.click(config.legendEnforce)
                    print(f"luckyEnforce 클릭 {i + 1}회")
                    time.sleep(0.3)
            else:
                print("조건 불충족 → luckyEnforce 10회 클릭")
                for i in range(10):
                    pyautogui.click(config.luckyEnforce)
                    print(f"luckyEnforce 클릭 {i + 1}회")
                    time.sleep(0.3)
        else:
            print("반복 호출 → legendEnforce 클릭")
            for i in range(10):
                pyautogui.click(config.legendEnforce)
                print(f"luckyEnforce 클릭 {i + 1}회")
                time.sleep(0.3)

        pyautogui.click(config.closeEnhance)
        print("enforceClose 클릭 완료")


# 단독 테스트용
if __name__ == "__main__":
    print("UNIT_CHECK 영역:", config.REGIONS['UNIT_CHECK'])
    with mss.mss() as sct:
        print("모니터 리스트:", sct.monitors)
    functions = GameFunctions()
    functions.placement()
