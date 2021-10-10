# -*- coding: utf-8 -*-
import pygame


class Settings:
    """保存游戏的所有设置类"""

    def __init__(self):
        """初始化游戏的所有设置"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 设置飞船的速度
        self.ship_speed_factor = 1.5
        # 设置飞船的宽度
        self.ship_width = 50
        self.ship_height = 50
        # 设置飞船有多少次机会
        self.ship_left = 3

        # 初始化子弹
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        # 屏幕上最多存在5发子弹
        self.bullets_allowed = 5

        # 设置外星人的宽、高
        self.alien_width = 50
        self.alien_height = 50
        # 设置外星人移动速度
        self.alien_speed_factor = 0.5
        # 设置外星人群向下移动速度
        self.fleet_drop_speed = 6
        # fleet_direction = 1 表示向右移动， -1 表示向左
        # 用于在接触到屏幕边缘是，更改移动方向
        self.fleet_direction = 1

        # 设置按钮的相关
        self.button_width = 200
        self.button_height = 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 225, 255)
        self.font = pygame.font.SysFont("微软雅黑", 48)
