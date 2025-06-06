import time
import threading
import pyautogui

from config import config
from util.util import find_image_on_screen


def clear_thread(stop_event):
    """
    게임 중 보스 클리어 상황을 감지하는 쓰레드입니다.
    - stop_event가 set되면 종료
    - bossClear 이미지가 화면에 보이면 지정 좌표를 차례로 클릭
    """
    while not stop_event.is_set():
        # 1) 보스 클리어 이미지가 화면에 보이는지 확인
        if find_image_on_screen(config.BOSS_CLEAR_TEMPLATE, threshold=0.8):
            print("bossClear 감지, 버튼 클릭 수행 시작")

            # 2) 클릭할 첫/두 번째 버튼 좌표를 config에서 가져오기
            x1, y1 = config.BOSS_CLEAR_POS1
            x2, y2 = config.BOSS_CLEAR_POS2

            # 3) 처음 두 번 클릭 (필수)
            pyautogui.click(x1, y1)
            time.sleep(0.3)
            pyautogui.click(x2, y2)
            time.sleep(0.3)

            # 4) 추가로 같은 동작을 3회 반복
            for _ in range(3):
                # 첫 번째 버튼 클릭
                pyautogui.click(x1, y1)
                time.sleep(0.3)
                # 두 번째 버튼 클릭
                pyautogui.click(x2, y2)
                time.sleep(0.3)

            print("bossClear 버튼 클릭 완료")

        # 0.5초 대기 후 다시 감지
        time.sleep(0.5)


if __name__ == "__main__":
    # 단독 테스트: Ctrl+C로 종료할 때 stop_event.set() 호출
    stop_event = threading.Event()
    t = threading.Thread(
        target=clear_thread,
        args=(stop_event,),
        daemon=True
    )
    t.start()
    print("BossClearThread 테스트 시작 (Ctrl+C로 중지)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        print("테스트 중지")
