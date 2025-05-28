from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:
    from src.game.alien_invasion import AlienInvasion


class Bullet(Sprite):
    """
    класс, отвечающий за выстрелы
    """

    def __init__(self, ai_game: AlienInvasion) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self) -> None:
        """
        изменяет координату У выстрела
        """
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        """
        отрисовывает выстрел
        """
        pygame.draw.rect(self.screen, self.color, self.rect)
