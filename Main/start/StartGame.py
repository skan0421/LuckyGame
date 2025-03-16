import time
from util.util import (extract_number_from_region, find_image_on_screen,
                       click_regions)
from config import config


# 게임 시작 전 작업 수행 (BeforeStartGame.py의 내용)
def main():
    # 1. main.png 템플릿 탐색 및 START 버튼 클릭
    found_main = find_image_on_screen(config.MAIN_TEMPLATE, threshold=0.8)
    if found_main is None:
        print("main.png 템플릿이 화면에서 발견되지 않았습니다.")
        return
    else:
        print("main.png 템플릿 발견:", found_main)
        click_regions(['START'])
        time.sleep(1)

    # 2. buy_energy.png 템플릿 탐색 후 BUY_ENERGY 영역의 숫자 추출
    found_buy = find_image_on_screen(config.BUY_ENERGY_TEMPLATE, threshold=0.8)
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
    # 게임 시작 전 작업 실행
    main()
    print("게임 시작 전 작업 완료. 게임 시작 후 10초 대기합니다...")
    time.sleep(10)

    print("getLegendThread 실행됨. 메인 스레드는 계속 대기합니다.")
    # 메인 스레드가 종료되지 않도록 무한 대기
    while True:
        time.sleep(1)
