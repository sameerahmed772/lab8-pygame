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
SPEED_BASE_CONSTANT: float = 100.0  # Formula: Max Speed = 100 / size
FRICTION: float = 0.995
ACCELERATION_RANGE: Tuple[float, float] = (-0.1, 0.1)
DEFAULT_COLOR_RANGE: Tuple[int, int] = (50, 255)

# Rendering constants
BG_COLOR: Tuple[int, int, int] = (30, 30, 30)
BG_GRID_COLOR: Tuple[int, int, int] = (35, 40, 45)
BG_BASE_COLOR: Tuple[int, int, int] = (20, 25, 30)
GRID_SIZE: int = 40
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
Square = Dict[str, Any]


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
    Create a list of square dictionaries with random sizes, colors, and speeds.
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

        # Max speed formula: F(size) = 100 / size
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
    Handle all pygame events safely.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.KEYDOWN:
            # Spacebar to add a new square
            if event.key == pygame.K_SPACE:
                squares.extend(create_squares(1, DEFAULT_COLOR_RANGE))

            # 'P' to pause/resume
            elif event.key == pygame.K_p:
                game_state["paused"] = not game_state["paused"]

            # Difficulty levels (Support both top row numbers and numpad)
            elif event.key in (pygame.K_1, pygame.K_KP1):
                game_state["difficulty"] = DIFFICULTY_LEVELS.get(1, 1.0)
            elif event.key in (pygame.K_2, pygame.K_KP2):
                game_state["difficulty"] = DIFFICULTY_LEVELS.get(2, 1.5)
            elif event.key in (pygame.K_3, pygame.K_KP3):
                game_state["difficulty"] = DIFFICULTY_LEVELS.get(3, 2.0)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Left click to remove squares and increase score
            if event.button == 1:
                mouse_pos = event.pos
                # Iterate backwards so we remove the "top" square drawn
                for s in reversed(squares):
                    if s["rect"].collidepoint(mouse_pos):
                        squares.remove(s)
                        game_state["score"] += SCORE_INCREMENT
                        break

    return True


def update_squares(squares: List[Square], game_state: Dict[str, Any]) -> None:
    """
    Update square positions, enforce size-based max speeds, and handle collisions.
    """
    if game_state["paused"]:
        return

    diff_multiplier = game_state["difficulty"]

    for square in squares:
        # 1. Apply constant acceleration (a slight random drift)
        accel_x = random.uniform(*ACCELERATION_RANGE) * diff_multiplier
        accel_y = random.uniform(*ACCELERATION_RANGE) * diff_multiplier
        square["vel"][0] += accel_x
        square["vel"][1] += accel_y

        # 2. Apply friction
        square["vel"][0] *= FRICTION
        square["vel"][1] *= FRICTION

        # 3. CAP MAX SPEED BASED ON SIZE
        max_speed = (SPEED_BASE_CONSTANT / square["size"]) * diff_multiplier
        current_speed = math.hypot(square["vel"][0], square["vel"][1])

        if current_speed > max_speed:
            # Scale velocity vector down to max_speed
            scale = max_speed / current_speed
            square["vel"][0] *= scale
            square["vel"][1] *= scale

        # 4. Move square using float positions for accuracy
        square["pos"][0] += square["vel"][0]
        square["pos"][1] += square["vel"][1]

        # Sync rect to float position
        square["rect"].x = int(square["pos"][0])
        square["rect"].y = int(square["pos"][1])

        # 5. Bounce off walls
        if square["rect"].left <= 0:
            square["rect"].left = 0
            bounce_off_wall(square, "x", -1)
        elif square["rect"].right >= WIDTH:
            square["rect"].right = WIDTH
            bounce_off_wall(square, "x", 1)

        if square["rect"].top <= 0:
            square["rect"].top = 0
            bounce_off_wall(square, "y", -1)
        elif square["rect"].bottom >= HEIGHT:
            square["rect"].bottom = HEIGHT
            bounce_off_wall(square, "y", 1)

    # 6. Collision detection between squares
    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            if squares[i]["rect"].colliderect(squares[j]["rect"]):
                # Simple elastic collision: swap velocities
                squares[i]["vel"], squares[j]["vel"] = (
                    squares[j]["vel"],
                    squares[i]["vel"],
                )

                # Push apart slightly to prevent getting stuck
                squares[i]["pos"][0] += squares[i]["vel"][0]
                squares[i]["pos"][1] += squares[i]["vel"][1]


# ============================================================================
# RENDERING
# ============================================================================


def render_text_overlays(
    screen: pygame.Surface,
    squares: List[Square],
    game_state: Dict[str, Any],
    font: pygame.font.Font,
    clock: pygame.time.Clock,
) -> None:
    """
    Render all text overlays.
    """
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, TEXT_COLOR)
    count_text = font.render(
        f"Squares: {len(squares)} (Press SPACE to add)", True, TEXT_COLOR
    )
    score_text = font.render(
        f"Score: {game_state['score']} (Click squares)", True, TEXT_COLOR
    )

    elapsed_seconds = (pygame.time.get_ticks() - game_state["start_time"]) // 1000
    timer_text = font.render(f"Timer: {elapsed_seconds}s", True, TEXT_COLOR)

    diff_text = font.render(
        f"Difficulty [1,2,3]: {game_state['difficulty']}x", True, TEXT_COLOR
    )

    screen.blit(fps_text, (TEXT_OFFSET_X, TEXT_OFFSET_X))
    screen.blit(count_text, (TEXT_OFFSET_X, TEXT_OFFSET_X + TEXT_LINE_HEIGHT))
    screen.blit(score_text, (TEXT_OFFSET_X, TEXT_OFFSET_X + TEXT_LINE_HEIGHT * 2))
    screen.blit(timer_text, (TEXT_OFFSET_X, TEXT_OFFSET_X + TEXT_LINE_HEIGHT * 3))
    screen.blit(diff_text, (TEXT_OFFSET_X, TEXT_OFFSET_X + TEXT_LINE_HEIGHT * 4))

    if game_state["paused"]:
        pause_font = pygame.font.SysFont(None, PAUSE_FONT_SIZE)
        pause_text = pause_font.render("PAUSED", True, PAUSE_TEXT_COLOR)
        screen.blit(
            pause_text,
            (
                WIDTH // 2 - pause_text.get_width() // 2,
                HEIGHT // 2 - pause_text.get_height() // 2,
            ),
        )


def render(
    screen: pygame.Surface,
    squares: List[Square],
    game_state: Dict[str, Any],
    font: pygame.font.Font,
    clock: pygame.time.Clock,
    bg_image: Optional[pygame.Surface] = None,
) -> None:
    """
    Render all squares, backgrounds, and text overlays.
    """
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(BG_COLOR)

    for square in squares:
        pygame.draw.rect(screen, square["color"], square["rect"])
        pygame.draw.rect(
            screen, SQUARE_OUTLINE_COLOR, square["rect"], SQUARE_OUTLINE_WIDTH
        )

    render_text_overlays(screen, squares, game_state, font, clock)
    pygame.display.flip()


# ============================================================================
# MAIN GAME LOOP
# ============================================================================


def main() -> None:
    """
    Main game loop orchestration.
    """
    screen, clock = init_pygame(fullscreen=False)
    font = pygame.font.SysFont(None, FONT_SIZE)

    # Create a procedural background surface
    bg_surface = pygame.Surface((WIDTH, HEIGHT))
    bg_surface.fill(BG_BASE_COLOR)

    # Draw background grid using GRID_SIZE
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(bg_surface, BG_GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(bg_surface, BG_GRID_COLOR, (0, y), (WIDTH, y))

    squares = create_squares(NUM_SQUARES)

    game_state = {
        "paused": False,
        "score": 0,
        "start_time": pygame.time.get_ticks(),
        "difficulty": DIFFICULTY_LEVELS[1],
    }

    running = True
    while running:
        running = handle_events(squares, game_state)
        update_squares(squares, game_state)
        render(screen, squares, game_state, font, clock, bg_image=bg_surface)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
