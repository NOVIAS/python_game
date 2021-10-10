# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """显示得分信息"""

    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.score_image = None
        self.score_rect = None
        self.ships = None

        # 显示得分时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont("微软雅黑", 48)

        # 准备初始得分图像
        self.prep_score()
        # 剩余飞船数量图像
        self.prep_ships()

    def prep_score(self):
        """将得分转换为一张图像"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将得分放到右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分"""
        # round 让浮点数精确到小数点几位，负数则表示按整10，100，...取值
        rounded_score = int(round(self.stats.score, 0))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)
        self.screen.blit(self.score_image, self.score_rect)
        # 绘制飞船
        self.ships.draw(self.screen)

    def prep_ships(self):
        """显示还剩下多少飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
