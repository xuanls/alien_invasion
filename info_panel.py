import pygame.font
from pygame.sprite import Group

from ship import  Ship
class Info_panel():
    """显示游戏信息"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示信息涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 字体
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分图像
        self.prep_score()
        self.prep_wave()

        # 初始生命数
        self.prep_ships()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_wave(self):
        """将波次转换为一幅渲染的图像"""
        rounded_wave = self.stats.wave
        wave_str = "wave: {:,}".format(rounded_wave)
        self.wave_image = self.font.render(wave_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # 将波次放在屏幕右上角
        self.wave_rect = self.wave_image.get_rect()
        self.wave_rect.right = self.screen_rect.right - 20
        self.wave_rect.top = 20 + self.score_rect.bottom

    def prep_ships(self):
        """显示还剩下多少飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """"在屏幕上显示分数"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.wave_image, self.wave_rect)

        if self.stats.game_activate:
            # 绘制飞船
            self.ships.draw(self.screen)


