# -*- coding: utf-8 -*-

class GameStats():
    """用于统计游戏信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.ship_left = ai_settings.ship_left
        self.score = 0
        # 在游戏开始时，激活游戏
        self.game_active = False
        self.reset_state()

    def reset_state(self):
        """初始化在游戏运行时产生的各种统计数据"""
        self.ship_left = self.ai_settings.ship_left
        self.score = 0
