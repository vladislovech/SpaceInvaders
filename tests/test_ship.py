from unittest.mock import MagicMock, Mock, patch

import pytest

from src.entities.ship import Ship


@pytest.fixture
def mock_game() -> Mock:
    game = Mock()
    game.screen = Mock()
    game.settings = Mock()
    game.settings.ship_speed = 0.5

    screen_rect = MagicMock()
    screen_rect.right = 800
    screen_rect.left = 0
    screen_rect.width = 800
    screen_rect.height = 600
    screen_rect.midbottom = (400, 600)

    game.screen.get_rect.return_value = screen_rect
    game.screen_rect = screen_rect
    return game


@pytest.fixture
def mock_surface() -> MagicMock:
    surface = MagicMock()
    ship_rect = MagicMock()
    ship_rect.width = 60
    ship_rect.height = 40
    ship_rect.midbottom = (400, 600)
    ship_rect.right = 430  # 400 + 60/2
    ship_rect.left = 370  # 400 - 60/2
    surface.get_rect.return_value = ship_rect
    return surface


def test_ship_initialization(mock_game: Mock, mock_surface: MagicMock) -> None:
    with patch('pygame.image.load', return_value=mock_surface), patch(
        'pygame.transform.scale', return_value=mock_surface
    ):
        ship = Ship(mock_game)
        assert ship.rect.midbottom == mock_game.screen_rect.midbottom
        assert not ship.moving_right
        assert not ship.moving_left


def test_ship_movement(mock_game: Mock, mock_surface: MagicMock) -> None:
    with patch('pygame.image.load', return_value=mock_surface), patch(
        'pygame.transform.scale', return_value=mock_surface
    ):
        ship = Ship(mock_game)

        # Начальные координаты
        initial_x = ship.x = 400
        ship.rect.x = 400
        ship.rect.right = 430
        ship.rect.left = 370

        # Движение вправо
        ship.moving_right = True
        ship.update()
        assert ship.x == initial_x + mock_game.settings.ship_speed

        # Движение влево
        ship.moving_right = False
        ship.moving_left = True
        initial_x = ship.x
        ship.update()
        assert ship.x == initial_x - mock_game.settings.ship_speed


def test_ship_boundaries(mock_game: Mock, mock_surface: MagicMock) -> None:
    with patch('pygame.image.load', return_value=mock_surface), patch(
        'pygame.transform.scale', return_value=mock_surface
    ):
        ship = Ship(mock_game)

        # Правый край
        ship.x = 800 - 30  # 800 (screen right) - половина ширины корабля
        ship.rect.x = ship.x
        ship.rect.right = 800
        ship.moving_right = True
        initial_x = ship.x
        ship.update()
        assert ship.x == initial_x  # Не должен двигаться дальше

        # Левый край
        ship.x = 30  # Половина ширины корабля
        ship.rect.x = ship.x
        ship.rect.left = 0
        ship.moving_left = True
        initial_x = ship.x
        ship.update()
        assert ship.x == initial_x  # Не должен двигаться дальше


def test_ship_center(mock_game: Mock, mock_surface: MagicMock) -> None:
    with patch('pygame.image.load', return_value=mock_surface), patch(
        'pygame.transform.scale', return_value=mock_surface
    ):
        ship = Ship(mock_game)
        ship.x = 100
        ship.rect.x = 100
        ship.center_ship()
        assert ship.rect.midbottom == mock_game.screen_rect.midbottom
