# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始化位置"""
        super().__init__()
        self.screen = screen
        # 设置飞船的速度
        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        # 对元素图标进行缩放
        self.image = pygame.transform.scale(self.image, (ai_settings.ship_width, ai_settings.ship_height))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央位置
        self.rect.centerx = self.screen_rect.centerx

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        # 每艘新飞船与屏幕的底部平行
        # 对于pygame来说，左上角的坐标为0，0， 右下角的坐标为1200，800
        self.rect.bottom = self.screen_rect.bottom

        # 飞船是否处于移动状态的监听
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动状态来调整飞船的位置"""
        # 更新飞船的center值， 而不是rect
        # 对飞船可移动的边界进行限制
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        # 这里不适用 elif
        # elif 会导致 moving_right 始终保持最高级别
        # 当同时按下左右键，飞船会一直向右移动，而不是预期的在中间停止
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # 根据self.center 更新 rect 对象
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """当飞船坠毁后，重置飞船的位置"""
        self.center = self.screen_rect.centerx
