class Settings:
    """
    настройки игры
    """

    def __init__(self) -> None:
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        self.ship_limit = 3

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

        self.fleet_drop_speed = 10

        self.speedup_scale = 15
        self.score_scale = 2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        """
        настройки, меняющиеся по ходу игры
        """
        self.ship_speed = 0.6
        self.bullet_speed = 1.0
        self.alien_speed = 0.3
        self.mystery_ship_speed = 2

        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self) -> None:
        """
        настройки, изменяющиеся с переходом на новые уровни
        """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
