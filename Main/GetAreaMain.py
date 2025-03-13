import cv2
import numpy as np
import mss
from pynput import mouse
import os

# -----------------------------
# 1. 전역 변수 및 함수 정의
# -----------------------------
points = []  # 마우스 클릭 좌표 저장 (전체 화면 기준)

def on_click(x, y, button, pressed):
    """
    마우스 클릭 이벤트 콜백 함수.
    6번 클릭하면 종료.
    """
    if pressed:
        print(f"클릭 위치: ({x}, {y})")
        points.append((x, y))
        if len(points) == 6:
            return False  # 리스너 종료

def get_region_from_points(pt_pair):
    """
    두 점을 받아, MSS에 사용 가능한 영역 딕셔너리 반환.
    예: {"left": x1, "top": y1, "width": w, "height": h}
    """
    (x1, y1), (x2, y2) = pt_pair
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)
    return {"left": left, "top": top, "width": right - left, "height": bottom - top}

def capture_region_image(region):
    """
    mss를 사용하여 지정한 영역을 캡쳐한 이미지를 반환.
    """
    with mss.mss() as sct:
        sct_img = sct.grab(region)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

def show_region(region_name, region, image):
    """
    영역 정보와 이미지를 표시.
    """
    print(f"{region_name} 영역: {region}")
    cv2.imshow(f"{region_name} 영역", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def subdivide_and_draw_grid(image, rows, cols):
    """
    image를 rows x cols 격자로 나누고,
    각 셀의 중앙 좌표를 계산해 선 및 점을 그린 이미지를 반환.
    """
    height, width, _ = image.shape
    cell_width = width / cols
    cell_height = height / rows
    grid_img = image.copy()
    centers = []

    # 가로선
    for r in range(rows + 1):
        y = int(r * cell_height)
        cv2.line(grid_img, (0, y), (width, y), (255, 255, 255), 1)

    # 세로선
    for c in range(cols + 1):
        x = int(c * cell_width)
        cv2.line(grid_img, (x, 0), (x, height), (255, 255, 255), 1)

    # 중앙점 계산
    for r in range(rows):
        for c in range(cols):
            center_x = int((c + 0.5) * cell_width)
            center_y = int((r + 0.5) * cell_height)
            centers.append((center_x, center_y))
            cv2.circle(grid_img, (center_x, center_y), 3, (0, 255, 0), -1)

    return grid_img, centers

def save_to_config_py(round_range, gold_range, unit_range, centers, config_path="config.py"):
    """
    전달받은 좌표(ROUND_RANGE, GOLD_RANGE, UNIT_RANGE)와
    UNIT_RANGE의 18개 셀 중앙 좌표(centers)를 config.py에 저장.
    """
    # config.py를 덮어쓰기 모드로 연다.
    with open(config_path, "w", encoding="utf-8") as f:
        f.write("# config.py (자동 생성)\n\n")

        # ROUND_RANGE, GOLD_RANGE, UNIT_RANGE
        f.write(f"ROUND_RANGE = {round_range}\n")
        f.write(f"GOLD_RANGE = {gold_range}\n")
        f.write(f"UNIT_RANGE = {unit_range}\n\n")

        # UNIT_CELL_CENTERS
        f.write("UNIT_CELL_CENTERS = [\n")
        for cx, cy in centers:
            f.write(f"    ({cx}, {cy}),\n")
        f.write("]\n\n")

        # UNIT_CELL_STATUS (예: 처음에는 모두 False)
        f.write(f"UNIT_CELL_STATUS = [False] * {len(centers)}\n")

    print(f"\n[INFO] config.py가 생성(또는 갱신)되었습니다. 경로: {os.path.abspath(config_path)}")

# -----------------------------
# 2. 메인 함수
# -----------------------------
def main():
    print("총 6번의 클릭으로 3개의 영역(ROUND_RANGE, GOLD_RANGE, UNIT_RANGE)을 지정하세요.")

    # 마우스 리스너: 6번 클릭할 때까지 대기
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    # 좌표가 6개 미만이면 종료
    if len(points) < 6:
        print("6개의 좌표가 입력되지 않았습니다. 프로그램을 종료합니다.")
        return

    print("입력된 좌표 (전체 화면 기준):", points)

    # 2개씩 나눠 영역 추출
    round_range_points = points[0:2]
    gold_range_points  = points[2:4]
    unit_range_points  = points[4:6]

    # 딕셔너리 형태로 변환
    round_range = get_region_from_points(round_range_points)
    gold_range  = get_region_from_points(gold_range_points)
    unit_range  = get_region_from_points(unit_range_points)

    print("ROUND_RANGE =", round_range)
    print("GOLD_RANGE  =", gold_range)
    print("UNIT_RANGE  =", unit_range)

    # 영역별 캡쳐
    round_img = capture_region_image(round_range)
    gold_img  = capture_region_image(gold_range)
    unit_img  = capture_region_image(unit_range)

    # 영역 표시
    # show_region("ROUND_RANGE", round_range, round_img)
    # show_region("GOLD_RANGE",  gold_range,  gold_img)

    # UNIT_RANGE → 3행 × 6열로 나누고 격자/중앙점 표시
    rows, cols = 3, 6
    grid_img, centers = subdivide_and_draw_grid(unit_img, rows, cols)

    print("UNIT_RANGE를 3행 x 6열로 나눈 각 셀의 중앙 좌표 (로컬 기준):")
    for i, center in enumerate(centers, start=1):
        print(f"{i}번 셀: {center}")

    # show_region("UNIT_RANGE (격자)", unit_range, grid_img)

    # config.py에 저장
    save_to_config_py(round_range, gold_range, unit_range, centers, config_path="../config/config.py")


if __name__ == "__main__":
    main()
