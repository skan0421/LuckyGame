import time
import threading

import cv2
import pyautogui

from util.util import find_image_on_screen
from config import config
from Main.start import StartGame, CheckSpeed
from Main.thread.ThreadManager import ThreadManager
from util.game_timer import GameTimer

game_timer = GameTimer()  # 싱글턴 객체
game_timer.start()  # 어디서든 동일 객체로 동작
print(f"게임 경과 시간: {game_timer.elapsed()}초")

# 이미지 템플릿 경로

# ThreadManager 인스턴스
thread_manager = ThreadManager()


def state_monitor():
    """
    이 함수는 게임 상태를 계속 모니터링하는 쓰레드입니다.
    - MAIN 화면이 보이면 게임 시작 및 시간 기록
    - SPEED1/2 상태가 보이면 게임 중으로 간주하고 CheckSpeed 호출
    - GAME_END 상태가 보이면 게임 종료 및 시간 측정
    """
    while True:
        # 매칭 실패 화면 감지 시 대기
        if find_image_on_screen(config.ERROR_TEMPLATE, 0.8):
            print("ERROR 상태 감지됨")
            time.sleep(5)
            continue

        # 메인 화면 진입 감지 → 게임 시작
        if find_image_on_screen(config.MAIN_TEMPLATE, 0.8):
            print("MAIN 상태 감지됨")
            game_timer.start()  # 게임 시작 시간 기록
            config.GAME_STARTED = True  # 게임 재시작 신호
            StartGame.main()
            time.sleep(5)
            continue

        # 게임 진행 중인 상태
        if find_image_on_screen(config.SPEED1_TEMPLATE, 0.8) or find_image_on_screen(config.SPEED2_TEMPLATE, 0.8):
            print("게임 중 감지됨")
            CheckSpeed.main()

            # 게임이 끝날 때까지 대기
            last_logged = 0  # 마지막으로 로그를 남긴 시간
            while find_image_on_screen(config.GAME_END_TEMPLATE, 0.8) is None:
                elapsed_time = game_timer.elapsed()
                if elapsed_time - last_logged >= 5:
                    print(f"[GameTimer] 게임 진행 중... {elapsed_time:.2f}초 경과")
                    last_logged = elapsed_time
                time.sleep(1)

            # 게임 종료 처리
            game_timer.stop()  # 종료 시간 기록
            thread_manager.stop_all()
            print(f"[GameTimer] 게임 진행 중... {elapsed_time:.2f}초 경과")

        # --- 게임 종료 처리 후 로비로 나가기 전에 moreReward 처리 추가 ---
        more_reward_path = config.MORE_REWARD_TEMPLATE  # 이미지 경로
        more_reward_loc = find_image_on_screen(more_reward_path, threshold=0.7)
        if more_reward_loc:
            print(f"🎁 moreReward 이미지 감지됨 @ {more_reward_loc}")
            # 이미지 크기 읽어서 중심 계산
            template_img = cv2.imread(more_reward_path, cv2.IMREAD_GRAYSCALE)
            h, w = template_img.shape
            center_x = more_reward_loc[0] + w // 2
            center_y = more_reward_loc[1] + h // 2
            pyautogui.click(center_x, center_y)
            print("moreReward 클릭 완료. 15초 대기...")
            time.sleep(10)
        else:
            print("❌ moreReward 이미지 감지 안됨")

        # ─── 로비 복귀 클릭 ─────────────────────────────────────────
        go_lobby = config.GO_LOBBY
        if go_lobby:
            print(f"GO_LOBBY 클릭 시도: {go_lobby}")
            # 재시도 횟수 초기화
            retry = 0
            # 최대 5번까지 클릭해보고, 'Game End' 화면이 사라졌는지 체크
            while retry < 5 and find_image_on_screen(config.GAME_END_TEMPLATE, 0.8):
                # 1) 로비 버튼 클릭
                pyautogui.click(*go_lobby)
                print(f"  ↳ {retry + 1}번째 클릭 후 대기")
                time.sleep(3)  # 클릭 후 잠시 대기
                retry += 1

            # 여전히 종료 화면이 남아있다면 경고
            if find_image_on_screen(config.GAME_END_TEMPLATE, 0.8):
                print("⚠️ GAME_END 템플릿이 여전히 감지됩니다. 클릭이 불완전할 수 있어요.")
                pyautogui.click(*go_lobby)
            else:
                print("✅ GAME_END 화면 사라짐 확인")

            # 2) 보상 팝업 닫기 (PACKAGE → CLOSE_PACKAGE)
            #    find_image_on_screen 호출에 위치 인자 사용
            pkg_loc = find_image_on_screen(config.PACKAGE_TEMPLATE, 0.7)
            if pkg_loc:
                print("PACKAGE 팝업 감지 → 닫기 버튼 탐색")
                close_loc = find_image_on_screen(config.CLOSE_PACKAGE_TEMPLATE, 0.7)
                if close_loc:
                    pyautogui.click(*close_loc)
                    print(f"닫기 버튼 클릭: {close_loc}")
                else:
                    print("❌ CLOSE_PACKAGE 이미지가 화면에서 감지되지 않음")
            else:
                print("ℹ️ PACKAGE 이미지가 감지되지 않아 닫기 동작 스킵")
        else:
            print("❌ GO_LOBBY 좌표가 정의되어 있지 않습니다.")
        # ───────────────────────────────────────────────────────────────
        continue


# 프로그램 시작 시 모니터링 쓰레드 실행
if __name__ == "__main__":
    threading.Thread(target=state_monitor, daemon=True).start()

    # 메인 쓰레드는 종료되지 않도록 무한 대기
    while True:
        time.sleep(1)
