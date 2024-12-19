import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """外星人"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其初始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像，并设置其rect属性
        original_image = pygame.image.load('images/nailong.bmp')

        # 定义缩放后的尺寸
        scaled_width = original_image.get_width() // 2  # 将宽度缩小一半
        scaled_height = original_image.get_height() // 2  # 将高度缩小一半

        # 缩放图片
        self.image = pygame.transform.scale(original_image, (scaled_width, scaled_height))

        # 获取其外接矩形
        self.rect = self.image.get_rect()

        # 每个外星人初始都在屏幕左上角附近
        self.rect.x = 0
        self.rect.y = 0

        # 存储外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.fleet_direction = 1

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """外星人位于屏幕边缘返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """向左或向右移动外星人，同时向下移动"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.fleet_direction)
        self.rect.x = self.x
        self.y += self.ai_settings.fleet_drop_speed
        self.rect.y = self.y


