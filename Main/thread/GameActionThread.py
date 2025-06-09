import time

from Main.GameFunctions import GameFunctions, thread_manager
from Main.thread import ChallengeThread
from config import config
from util.game_timer import GameTimer


def action_thread(stop_event):
    functions = GameFunctions()
    game_timer = GameTimer()

    last_trigger_times = {
        "30": False,
        "120": False,
        "210": False,
        "loop": 0  # 루프 시작 시간 (300초 이후 반복)
    }

    last_elapsed = 0  # 이전 경과 시간
    enforce_call_count = 0  # 🔥 enforce 호출 카운터 추가

    while not stop_event.is_set():
        elapsed = game_timer.elapsed()

        if elapsed >= 630:
            break

        # 게임 재시작 감지 (경과시간 감소)
        if config.GAME_STARTED:
            print("게임 재시작 감지! UNIT_CELL_STATUS 초기화")
            config.UNIT_CELL_STATUS = [False] * 18  # 초기화 추가
            last_trigger_times = {key: False if key != "loop" else 0 for key in last_trigger_times}
            enforce_call_count = 0  # 🔥 enforce 카운터 초기화
            config.GAME_STARTED = False  # 플래그 초기화

        # 30초
        if elapsed >= 30 and not last_trigger_times["30"]:
            print("🕒 30초: 소환 > 배치 > 뽑기")
            thread_manager.stop_thread("ChallengeThread")
            if stop_event.wait(1): break
            functions.summon(stop_event)
            if stop_event.wait(1): break
            functions.placement(stop_event)
            if stop_event.wait(1): break
            functions.hero_roulette(elapsed_time=elapsed, stop_event=stop_event)
            if stop_event.wait(1): break
            last_trigger_times["30"] = True
            thread_manager.start_thread("ChallengeThread", ChallengeThread.boss_thread)

        # 120초
        if elapsed >= 120 and not last_trigger_times["120"]:
            print("🕒 120초: 뽑기 > 배치 > 뽑기")
            thread_manager.stop_thread("ChallengeThread")
            if stop_event.wait(1): break  # 스레드 종료 기다리기
            functions.hero_roulette(elapsed_time=elapsed, stop_event=stop_event)
            if stop_event.wait(1): break
            functions.placement(stop_event)
            if stop_event.wait(1): break
            functions.hero_roulette(elapsed_time=elapsed, stop_event=stop_event)
            if stop_event.wait(1): break
            last_trigger_times["120"] = True
            thread_manager.start_thread("ChallengeThread", ChallengeThread.boss_thread)

        # 300초
        if elapsed >= 210 and not last_trigger_times["210"]:
            print("🕒 300초: 강화 > 뽑기 > 소환 > 배치")
            thread_manager.stop_thread("ChallengeThread")
            if stop_event.wait(1): break  # 스레드 종료 기다리기
            enforce_call_count += 1  # 🔥 enforce 호출 카운트 증가
            functions.hero_roulette(elapsed_time=elapsed)
            if stop_event.wait(1): break
            functions.enforce(is_first_call=(enforce_call_count == 1))  # 🔥 첫 호출만 True
            if stop_event.wait(1): break
            functions.summon(stop_event)
            if stop_event.wait(1): break
            functions.placement(stop_event)
            if stop_event.wait(1): break
            last_trigger_times["210"] = True
            last_trigger_times["loop"] = elapsed
            thread_manager.start_thread("ChallengeThread", ChallengeThread.boss_thread)

        # 200초 이후 반복 (100초마다)
        if elapsed >= 210:
            loop_elapsed = elapsed - last_trigger_times["loop"]
            if loop_elapsed >= 60:
                target_cells = [1, 5, 7, 11]
                true_count = sum(1 for cell in target_cells if config.UNIT_CELL_STATUS[cell - 1])
                if true_count < 2:
                    print(f"🕒 {elapsed:.2f}초: 조건 미달(1,5,7,11 중 {true_count}개 True) → 강화 > 뽑기 > 소환 > 배치")
                    thread_manager.stop_thread("ChallengeThread")
                    if stop_event.wait(1): break  # 스레드 종료 기다리기
                    enforce_call_count += 1  # 🔥 반복 enforce 호출 카운트 증가
                    functions.hero_roulette(elapsed_time=elapsed)
                    if stop_event.wait(1): break
                    functions.summon(stop_event)
                    if stop_event.wait(1): break
                    functions.placement(stop_event)
                    if stop_event.wait(1): break
                    thread_manager.start_thread("ChallengeThread", ChallengeThread.boss_thread)
                else:
                    print(f"🕒 {elapsed:.2f}초: 조건 달성(1,5,7,11 중 {true_count}개 True) → 강화만 반복")
                    thread_manager.stop_thread("ChallengeThread")
                    if stop_event.wait(1): break  # 스레드 종료 기다리기
                    enforce_call_count += 1
                    functions.enforce(is_first_call=(enforce_call_count == 1))
                    if stop_event.wait(1): break
                    thread_manager.start_thread("ChallengeThread", ChallengeThread.boss_thread)
                last_trigger_times["loop"] = elapsed
        if stop_event.wait(1): break  # 루프 대기
