import time               # 시간 지연을 위한 모듈
import pyautogui          # 마우스/키보드 자동화를 위한 모듈
from config import config, config_center

def process_sell_and_synthesis(cell):
    """
    주어진 cell 번호(1~18)에 대해 아래 동작을 수행합니다.
      1. 해당 셀의 유닛을 클릭합니다. (UNIT_CELL_CENTERS)
      2. 해당 셀의 합성 버튼을 클릭합니다. (SYNTHESIS_CENTERS)
      3. 다시 해당 셀의 유닛을 클릭합니다.
      4. 해당 셀의 판매 버튼을 3번 클릭합니다. (SELL_CENTERS)
      5. 처리 후, 해당 셀의 상태를 True로 업데이트합니다.
    """
    # 1. 유닛 클릭 (UNIT_CELL_CENTERS)
    unit_coord = config_center.UNIT_CELL_CENTERS.get(cell)
    if unit_coord:
        print(f"Cell {cell}: 유닛 클릭 {unit_coord}")
        pyautogui.click(*unit_coord)
        time.sleep(0.5)
    else:
        print(f"Cell {cell}: UNIT_CELL_CENTERS 좌표가 없습니다.")
        return

    # 2. 합성 버튼 클릭 (SYNTHESIS_CENTERS)
    synthesis_coord = config_center.SYNTHESIS_CENTERS.get(cell)
    if synthesis_coord:
        print(f"Cell {cell}: 합성 버튼 클릭 {synthesis_coord}")
        pyautogui.click(*synthesis_coord)
        time.sleep(0.5)
    else:
        print(f"Cell {cell}: SYNTHESIS_CENTERS 좌표가 없습니다.")
        return

    # 3. 다시 유닛 클릭 (UNIT_CELL_CENTERS)
    if unit_coord:
        print(f"Cell {cell}: 다시 유닛 클릭 {unit_coord}")
        pyautogui.click(*unit_coord)
        time.sleep(0.5)

    # 4. 판매 버튼 3번 클릭 (SELL_CENTERS)
    sell_coord = config_center.SELL_CENTERS.get(cell)
    if sell_coord:
        for i in range(3):
            print(f"Cell {cell}: 판매 버튼 {i+1}번째 클릭 {sell_coord}")
            pyautogui.click(*sell_coord)
            time.sleep(0.5)
    else:
        print(f"Cell {cell}: SELL_CENTERS 좌표가 없습니다.")
        return

    # 5. 처리 후 상태 업데이트 (인덱스는 cell-1)
    config.UNIT_CELL_STATUS[cell - 1] = True
    print(f"Cell {cell} 처리 완료. 상태 업데이트됨.")

def process_sell_synthesis_all():
    """
    config.UNIT_CELL_STATUS가 False인 전체 셀(1~18)에 대해
    process_sell_and_synthesis() 함수를 반복 실행합니다.
    """
    for cell in range(1, 19):
        if not config.UNIT_CELL_STATUS[cell - 1]:
            print(f"==== Cell {cell} 처리 시작 ====")
            process_sell_and_synthesis(cell)
            print(f"==== Cell {cell} 처리 종료 ====")
            time.sleep(1)
        else:
            print(f"Cell {cell} 이미 처리되어 건너뜁니다.")

def main():
    process_sell_synthesis_all()
    print("프로세스 종료.")

if __name__ == "__main__":
    main()
