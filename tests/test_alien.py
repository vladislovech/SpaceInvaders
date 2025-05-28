from unittest.mock import MagicMock, Mock, patch

import pytest

from src.entities.alien import Alien


@pytest.fixture
def mock_game() -> Mock:
    game = Mock()
    game.screen = Mock()
    game.settings = Mock()
    game.settings.alien_speed = 0.5
    game.settings.fleet_direction = 1
    game.screen.get_rect.return_value = MagicMock(right=800, left=0)  # Добавляем мок для get_rect
    return game


@pytest.fixture
def mock_surface() -> MagicMock:
    """Фикстура для создания мока Surface"""
    surface = MagicMock()
    surface.get_rect.return_value = MagicMock(width=60, height=40)
    return surface


def test_alien_initialization(mock_game: Mock, mock_surface: MagicMock) -> None:
    """Проверка инициализации пришельца"""
    with patch('pygame.image.load', return_value=mock_surface), patch(
        'pygame.transform.scale', return_value=mock_surface
    ):
        alien = Alien(mock_game, 1)
        assert alien.alien_type == 1
        assert hasattr(alien, 'rect')
        assert alien.x == alien.rect.x
        assert hasattr(alien, 'image')


def test_alien_load_image(mock_game: Mock, mock_surface: MagicMock) -> None:
    """Проверка загрузки изображения"""
    with patch('pygame.image.load', return_value=mock_surface) as mock_load, patch(
        'pygame.transform.scale', return_value=mock_surface
    ):
        alien = Alien(mock_game)
        mock_load.assert_called()
        assert hasattr(alien, 'image')


def test_alien_check_edges(mock_game: Mock, mock_surface: MagicMock) -> None:
    """Проверка обнаружения края экрана"""
    with patch('pygame.image.load', return_value=mock_surface), patch(
        'pygame.transform.scale', return_value=mock_surface
    ):
        alien = Alien(mock_game)

        # Проверка правого края
        alien.rect.right = mock_game.screen.get_rect().right + 1
        assert alien.check_edges() is True

        # Проверка левого края
        alien.rect.left = -1
        assert alien.check_edges() is True

        # Проверка когда не у края
        alien.rect.left = 100
        alien.rect.right = 200
        assert alien.check_edges() is False


def test_alien_update(mock_game: Mock, mock_surface: MagicMock) -> None:
    """Проверка движения пришельца"""
    with patch('pygame.image.load', return_value=mock_surface), patch(
        'pygame.transform.scale', return_value=mock_surface
    ):
        alien = Alien(mock_game)
        initial_x = alien.x
        alien.update()
        assert alien.x == initial_x + mock_game.settings.alien_speed * mock_game.settings.fleet_direction
