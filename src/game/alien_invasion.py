import sys
from time import sleep

import pygame
from game_stats import GameStats
from pygame.event import Event

from src.entities.alien import Alien
from src.entities.bullet import Bullet
from src.entities.bunker import Bunker
from src.entities.mystery_ship import MysteryShip
from src.entities.ship import Ship
from src.game.settings import Settings
from src.ui.button import Button
from src.ui.high_scores import HighScores
from src.ui.scoreboard import Scoreboard


class AlienInvasion:
    """
    основной класс проекта spaceInvaders, объединяющий всю логику игры
    """

    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.screen_rect = self.screen.get_rect()

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.high_scores = HighScores(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bunkers = pygame.sprite.Group()
        self.mystery_ship = MysteryShip(self)

        self._create_fleet()

        self.play_button = Button(self, "Play")

        self.name_input_active = False
        self.name_input_text = ""
        self.player_name = ""
        self.input_font = pygame.font.SysFont(None, 48)

    def run_game(self) -> None:
        """
        вызывает методы отрисовки элементов игры
        """
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.mystery_ship.update()

            self._update_screen()

    def _check_events(self) -> None:
        """
        отслеживает действия игрока
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.name_input_active:
                    if event.key == pygame.K_RETURN:
                        self.player_name = self.name_input_text
                        self.name_input_active = False
                        self._start_game()
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_input_text = self.name_input_text[:-1]
                    else:
                        self.name_input_text += event.unicode
                else:
                    self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos: tuple[int, int]) -> None:
        """
        проверяет, нажата ли кнопка PLAY
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active and not self.name_input_active:
            self.name_input_active = True
            self.name_input_text = ""

    def _start_game(self) -> None:
        """
        запускает игровой процесс
        """
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self._create_bunkers()
        self.ship.center_ship()

        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event: Event) -> None:
        """
        обрабатывает нажатие клавиш
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event: Event) -> None:
        """
        обрабатывает отпускание клавиш
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self) -> None:
        """
        следит за кол-вом пуль на экране, и создает новую пулю если это возможно
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self) -> None:
        """
        обновляет состояние пули
        """
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_collisions()

    def _check_bullet_collisions(self) -> None:
        """
        обрабатывает столкновение пули
        """
        bunker_hits = pygame.sprite.groupcollide(self.bullets, self.bunkers, True, False)

        for bunker in bunker_hits.values():
            for b in bunker:
                b.health -= 1
                if b.health <= 0:
                    self.bunkers.remove(b)

        if self.mystery_ship.active and pygame.sprite.spritecollideany(self.mystery_ship, self.bullets):
            self.stats.score += self.mystery_ship.points
            self.sb.prep_score()
            self.mystery_ship.reset()
            for bullet in self.bullets:
                if pygame.sprite.collide_rect(bullet, self.mystery_ship):
                    self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self) -> None:
        """
        обновляет состояние пришельца
        """
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        pygame.sprite.groupcollide(self.aliens, self.bunkers, False, True)

        self._check_aliens_bottom()

    def _check_aliens_bottom(self) -> None:
        """
        прерывание игры в случае, если пришелец достиг низа поля
        """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _draw_name_input(self) -> None:
        """
        отрисовывает поле ввода имени
        """
        prompt_text = "Enter your name:"
        prompt_surface = self.input_font.render(prompt_text, True, (255, 255, 255))
        prompt_rect = prompt_surface.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery - 50))
        self.screen.blit(prompt_surface, prompt_rect)

        input_surface = self.input_font.render(self.name_input_text, True, (255, 255, 255))
        input_rect = input_surface.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery))
        pygame.draw.rect(self.screen, (255, 255, 255), input_rect.inflate(20, 10), 2)
        self.screen.blit(input_surface, input_rect)

    def _ship_hit(self) -> None:
        """
        Обрабатывает столкновение корабля
        """
        self.stats.ships_left -= 1
        self.sb.prep_ships()

        if self.stats.ships_left <= 0:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

            if self.high_scores.check_new_high_score():
                self.high_scores.add_high_score(self.player_name)
                self.high_scores.show_high_scores()
            return

        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        sleep(0.5)

    def _create_fleet(self) -> None:
        """
        создание флота пришельцев
        """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                alien_type = 1 if (row_number + alien_number) % 2 == 0 else 2
                self._create_alien(alien_number, row_number, alien_type)

    def _create_alien(self, alien_number: int, row_number: int, alien_type: int) -> None:
        """
        создание пришельца
        """
        alien = Alien(self, alien_type)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self) -> None:
        """
        проверяет, нужно ли сменить направление движения флота пришелельцев
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        """
        сменяет направление движения флота пришельцев с постепенным приближением к игроку
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self) -> None:
        """
        отображает всю графику игры
        """
        self.screen.fill(self.settings.bg_color)

        if self.name_input_active:
            self._draw_name_input()
        elif not self.stats.game_active and not self.name_input_active:
            self.play_button.draw_button()

        if self.stats.game_active:
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            for bunker in self.bunkers.sprites():
                bunker.draw()
            self.mystery_ship.draw()
            self.sb.show_score()

        pygame.display.flip()

    def _create_bunkers(self) -> None:
        """
        создание бункеров
        """
        for i in range(4):
            bunker = Bunker(self, (i + 1) * self.settings.screen_width // 5)
            self.bunkers.add(bunker)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
