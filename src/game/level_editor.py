from typing import Any

import pygame
from pygame.sprite import Group

from src.entities.alien import Alien
from src.game.settings import Settings


class LevelEditor:
    """Простой редактор уровней"""

    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Level Editor")

        self.aliens = Group()
        self.running = True
        self.font = pygame.font.SysFont(None, 36)

    def run(self) -> None:
        """Запуск редактора"""
        while self.running:
            self._check_events()
            self._update_screen()

    def _check_events(self) -> None:
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка - добавить
                    self._add_alien(event.pos)
                elif event.button == 3:  # Правая кнопка - удалить
                    self._remove_alien(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # Сохранить
                    self._save_level()
                elif event.key == pygame.K_l:  # Загрузить
                    self._load_level()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def _add_alien(self, pos: Any) -> None:
        """Добавить пришельца"""
        alien = Alien(self)
        alien.rect.center = pos
        alien.x = float(alien.rect.x)
        self.aliens.add(alien)

    def _remove_alien(self, pos: Any) -> None:
        """Удалить пришельца"""
        for alien in self.aliens:
            if alien.rect.collidepoint(pos):
                self.aliens.remove(alien)
                break

    def _save_level(self) -> None:
        """Сохранить уровень в файл"""
        with open('level.txt', 'w') as f:
            for alien in self.aliens:
                f.write(f"{alien.rect.x},{alien.rect.y},{alien.alien_type}\n")

    def _load_level(self) -> None:
        """Загрузить уровень из файла"""
        try:
            with open('level.txt', 'r') as f:
                self.aliens.empty()
                for line in f:
                    x, y, alien_type = map(int, line.strip().split(','))
                    alien = Alien(self, alien_type)
                    alien.rect.x = x
                    alien.rect.y = y
                    alien.x = float(x)
                    self.aliens.add(alien)
        except FileNotFoundError:
            pass

    def _update_screen(self) -> None:
        """Обновление экрана"""
        self.screen.fill(self.settings.bg_color)

        # Отрисовка пришельцев
        for alien in self.aliens:
            self.screen.blit(alien.image, alien.rect)

        # Отрисовка инструкций
        instructions = [
            "Left Click: Add Alien",
            "Right Click: Remove Alien",
            "S: Save Level",
            "L: Load Level",
            "ESC: Exit",
        ]

        for i, text in enumerate(instructions):
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, 10 + i * 30))

        pygame.display.flip()


if __name__ == '__main__':
    editor = LevelEditor()
    editor.run()
