import pygame
from pygame.sprite import Sprite
import random


class MysteryShip(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        original_image = pygame.image.load('images/ships/mystery_ship.png')
        self.image = pygame.transform.scale(original_image, (60, 40))
        self.rect = self.image.get_rect()

        self.rect.x = self.screen_rect.right
        self.rect.y = 50

        self.x = float(self.rect.x)

        self.direction = -1
        self.speed = 0.6

        self.points = random.randint(1, 10) * 100

        self.active = False
        self.appear_time = 0
        self.delay = random.randint(10000, 30000)  # 10-30 seconds

    def update(self):
        if not self.active:
            current_time = pygame.time.get_ticks()
            if current_time - self.appear_time > self.delay:
                self.active = True
                self.x = -self.rect.width
                if random.random() > 0.5:
                    self.x = self.screen_rect.right
                    self.direction = -1
                else:
                    self.x = -self.rect.width
                    self.direction = 1
            return

        self.x += self.speed * self.direction
        self.rect.x = self.x

        if (self.direction == 1 and self.rect.left > self.screen_rect.right) or \
                (self.direction == -1 and self.rect.right < 0):
            self.reset()

    def reset(self):
        self.active = False
        self.appear_time = pygame.time.get_ticks()
        self.delay = random.randint(10000, 30000)
        self.points = random.randint(1, 10) * 100

    def draw(self):
        if self.active:
            self.screen.blit(self.image, self.rect)