# BeforeStartGame.pyimport time
import time

from util.util import (capture_region_image, capture_text_from_region,
                       extract_number_from_region, find_image_on_screen,
                       click_regions)
from config import config

def main():
    # 예시: main.png 템플릿 탐색 및 START 버튼 클릭
    main_template = r"C:/Users/user/Desktop/LuckyG/config/unit_image/main.png"
    found_main = find_image_on_screen(main_template, threshold=0.8)
    if found_main is None:
        print("main.png 템플릿이 화면에서 발견되지 않았습니다.")
        return
    else:
        print("main.png 템플릿 발견:", found_main)
        click_regions(['START'])
        time.sleep(1)

    # 예시: buy_energy.png 템플릿 탐색 후, BUY_ENERGY 영역의 숫자 추출
    buy_energy_template = r"C:/Users/user/Desktop/LuckyG/config/unit_image/buy_energy.png"
    found_buy = find_image_on_screen(buy_energy_template, threshold=0.8)
    if found_buy is None:
        print("buy_energy.png 템플릿이 화면에서 발견되지 않았습니다.")
        return
    else:
        print("buy_energy.png 템플릿 발견:", found_buy)
        buy_energy_number = extract_number_from_region(config.REGIONS['BUY_ENERGY'])
        print("추출된 BUY_ENERGY 숫자:", buy_energy_number)
        if buy_energy_number >= 300:
            print("BUY_ENERGY 숫자가 300 이상입니다. 추가 동작 중지.")
            return
        else:
            sequence = ['START', 'BUY_ENERGY_SURE', 'CB_BUY_ENERGY', 'CB_UPGRADE', 'START']
            click_regions(sequence)

if __name__ == "__main__":
    main()