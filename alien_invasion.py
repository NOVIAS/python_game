# -*- coding: utf-8 -*-

import pygame
from pygame.sprite import Group

import game_functions as gf
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    # 初始化游戏的设置
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion Game')

    # 创建一个用于统计信息的类
    stats = GameStats(ai_settings)
    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建一艘新的飞船
    ship = Ship(ai_settings, screen)
    # 创建一个空外星人组
    aliens = Group()
    # 创建一个用于储存子弹的空编组，管理发射出去的子弹
    bullets = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, aliens)

    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets)
        if stats.game_active:
            # 更新飞船的位置信息
            ship.update()
            # 控制子弹的状态
            gf.update_bullets(ai_settings, screen, stats, sb, aliens, bullets)
            # 控制外星人移动
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
        # 更新当前的屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
