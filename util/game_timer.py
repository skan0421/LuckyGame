# game_timer.py
import time

class GameTimer:
    _instance = None  # 싱글턴 인스턴스 저장

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GameTimer, cls).__new__(cls)
            cls._instance.start_time = None
            cls._instance.end_time = None
        return cls._instance

    def start(self):
        self.start_time = time.time()
        self.end_time = None  # 시작할 때 종료 시간 초기화
        print("[GameTimer] 게임 시작 시간 기록됨.")

    def stop(self):
        self.end_time = time.time()
        print("[GameTimer] 게임 종료 시간 기록됨.")
        print(f"[GameTimer] 총 게임 시간: {self.elapsed():.2f}초")
        self.start_time = None
        self.end_time = None

    def elapsed(self):
        if self.start_time is None:
            return 0
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time
