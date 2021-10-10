# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示外星人类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像，并设置其rect属性
        self.image = pygame.image.load("images/alien.bmp")
        self.image = pygame.transform.scale(self.image, (ai_settings.alien_width, ai_settings.alien_height))
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 保存外星人的准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定的位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edge(self):
        """如果外星人位于边缘，返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """向 左/右 移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
