import pygame
from pygame.sprite import Sprite
import random


class MysteryShip(Sprite):
    """A class to represent the mystery ship that appears randomly."""

    def __init__(self, ai_game):
        """Initialize the mystery ship."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the image and set its rect
        original_image = pygame.image.load('images/ships/mystery_ship.png')
        self.image = pygame.transform.scale(original_image, (60, 40))
        self.rect = self.image.get_rect()

        # Start the mystery ship off-screen
        self.rect.x = self.screen_rect.right
        self.rect.y = 50

        # Store the ship's exact position
        self.x = float(self.rect.x)

        # Movement direction and speed
        self.direction = -1  # Moves left to right
        self.speed = 0.6

        # Points value (random between 100 and 1000 in increments of 100)
        self.points = random.randint(1, 10) * 100

        # Appearance timing
        self.active = False
        self.appear_time = 0
        self.delay = random.randint(10000, 30000)  # 10-30 seconds

    def update(self):
        """Update the mystery ship's position."""
        if not self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.appear_time > self.delay:
                self.active = True
                self.x = -self.rect.width  # Start from left if moving right
                if random.random() > 0.5:  # 50% chance to move right to left
                    self.x = self.screen_rect.right
                    self.direction = -1
                else:  # 50% chance to move left to right
                    self.x = -self.rect.width
                    self.direction = 1
            return

        self.x += self.speed * self.direction
        self.rect.x = self.x

        # Reset if moved off screen
        if (self.direction == 1 and self.rect.left > self.screen_rect.right) or \
                (self.direction == -1 and self.rect.right < 0):
            self.reset()

    def reset(self):
        """Reset the mystery ship for another appearance."""
        self.active = False
        self.appear_time = pygame.time.get_ticks()
        self.delay = random.randint(10000, 30000)  # 10-30 seconds
        self.points = random.randint(1, 10) * 100

    def draw(self):
        """Draw the mystery ship at its current location."""
        if self.active:
            self.screen.blit(self.image, self.rect)