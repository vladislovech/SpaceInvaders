import pygame
from pygame.sprite import Sprite


class Bunker(Sprite):
    """A class to represent a bunker that protects the ship."""

    def __init__(self, ai_game, x_pos):
        """Initialize the bunker and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = (0, 180, 0)

        # Create a bunker rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, 80, 60)
        self.rect.x = x_pos
        self.rect.bottom = ai_game.ship.rect.top - 20

        # Bunker health
        self.health = 4

    def draw(self):
        """Draw the bunker to the screen."""
        if self.health > 0:
            pygame.draw.rect(self.screen, self.color, self.rect)