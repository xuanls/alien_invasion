class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # 游戏刚开始时处于非活动状态
        self.game_activate = False

    def reset_stats(self):
        """初始化在游戏运行期间可能改变的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.wave = 1
