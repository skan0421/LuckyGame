from config import config
import os

def compute_center(region):
    """
    영역(region) 딕셔너리에서 중앙 좌표를 계산합니다.
    region: {'left': 값, 'top': 값, 'width': 값, 'height': 값}
    반환: (center_x, center_y)
    """
    center_x = region['left'] + region['width'] // 2
    center_y = region['top'] + region['height'] // 2
    return (center_x, center_y)

def update_centers():
    """
    config.py의 SELL_VALUES, SYNTHESIS_VALUES, REGIONS 각 항목에 대해 중앙 좌표를 계산합니다.
    반환: (sell_centers, synthesis_centers, region_centers)
      - sell_centers: {1: (cx, cy), 2: (cx, cy), ...}
      - synthesis_centers: {1: (cx, cy), 2: (cx, cy), ...}
      - region_centers: {'ENERGY': (cx,cy), ...}
    """
    sell_centers = {}
    for key, value in config.SELL_VALUES.items():
        sell_centers[key] = compute_center(value)

    synthesis_centers = {}
    for key, value in config.SYNTHESIS_VALUES.items():
        synthesis_centers[key] = compute_center(value)

    region_centers = {}
    for key, value in config.REGIONS.items():
        region_centers[key] = compute_center(value)

    return sell_centers, synthesis_centers, region_centers

def save_centers(sell_centers, synthesis_centers, region_centers, config_path="config_center.py"):
    """
    계산된 중앙 좌표들을 새로운 config 파일(config_center.py)에 저장합니다.
    """
    with open(config_path, "w", encoding="utf-8") as f:
        f.write("# config_center.py (자동 생성)\n")
        f.write("# 각 영역의 중앙 좌표를 정의합니다.\n\n")

        f.write("SELL_CENTERS = {\n")
        for key, center in sell_centers.items():
            f.write(f"    {key}: {center},\n")
        f.write("}\n\n")

        f.write("SYNTHESIS_CENTERS = {\n")
        for key, center in synthesis_centers.items():
            f.write(f"    {key}: {center},\n")
        f.write("}\n\n")

        f.write("REGION_CENTERS = {\n")
        for key, center in region_centers.items():
            f.write(f"    '{key}': {center},\n")
        f.write("}\n")

    print(f"[INFO] config_center.py가 저장되었습니다. 경로: {os.path.abspath(config_path)}")

if __name__ == '__main__':
    sell_centers, synthesis_centers, region_centers = update_centers()
    save_centers(sell_centers, synthesis_centers, region_centers)
