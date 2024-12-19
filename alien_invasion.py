# 创建pygame窗口并响应用户输入

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import  Button
from info_panel import Info_panel
import game_functions as gf

import logging
import traceback

logging.basicConfig(filename='app.log', level=logging.ERROR)

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = ai_settings.screen
    icon = ai_settings.icon
    bg_image = ai_settings.bg_image

    pygame.display.set_caption("我才是奶龙！")
    pygame.display.set_icon(icon)

    # 创建一个用于储存统计信息的实例，并创建信息面板
    stats = GameStats(ai_settings)
    info = Info_panel(ai_settings, screen, stats)

    # 创建一艘飞船、一个子弹编组和一个外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # 创建play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, stats, info, play_button, ship, aliens, bullets)

        if stats.game_activate:
            ship.update()
            gf.update_bullet(ai_settings, screen, stats, info, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, info, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, info, ship, aliens, bullets, play_button)


if __name__ == '__main__':

    try:
        run_game()
        print("程序启动")
    except Exception as e:
        logging.error(f"程序崩溃: {e}\\n{traceback.format_exc()}")
        print("程序崩溃，请查看 app.log 文件获取更多信息")
