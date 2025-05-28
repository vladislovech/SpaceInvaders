from __future__ import annotations

from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:
    from src.game.alien_invasion import AlienInvasion


class Ship(Sprite):
    """
    класс, отвечающий за корабль игрока
    """

    def __init__(self, ai_game: AlienInvasion) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        original_image = pygame.image.load('../../images/ships/player_ship.png')
        self.image = pygame.transform.scale(original_image, (60, 40))
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self) -> None:
        """
        изменяем координату X корабля
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self) -> None:
        """
        прорисовывает корабль
        """
        self.screen.blit(self.image, self.rect)

    def center_ship(self) -> None:
        """
        помещает корабль игрока по центру экрана
        """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
