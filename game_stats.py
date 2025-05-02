from alien_invasion import AlienInvasion


class GameStats:
    def __init__(self, ai_game: AlienInvasion) -> None:
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score: int = 0
        self.game_active: bool = False
        self.player_name: str = ""

    def reset_stats(self) -> None:
        self.ships_left: int = self.settings.ship_limit
        self.score: int = 0
        self.level: int = 1
