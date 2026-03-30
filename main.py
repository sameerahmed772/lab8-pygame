import pygame
import random
import math
from typing import List, Dict, Tuple, Optional, Any

# ============================================================================
# CONSTANTS
# ============================================================================
# Screen dimensions
WIDTH: int = 800
HEIGHT: int = 600
FPS: int = 60

# Square properties
MIN_SQUARE_SIZE: int = 15
MAX_SQUARE_SIZE: int = 80
NUM_SQUARES: int = 15
SQUARE_OUTLINE_WIDTH: int = 2

# Physics constants
SPEED_BASE_CONSTANT: float = 100.0  # Used for F(size) max speed calculation
FRICTION: float = 0.995
ACCELERATION_RANGE: Tuple[float, float] = (-0.1, 0.1)
DEFAULT_COLOR_RANGE: Tuple[int, int] = (50, 255)

# Rendering constants
BG_COLOR: Tuple[int, int, int] = (30, 30, 30)
BG_GRID_COLOR: Tuple[int, int, int] = (35, 40, 45)
BG_BASE_COLOR: Tuple[int, int, int] = (20, 25, 30)
GRID_SIZE: int = 40  # Replaced SQUARE_SIZE for the background grid
TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)
SQUARE_OUTLINE_COLOR: Tuple[int, int, int] = (255, 255, 255)
PAUSE_TEXT_COLOR: Tuple[int, int, int] = (255, 50, 50)
FONT_SIZE: int = 24
PAUSE_FONT_SIZE: int = 72

# UI Layout
TEXT_OFFSET_X: int = 10
TEXT_LINE_HEIGHT: int = 25
SCORE_INCREMENT: int = 100
DIFFICULTY_LEVELS: Dict[int, float] = {1: 1.0, 2: 1.5, 3: 2.0}

# Type alias for clarity
Square = Dict[
    str, Any
]  # {"rect": Rect, "pos": List[float], "color": Tuple, "vel": List[float], "size": int}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def bounce_off_wall(square: Square, axis: str, velocity_sign: int) -> None:
    """
    Handle bouncing off walls by reversing velocity and resetting position.
    """
    if axis == "x":
        square["pos"][0] = float(square["rect"].x)
        square["vel"][0] *= -1
    elif axis == "y":
        square["pos"][1] = float(square["rect"].y)
        square["vel"][1] *= -1


# ============================================================================
# INITIALIZATION
# ============================================================================


def init_pygame(fullscreen: bool = False) -> Tuple[pygame.Surface, pygame.time.Clock]:
    """
    Initialize Pygame and return the screen and clock objects.
    """
    try:
        pygame.init()
        pygame.font.init()

        flags = pygame.FULLSCREEN if fullscreen else 0
        screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        pygame.display.set_caption("Lab 8: Random Moving Squares (Size = Speed)")
        clock = pygame.time.Clock()

        return screen, clock
    except pygame.error as e:
        print(f"Critical Error: Failed to initialize Pygame display. Details: {e}")
        raise SystemExit


def create_squares(
    num_squares: int,
    color_range: Tuple[int, int] = DEFAULT_COLOR_RANGE,
) -> List[Square]:
    """
    Create a list of square dictionaries with random sizes, colors, and speeds based on size.
    """
    if num_squares <= 0:
        raise ValueError("Parameter num_squares must be greater than 0.")

    squares = []
    for _ in range(num_squares):
        # Generate random size
        size = random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE)

        rect = pygame.Rect(
            random.randint(0, WIDTH - size),
            random.randint(0, HEIGHT - size),
            size,
            size,
        )
        color = (
            random.randint(*color_range),
            random.randint(*color_range),
            random.randint(*color_range),
        )

        # Max speed formula: 100 / size
        max_speed = SPEED_BASE_CONSTANT / size

        # Generate random initial trajectory
        angle = random.uniform(0, 2 * math.pi)
        init_speed = random.uniform(max_speed * 0.5, max_speed)

        squares.append(
            {
                "rect": rect,
                "pos": [float(rect.x), float(rect.y)],
                "color": color,
                "vel": [math.cos(angle) * init_speed, math.sin(angle) * init_speed],
                "size": size,
            }
        )
    return squares


# ============================================================================
# UPDATE LOGIC
# ============================================================================


def handle_events(squares: List[Square], game_state: Dict[str, Any]) -> bool:
    """
    Handle all pygame events.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                squares.extend(create_squares(1))
            elif event.key == pygame.K_p:
                game_state["paused"] = not game_state["paused"]
            elif event.key == pygame.K_1:
                game_state["difficulty"] = DIFFICULTY
