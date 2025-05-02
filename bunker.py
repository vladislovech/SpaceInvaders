import pygame
from pygame.sprite import Sprite

from alien_invasion import AlienInvasion


class Bunker(Sprite):
    def __init__(self, ai_game: AlienInvasion, x_pos: int) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.original_color = (0, 180, 0)

        self.rect = pygame.Rect(0, 0, 80, 60)
        self.rect.x = x_pos
        self.rect.bottom = ai_game.ship.rect.top - 20

        self.health = 4
        self.max_health = 4

    def draw(self) -> None:
        if self.health > 0:
            damage = 1 - (self.health / self.max_health)

            damaged_color = (
                max(0, self.original_color[0] - int(100 * damage)),
                max(0, self.original_color[1] - int(100 * damage)),
                max(0, self.original_color[2] - int(50 * damage)),
            )

            pygame.draw.rect(self.screen, damaged_color, self.rect)

            self._draw_damage_cracks()

    def _draw_damage_cracks(self) -> None:
        if self.health < self.max_health:
            crack_color = (40, 40, 40)  # Темно-серый

            pygame.draw.line(
                self.screen,
                crack_color,
                (self.rect.left + 5, self.rect.centery),
                (self.rect.right - 5, self.rect.centery),
                2,
            )

            if self.health <= 2:
                pygame.draw.line(
                    self.screen,
                    crack_color,
                    (self.rect.centerx, self.rect.top + 5),
                    (self.rect.centerx, self.rect.bottom - 5),
                    2,
                )

            if self.health == 1:
                pygame.draw.line(
                    self.screen,
                    crack_color,
                    (self.rect.left + 5, self.rect.top + 5),
                    (self.rect.right - 5, self.rect.bottom - 5),
                    2,
                )
                pygame.draw.line(
                    self.screen,
                    crack_color,
                    (self.rect.left + 5, self.rect.bottom - 5),
                    (self.rect.right - 5, self.rect.top + 5),
                    2,
                )
