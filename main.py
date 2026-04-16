import pygame
import random
import math
from typing import List, Dict, Tuple, Optional, Any

# ============================================================================
# CONSTANTS
# ============================================================================
WIDTH: int = 800
HEIGHT: int = 600
FPS: int = 60

MIN_SQUARE_SIZE: int = 15
MAX_SQUARE_SIZE: int = 80
NUM_SQUARES: int = 15
SQUARE_OUTLINE_WIDTH: int = 2

# LIFE SPAN CONSTANTS (Seconds converted to milliseconds)
MIN_LIFE_SPAN: int = 30 * 1000
MAX_LIFE_SPAN: int = 180 * 1000

SPEED_BASE_CONSTANT: float = 100.0
FRICTION: float = 0.995
ACCELERATION_RANGE: Tuple[float, float] = (-0.1, 0.1)
DEFAULT_COLOR_RANGE: Tuple[int, int] = (50, 255)

FLEE_RADIUS: float = 150.0
FLEE_FORCE: float = 0.8

BG_COLOR: Tuple[int, int, int] = (30, 30, 30)
BG_GRID_COLOR: Tuple[int, int, int] = (35, 40, 45)
BG_BASE_COLOR: Tuple[int, int, int] = (20, 25, 30)
GRID_SIZE: int = 40
TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)
SQUARE_OUTLINE_COLOR: Tuple[int, int, int] = (255, 255, 255)
PAUSE_TEXT_COLOR: Tuple[int, int, int] = (255, 50, 50)
FONT_SIZE: int = 24
PAUSE_FONT_SIZE: int = 72

TEXT_OFFSET_X: int = 10
TEXT_LINE_HEIGHT: int = 25
SCORE_INCREMENT: int = 100
DIFFICULTY_LEVELS: Dict[int, float] = {1: 1.0, 2: 1.5, 3: 2.0}

Square = Dict[str, Any]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def bounce_off_wall(square: Square, axis: str) -> None:
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
    pygame.init()
    pygame.font.init()
    flags = pygame.FULLSCREEN if fullscreen else 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    pygame.display.set_caption("Lab 8: Life Span & Rebirth")
    clock = pygame.time.Clock()
    return screen, clock


def create_squares(
    num_squares: int,
    color_range: Tuple[int, int] = DEFAULT_COLOR_RANGE,
) -> List[Square]:
    squares: List[Square] = []
    current_time: int = pygame.time.get_ticks()

    for _ in range(num_squares):
        size: int = random.randint(MIN_SQUARE_SIZE, MAX_SQUARE_SIZE)
        rect: pygame.Rect = pygame.Rect(
            random.randint(0, WIDTH - size),
            random.randint(0, HEIGHT - size),
            size,
            size,
        )
        color: Tuple[int, int, int] = (
            random.randint(*color_range),
            random.randint(*color_range),
            random.randint(*color_range),
        )

        max_speed: float = SPEED_BASE_CONSTANT / size
        angle: float = random.uniform(0, 2 * math.pi)
        init_speed: float = random.uniform(max_speed * 0.5, max_speed)

        # Added birth_time and life_span (ms)
        life_span: int = random.randint(MIN_LIFE_SPAN, MAX_LIFE_SPAN)

        squares.append(
            {
                "rect": rect,
                "pos": [float(rect.x), float(rect.y)],
                "color": color,
                "vel": [math.cos(angle) * init_speed, math.sin(angle) * init_speed],
                "size": size,
                "birth_time": current_time,
                "life_span": life_span,
            }
        )
    return squares


# ============================================================================
# UPDATE LOGIC
# ============================================================================


def handle_events(squares: List[Square], game_state: Dict[str, Any]) -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                squares.extend(create_squares(1))
            elif event.key == pygame.K_p:
                game_state["paused"] = not game_state["paused"]
            elif event.key in (pygame.K_1, pygame.K_KP1):
                game_state["difficulty"] = DIFFICULTY_LEVELS.get(1, 1.0)
            elif event.key in (pygame.K_2, pygame.K_KP2):
                game_state["difficulty"] = DIFFICULTY_LEVELS.get(2, 1.5)
            elif event.key in (pygame.K_3, pygame.K_KP3):
                game_state["difficulty"] = DIFFICULTY_LEVELS.get(3, 2.0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                for s in reversed(squares):
                    if s["rect"].collidepoint(mouse_pos):
                        squares.remove(s)
                        game_state["score"] += SCORE_INCREMENT
                        break
    return True


def update_squares(squares: List[Square], game_state: Dict[str, Any]) -> None:
    if game_state["paused"]:
        return

    current_time: int = pygame.time.get_ticks()
    diff_multiplier: float = game_state["difficulty"]

    # We use a copy of the list or iterate carefully when removing items
    for square in squares[:]:

        # --- LIFE SPAN CHECK ---
        if current_time - square["birth_time"] > square["life_span"]:
            squares.remove(square)
            squares.extend(create_squares(1))  # Rebirth
            continue

        # 1. Acceleration
        accel_x: float = random.uniform(*ACCELERATION_RANGE) * diff_multiplier
        accel_y: float = random.uniform(*ACCELERATION_RANGE) * diff_multiplier

        # 2. Fleeing
        flee_accel_x: float = 0.0
        flee_accel_y: float = 0.0
        sq1_center_x: float = square["pos"][0] + (square["size"] / 2.0)
        sq1_center_y: float = square["pos"][1] + (square["size"] / 2.0)

        for other in squares:
            if square is not other and other["size"] > square["size"]:
                sq2_center_x: float = other["pos"][0] + (other["size"] / 2.0)
                sq2_center_y: float = other["pos"][1] + (other["size"] / 2.0)
                dx: float = sq1_center_x - sq2_center_x
                dy: float = sq1_center_y - sq2_center_y
                distance: float = math.hypot(dx, dy)

                if distance == 0:
                    dx, dy = random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)
                    distance = math.hypot(dx, dy)

                if distance < FLEE_RADIUS:
                    repulsion: float = (FLEE_RADIUS - distance) / FLEE_RADIUS
                    flee_accel_x += (dx / distance) * FLEE_FORCE * repulsion
                    flee_accel_y += (dy / distance) * FLEE_FORCE * repulsion

        square["vel"][0] += accel_x + flee_accel_x
        square["vel"][1] += accel_y + flee_accel_y
        square["vel"][0] *= FRICTION
        square["vel"][1] *= FRICTION

        max_speed: float = (SPEED_BASE_CONSTANT / square["size"]) * diff_multiplier
        current_speed: float = math.hypot(square["vel"][0], square["vel"][1])
        if current_speed > max_speed:
            scale: float = max_speed / current_speed
            square["vel"][0] *= scale
            square["vel"][1] *= scale

        square["pos"][0] += square["vel"][0]
        square["pos"][1] += square["vel"][1]
        square["rect"].x, square["rect"].y = int(square["pos"][0]), int(
            square["pos"][1]
        )

        # Wall Bounce
        if square["rect"].left <= 0:
            square["rect"].left = 0
            bounce_off_wall(square, "x")
        elif square["rect"].right >= WIDTH:
            square["rect"].right = WIDTH
            bounce_off_wall(square, "x")
        if square["rect"].top <= 0:
            square["rect"].top = 0
            bounce_off_wall(square, "y")
        elif square["rect"].bottom >= HEIGHT:
            square["rect"].bottom = HEIGHT
            bounce_off_wall(square, "y")

    # Collisions
    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            if squares[i]["rect"].colliderect(squares[j]["rect"]):
                squares[i]["vel"], squares[j]["vel"] = (
                    squares[j]["vel"],
                    squares[i]["vel"],
                )


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
# MAIN
# ============================================================================


def main() -> None:
    screen, clock = init_pygame()
    font = pygame.font.SysFont(None, FONT_SIZE)
    bg_surface = pygame.Surface((WIDTH, HEIGHT))
    bg_surface.fill(BG_BASE_COLOR)
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
