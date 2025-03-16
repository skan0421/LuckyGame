import cv2                               # OpenCV: 이미지 처리 라이브러리
import numpy as np                       # 넘파이: 배열 처리 라이브러리
import mss                               # mss: 화면 캡쳐 라이브러리
from pynput import mouse                 # pynput: 마우스 이벤트 처리 라이브러리
import os

# -----------------------------
# 1. 영역 분할을 위한 클래스 정의 (예: UNIT_RANGE 전용)
# -----------------------------
class RegionGrid:
    def __init__(self, image, rows, cols):
        """
        image: 캡쳐된 이미지 (영역)
        rows, cols: 분할할 행과 열 개수
        """
        self.image = image
        self.rows = rows
        self.cols = cols

    def subdivide(self):
        """
        이미지를 rows x cols 격자로 나누고,
        각 셀의 중앙 좌표와 그리드가 그려진 이미지를 반환.
        """
        height, width, _ = self.image.shape
        cell_width = width / self.cols
        cell_height = height / self.rows
        grid_img = self.image.copy()
        centers = []

        # 가로선 그리기
        for r in range(self.rows + 1):
            y = int(r * cell_height)
            cv2.line(grid_img, (0, y), (width, y), (255, 255, 255), 1)

        # 세로선 그리기
        for c in range(self.cols + 1):
            x = int(c * cell_width)
            cv2.line(grid_img, (x, 0), (x, height), (255, 255, 255), 1)

        # 각 셀의 중앙 좌표 계산 후 초록색 점 표시
        for r in range(self.rows):
            for c in range(self.cols):
                center_x = int((c + 0.5) * cell_width)
                center_y = int((r + 0.5) * cell_height)
                centers.append((center_x, center_y))
                cv2.circle(grid_img, (center_x, center_y), 3, (0, 255, 0), -1)

        return grid_img, centers

# -----------------------------
# 2. 전역 변수 및 기본 함수 정의
# -----------------------------
# 사용자가 클릭한 좌표(전체 화면 기준)를 저장할 리스트
# (각 영역은 두 점으로 정의됨)
points = []

def on_click(x, y, button, pressed):
    """
    마우스 클릭 이벤트 콜백 함수.
    버튼이 눌릴 때 좌표를 points 리스트에 저장하고,
    두 점이 입력되면 리스너를 종료합니다.
    """
    if pressed:
        print(f"클릭 위치: ({x}, {y})")
        points.append((x, y))
        if len(points) == 2:
            return False  # 2번 클릭 시 리스너 종료

def get_region_from_points(pt_pair):
    """
    두 점(pt_pair)을 받아, 좌측상단과 우측하단을 계산한 후,
    MSS에서 사용할 영역 딕셔너리 {"left": 값, "top": 값, "width": 값, "height": 값}를 반환합니다.
    """
    (x1, y1), (x2, y2) = pt_pair
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)
    return {"left": left, "top": top, "width": right - left, "height": bottom - top}

def capture_region_image(region):
    """
    mss를 사용하여 지정한 영역(region)을 캡쳐한 이미지를 반환합니다.
    """
    with mss.mss() as sct:
        sct_img = sct.grab(region)
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img

def show_region(region_name, region, image):
    """
    영역 정보와 이미지를 OpenCV 창에 표시합니다.
    """
    print(f"{region_name} 영역: {region}")
    cv2.imshow(f"{region_name} 영역", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_to_config_py(regions, grid_data, config_path="config.py"):
    """
    regions: dict, 예: {"ROUND_RANGE": {...}, "GOLD_RANGE": {...}, "UNIT_RANGE": {...}}
    grid_data: dict, UNIT_RANGE에 대한 그리드 정보, 예: {"UNIT_CELL_CENTERS": [...], "UNIT_CELL_STATUS": [...]}
    config_path: 저장할 config.py의 경로
    """
    with open(config_path, "w", encoding="utf-8") as f:
        f.write("# config.py (자동 생성)\n\n")
        f.write("REGIONS = {\n")
        for name, region in regions.items():
            f.write(f"    '{name}': {region},\n")
        f.write("}\n\n")
        if grid_data:
            f.write("UNIT_CELL_CENTERS = [\n")
            for center in grid_data.get("UNIT_CELL_CENTERS", []):
                f.write(f"    {center},\n")
            f.write("]\n\n")
            status = grid_data.get("UNIT_CELL_STATUS", [])
            f.write(f"UNIT_CELL_STATUS = {status}\n")
    print(f"[INFO] config.py가 생성(또는 갱신)되었습니다. 경로: {os.path.abspath(config_path)}")

# -----------------------------
# 3. 메인 함수: 반복적으로 영역 정의 및 저장
# -----------------------------
def main():
    regions = {}      # 영역 이름: 영역 딕셔너리 (예: "ROUND_RANGE": {...})
    grid_data = {}    # UNIT_RANGE 전용 그리드 정보 저장 (있을 경우)

    print("영역을 정의하려면, 각 영역에 대해 두 점을 클릭하세요.")
    print("각 영역이 정의된 후, 영역의 이름을 입력받습니다.")
    print("종료하려면 영역 이름 입력 시 'q'를 입력하세요.\n")

    while True:
        # 매 영역마다 points 리스트 초기화
        del points[:]  # 리스트 초기화

        print("영역 정의: 마우스로 두 점을 클릭하세요.")
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

        if len(points) < 2:
            print("두 점이 입력되지 않았습니다. 다시 시도하세요.")
            continue

        # 영역 딕셔너리 생성
        region = get_region_from_points(points)

        # 현재 정의된 영역을 캡쳐해서 미리보기
        region_img = capture_region_image(region)
        show_region("미리보기", region, region_img)

        # 영역 이름 입력 (사용자가 종료할 때까지)
        region_name = input("이 영역의 이름을 입력하세요 (종료하려면 'q' 입력): ").strip()
        if region_name.lower() == 'q':
            print("영역 정의를 종료합니다.")
            break

        regions[region_name] = region
        print(f"'{region_name}' 영역이 저장되었습니다.\n")

        # 만약 영역 이름이 UNIT_RANGE라면, 3행×6열로 18개 셀로 분할하여 그리드 생성
        if region_name.upper() == "UNIT_RANGE":
            # UNIT_RANGE 영역 이미지 재캡쳐 (이미 충분히 정확한 영역이라 가정)
            unit_img = capture_region_image(region)
            # RegionGrid 클래스 사용 (3행 x 6열)
            grid = RegionGrid(unit_img, 3, 6)
            grid_img, centers = grid.subdivide()
            print("UNIT_RANGE를 3행 x 6열로 나눈 각 셀의 중앙 좌표 (로컬 기준):")
            for i, center in enumerate(centers, start=1):
                print(f"{i}번 셀: {center}")
            show_region("UNIT_RANGE (격자)", region, grid_img)
            grid_data["UNIT_CELL_CENTERS"] = centers
            grid_data["UNIT_CELL_STATUS"] = [False] * len(centers)

        cont = input("다른 영역을 정의하시겠습니까? (y/n): ").strip().lower()
        if cont != 'y':
            break

    # config.py에 저장 (config.py 파일 경로는 필요에 따라 수정)
    save_to_config_py(regions, grid_data, config_path="../config/new_config.py")
    print("프로그램을 종료합니다.")

if __name__ == "__main__":
    main()
