# 游戏设置
import pygame.image


class Settings():
    """存储《外星人入侵》的所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.bg_color = (112, 184, 255)

        bg_image = pygame.image.load('images/bg_image_1.png')
        self.bg_image = pygame.transform.scale(bg_image, (self.screen_width, self.screen_height))

        # 图标设置
        self.icon = pygame.image.load('images/nailong_2_48×48.ico')

        # 音乐设置
        self.bgm_path = 'music/nailong.mp3'

        # 飞船设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_allowed = 10

        # 外星人设置


        # 以什么样的速度加快游戏
        self.speedup_scale = 1.1

        # 外星人点数提高的速度
        self.score_scale = 1.5

        # 动态设置
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的量"""
        self.ship_speed_factor = 5
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 2
        self.fleet_drop_speed = 0.3

        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.fleet_drop_speed *= self.speedup_scale
        self.alien_points *= self.score_scale
        # print(self.alien_points)