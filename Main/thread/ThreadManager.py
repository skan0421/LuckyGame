import threading
import time


class ThreadManager:
    _instance = None  # 싱글톤 인스턴스

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ThreadManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.threads = {}
        self.stop_events = {}
        self.__initialized = True

    def start_thread(self, name, target):
        """
        스레드를 시작합니다. 이미 실행 중이면 종료 후 재시작하고,
        진입·종료 로그를 남깁니다.
        """
        # 기존 스레드가 실행 중이면 종료 대기
        if name in self.threads:
            t_old = self.threads[name]
            if t_old.is_alive():
                print(f"[{name}] 이미 실행 중입니다. 종료 대기 중...")
                self.stop_thread(name)
                t_old.join(timeout=5)
                if t_old.is_alive():
                    print(f"[{name}] 종료되지 않아 강제 재시작합니다.")
                else:
                    print(f"[{name}] 정상 종료 후 재시작합니다.")

        # 새로운 stop_event 생성 및 저장
        stop_event = threading.Event()
        self.stop_events[name] = stop_event

        # 스레드 실행을 래핑할 함수
        def _run_with_logging():
            print(f"[{name}] ● ENTER THREAD LOOP")
            try:
                target(stop_event)
            finally:
                print(f"[{name}] ✖ EXIT THREAD LOOP")

        # 새 스레드 생성 및 시작
        t = threading.Thread(target=_run_with_logging, daemon=True)
        self.threads[name] = t
        print(f"[{name}] ▶ START THREAD")
        t.start()

        # 즉시 종료 확인
        time.sleep(1)
        if not t.is_alive():
            print(f"[{name}] 스레드가 즉시 종료되었습니다. 로직을 점검하세요.")

    def stop_thread(self, name):
        """
        특정 스레드에 종료 신호를 보냅니다.
        """
        ev = self.stop_events.get(name)
        if ev:
            ev.set()
            print(f"[{name}] ■ STOP SIGNAL SENT")
        else:
            print(f"[{name}] 종료 대상 스레드가 없습니다.")

    def stop_all(self):
        """
        모든 등록된 스레드에 종료 신호를 보냅니다.
        """
        print("[ThreadManager] ■ STOP ALL THREADS")
        for name, ev in self.stop_events.items():
            ev.set()
            print(f"[{name}] ■ STOP SIGNAL SENT")

    def is_running(self, name):
        """
        스레드 실행 상태 조회
        """
        t = self.threads.get(name)
        return bool(t and t.is_alive())
