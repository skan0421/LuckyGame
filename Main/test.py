from pynput import mouse

# 마우스 클릭 이벤트 콜백 함수
def on_click(x, y, button, pressed):
    if pressed:
        print(f"클릭한 좌표: ({x}, {y})")
        # 클릭할 때마다 계속 좌표 출력
    # 멈추지 않으므로 리스너는 종료하지 않음
    # if len(points) == 2: return False  와 같은 종료 조건은 생략

def main():
    print("마우스 클릭 위치를 출력합니다. 멈추려면 Ctrl+C를 눌러주세요.\n")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()  # 리스너가 계속 대기 상태 유지

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
