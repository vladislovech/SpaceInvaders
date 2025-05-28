from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pygame.font

if TYPE_CHECKING:
    from src.game.alien_invasion import AlienInvasion


class HighScores:
    """
    класс, отвечающий за таблицу рекордов
    """

    def __init__(self, ai_game: AlienInvasion) -> None:
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (255, 255, 255)
        self.title_font = pygame.font.SysFont(None, 72)
        self.score_font = pygame.font.SysFont(None, 48)

        self.scores_file = Path('../../data/high_scores.json')
        self.high_scores = self._load_high_scores()

    def _load_high_scores(self) -> Any:
        """
        загружает таблицу рекордов в формате JSON
        """
        try:
            if self.scores_file.exists():
                with open(self.scores_file) as f:
                    return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        return []

    def _save_high_scores(self) -> None:
        """
        сохраняет таблицу рекордов в формате JSON
        """
        with open(self.scores_file, 'w') as f:
            json.dump(self.high_scores, f, indent=4)

    def check_new_high_score(self) -> bool:
        """
        проверяет, нужно ли добавлять новый рекорд в таблицу
        """
        if len(self.high_scores) < 5:
            return True
        result: bool = self.stats.score > min(score['score'] for score in self.high_scores)
        return result

    def add_high_score(self, name: str) -> None:
        """
        добавляет новую запись в таблицу рекордов
        """
        new_entry = {"name": name, "score": self.stats.score}
        self.high_scores.append(new_entry)
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:5]
        self._save_high_scores()

    def show_high_scores(self) -> None:
        """
        выводит таблицу рекордов игроку
        """
        overlay = pygame.Surface((self.screen_rect.width, self.screen_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        title = self.title_font.render("High Scores", True, self.text_color)
        title_rect = title.get_rect(center=(self.screen_rect.centerx, 100))
        self.screen.blit(title, title_rect)

        for i, entry in enumerate(self.high_scores[:5]):
            score_text = f"{i+1}. {entry['name']}: {entry['score']:,}"
            score_render = self.score_font.render(score_text, True, self.text_color)
            score_rect = score_render.get_rect(center=(self.screen_rect.centerx, 180 + i * 50))
            self.screen.blit(score_render, score_rect)

        continue_text = self.score_font.render("Press any key to continue", True, self.text_color)
        continue_rect = continue_text.get_rect(center=(self.screen_rect.centerx, self.screen_rect.height - 50))
        self.screen.blit(continue_text, continue_rect)

        pygame.display.flip()
        self._wait_for_key()

    def _wait_for_key(self) -> None:
        """
        ожидание действий игрока, после вывода таблицы рекордов
        """
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
