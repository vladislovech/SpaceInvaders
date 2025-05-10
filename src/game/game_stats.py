from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game.alien_invasion import AlienInvasion


class GameStats:
    """
    класс, отвечающий за сбор статистики игрока
    """

    def __init__(self, ai_game: AlienInvasion) -> None:
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score: int = 0
        self.game_active: bool = False
        self.player_name: str = ""

    def reset_stats(self) -> None:
        """
        сброс статистики
        """
        self.ships_left: int = self.settings.ship_limit
        self.score: int = 0
        self.level: int = 1
