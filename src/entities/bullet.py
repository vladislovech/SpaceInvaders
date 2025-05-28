from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:
    from src.game.alien_invasion import AlienInvasion


class Bullet(Sprite):
    """
    класс, отвечающий за выстрелы
    """

    def __init__(self, ai_game: AlienInvasion, angle: float = 90) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.angle = math.radians(angle)  # угол в радианах
        self.speed = self.settings.bullet_speed

    def update(self) -> None:
        """
        изменяет координаты выстрела с учетом угла
        """
        self.x += math.cos(self.angle) * self.speed
        self.y -= math.sin(self.angle) * self.speed  # минус т.к. ось Y вниз
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        """
        отрисовывает выстрел
        """
        pygame.draw.rect(self.screen, self.color, self.rect)
