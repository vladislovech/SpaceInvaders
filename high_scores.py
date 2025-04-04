import pygame.font
import json
from pathlib import Path


class HighScores:
    """A class to manage and display high scores table."""

    def __init__(self, ai_game):
        """Initialize high scores attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings
        self.text_color = (30, 30, 30)
        self.title_font = pygame.font.SysFont(None, 72)
        self.score_font = pygame.font.SysFont(None, 48)

        # High scores data
        self.scores_file = Path('high_scores.json')
        self.high_scores = self._load_high_scores()

        # Prepare images
        self.prep_title()
        self.prep_scores()

    def _load_high_scores(self):
        """Load high scores from file or return default if file doesn't exist."""
        try:
            if self.scores_file.exists():
                with open(self.scores_file) as f:
                    return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # Default high scores
        return [{"name": "Player", "score": score} for score in [10000, 8000, 6000, 4000, 2000]]

    def _save_high_scores(self):
        """Save high scores to file."""
        with open(self.scores_file, 'w') as f:
            json.dump(self.high_scores, f)

    def check_new_high_score(self):
        """Check if current score qualifies for high scores."""
        for i, entry in enumerate(self.high_scores):
            if self.stats.score > entry["score"]:
                return True
        return False

    def add_high_score(self, name):
        """Add a new high score to the list."""
        new_entry = {"name": name, "score": self.stats.score}
        self.high_scores.append(new_entry)
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:5]  # Keep only top 5
        self._save_high_scores()
        self.prep_scores()

    def prep_title(self):
        """Prepare the high scores title image."""
        title_str = "High Scores"
        self.title_image = self.title_font.render(title_str, True,
                                                  self.text_color, self.settings.bg_color)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.centerx = self.screen_rect.centerx
        self.title_rect.top = 100

    def prep_scores(self):
        """Prepare the high scores images."""
        self.score_images = []
        self.score_rects = []

        for i, entry in enumerate(self.high_scores):
            score_str = f"{i + 1}. {entry['name']}: {entry['score']:,}"
            score_image = self.score_font.render(score_str, True,
                                                 self.text_color, self.settings.bg_color)
            score_rect = score_image.get_rect()
            score_rect.centerx = self.screen_rect.centerx
            score_rect.top = self.title_rect.bottom + 40 + i * 40

            self.score_images.append(score_image)
            self.score_rects.append(score_rect)

    def show_high_scores(self):
        """Draw high scores to the screen."""
        self.screen.blit(self.title_image, self.title_rect)
        for image, rect in zip(self.score_images, self.score_rects):
            self.screen.blit(image, rect)