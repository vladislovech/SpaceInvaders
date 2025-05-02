import random

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_game, alien_type=None):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.alien_type = alien_type if alien_type else random.randint(1,2)

        self.load_alien_image()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def load_alien_image(self):
        if self.alien_type == 1:
            original_image = pygame.image.load("images/aliens/alien1.png")
        else:
            original_image = pygame.image.load("images/aliens/alien2.png")

        self.image = pygame.transform.scale(original_image, (60, 40))
        self.rect = self.image.get_rect()

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x