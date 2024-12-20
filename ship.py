import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """飞船"""

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像
        original_image = pygame.image.load('images/nailong_2.png')

        # 定义缩放后的尺寸
        scaled_width = original_image.get_width() // 2  # 将宽度缩小一半
        scaled_height = original_image.get_height() // 2  # 将高度缩小一半

        # 缩放图片
        self.image = pygame.transform.scale(original_image, (scaled_width, scaled_height))

        # 获取其外接矩形
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船位置"""
        # 更新飞船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制飞机"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船停在屏幕居中"""
        self.center = self.screen_rect.centerx