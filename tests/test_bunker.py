from unittest.mock import Mock, patch

import pytest

from src.entities.bunker import Bunker


@pytest.fixture
def mock_game() -> Mock:
    """Фикстура для создания мока игры"""
    game = Mock()
    game.screen = Mock()
    game.settings = Mock()
    game.ship = Mock()
    game.ship.rect = Mock(top=500)
    return game


def test_bunker_initialization(mock_game: Mock) -> None:
    """Тест инициализации бункера"""
    bunker = Bunker(mock_game, 100)
    assert bunker.health == 4
    assert bunker.max_health == 4
    assert bunker.rect.x == 100
    assert bunker.rect.bottom == mock_game.ship.rect.top - 20


def test_bunker_draw(mock_game: Mock) -> None:
    """Тест отрисовки бункера"""
    with patch('pygame.draw.rect') as mock_draw_rect, patch.object(Bunker, '_draw_damage_cracks') as mock_cracks:
        bunker = Bunker(mock_game, 100)
        bunker.draw()
        mock_draw_rect.assert_called()
        mock_cracks.assert_called_once()


def test_bunker_damage_cracks(mock_game: Mock) -> None:
    """Тест отрисовки трещин в зависимости от здоровья"""
    with patch('pygame.draw.line') as mock_draw_line:
        bunker = Bunker(mock_game, 100)

        # Здоровье = 3 (1 трещины)
        bunker.health = 3
        bunker._draw_damage_cracks()
        assert mock_draw_line.call_count == 1

        # трещины = 2 (2 трещины)
        mock_draw_line.reset_mock()
        bunker.health = 2
        bunker._draw_damage_cracks()
        assert mock_draw_line.call_count == 2

        # Здоровье = 1 (4 трещины)
        mock_draw_line.reset_mock()
        bunker.health = 1
        bunker._draw_damage_cracks()
        assert mock_draw_line.call_count == 4


def test_bunker_no_draw_when_dead(mock_game: Mock) -> None:
    """Тест что уничтоженный бункер не рисуется"""
    with patch('pygame.draw.rect') as mock_draw_rect:
        bunker = Bunker(mock_game, 100)
        bunker.health = 0
        bunker.draw()
        mock_draw_rect.assert_not_called()
