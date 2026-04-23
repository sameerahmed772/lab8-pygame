import pygame
import random
import math
from typing import List, Dict, Tuple, Optional, TypedDict

# ============================================================================
# CONSTANTS
# ============================================================================
WIDTH: int = 800
HEIGHT: int = 600
FPS: int = 60

# Square properties
MIN_SQUARE_SIZE: int = 15
MAX_SQUARE_SIZE: int = 80
NUM_SQUARES: int = 15
SQUARE_OUTLINE_WIDTH: int = 2

# Life Span Constants (30 to 180 seconds in milliseconds)
MIN_LIFE_SPAN: int = 30000
MAX_LIFE_SPAN: int = 180000

# Physics constants
SPEED_BASE_CONSTANT: float = 100.0
FRICTION: float = 0.995
ACCELERATION_RANGE: Tuple[float, float] = (-0.1, 0.1)
DEFAULT_COLOR_RANGE: Tuple[int, int] = (50, 255)

# AI Behavior Constants
FLEE_RADIUS: float = 150.0
FLEE_FORCE: float = 0.8
CHASE_RADIUS: float = 200.0
CHASE_FORCE: float = 0.5

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

# ============================================================================
# TYPE DEFINITIONS
# ============================================================================


class Square(TypedDict):
    rect: pygame.Rect
    pos: List[float]
    color: Tuple[int, int, int]
    vel: List[float]
    size: int
    birth_time: int
    life_span: int


class GameState(TypedDict):
    paused: bool
    score: int
    start_time: int
    difficulty: float


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
    pygame.display.set_caption("Lab 11: Chase, Flee, & Lifespan")
    clock = pygame.time.Clock()
    return screen, clock


def create_squares(
    num_squares: int, color_range: Tuple[int, int] = DEFAULT_COLOR_RANGE
) -> List[Square]:
    squares: List[Square] = []
    now: int = pygame.time.get_ticks()

    for _ in range(num_squares):
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

        max_speed = SPEED_BASE_CONSTANT / size
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(max_speed * 0.5, max_speed)

        squares.append(
            {
                "rect": rect,
                "pos": [float(rect.x), float(rect.y)],
                "color": color,
                "vel": [math.cos(angle) * speed, math.sin(angle) * speed],
                "size": size,
                "birth_time": now,
                "life_span": random.randint(MIN_LIFE_SPAN, MAX_LIFE_SPAN),
            }
        )
    return squares


# ============================================================================
# UPDATE LOGIC
# ============================================================================


def handle_events(squares: List[Square], game_state: GameState) -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                squares.extend(create_squares(1))
            elif event.key == pygame.K_p:
                game_state["paused"] = not game_state["paused"]
            elif event.key in (pygame.K_1, pygame.K_KP1):
                game_state["difficulty"] = DIFFICULTY_LEVELS[1]
            elif event.key in (pygame.K_2, pygame.K_KP2):
                game_state["difficulty"] = DIFFICULTY_LEVELS[2]
            elif event.key in (pygame.K_3, pygame.K_KP3):
                game_state["difficulty"] = DIFFICULTY_LEVELS[3]
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for s in reversed(squares):
                if s["rect"].collidepoint(event.pos):
                    squares.remove(s)
                    game_state["score"] += SCORE_INCREMENT
                    break
    return True


def update_squares(squares: List[Square], game_state: GameState) -> None:
    if game_state["paused"]:
        return

    now = pygame.time.get_ticks()
    diff = game_state["difficulty"]

    for square in squares[:]:
        # 1. Lifespan Logic
        if now - square["birth_time"] > square["life_span"]:
            squares.remove(square)
            squares.extend(create_squares(1))
            continue

        # Start with random jitter
        ax = random.uniform(*ACCELERATION_RANGE) * diff
        ay = random.uniform(*ACCELERATION_RANGE) * diff

        cx, cy = (
            square["pos"][0] + square["size"] / 2,
            square["pos"][1] + square["size"] / 2,
        )

        # 2. Chase & Flee Logic
        for other in squares:
            if square is other:
                continue

            ox, oy = (
                other["pos"][0] + other["size"] / 2,
                other["pos"][1] + other["size"] / 2,
            )
            dx, dy = ox - cx, oy - cy
            dist = math.hypot(dx, dy) or 0.1

            # Fleeing (Current square is smaller)
            if square["size"] < other["size"]:
                if dist < FLEE_RADIUS:
                    force = ((FLEE_RADIUS - dist) / FLEE_RADIUS) * FLEE_FORCE
                    ax -= (dx / dist) * force
                    ay -= (dy / dist) * force

            # Chasing (Current square is larger)
            elif square["size"] > other["size"]:
                if dist < CHASE_RADIUS:
                    force = ((CHASE_RADIUS - dist) / CHASE_RADIUS) * CHASE_FORCE
                    ax += (dx / dist) * force
                    ay += (dy / dist) * force

        # Update Velocity
        square["vel"][0] = (square["vel"][0] + ax) * FRICTION
        square["vel"][1] = (square["vel"][1] + ay) * FRICTION

        # Speed Limit
        limit = (SPEED_BASE_CONSTANT / square["size"]) * diff
        curr_v = math.hypot(square["vel"][0], square["vel"][1])
        if curr_v > limit:
            square["vel"][0] *= limit / curr_v
            square["vel"][1] *= limit / curr_v

        # Update Position
        square["pos"][0] += square["vel"][0]
        square["pos"][1] += square["vel"][1]
        square["rect"].topleft = (int(square["pos"][0]), int(square["pos"][1]))

        # Wall Bounce
        if square["rect"].left <= 0 or square["rect"].right >= WIDTH:
            bounce_off_wall(square, "x")
        if square["rect"].top <= 0 or square["rect"].bottom >= HEIGHT:
            bounce_off_wall(square, "y")

    # Pairwise collisions
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
    game_state: GameState,
    font: pygame.font.Font,
    clock: pygame.time.Clock,
) -> None:
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, TEXT_COLOR)
    count_text = font.render(f"Squares: {len(squares)}", True, TEXT_COLOR)
    score_text = font.render(f"Score: {game_state['score']}", True, TEXT_COLOR)
    timer = (pygame.time.get_ticks() - game_state["start_time"]) // 1000
    timer_text = font.render(f"Time: {timer}s", True, TEXT_COLOR)
    diff_text = font.render(
        f"Difficulty: {game_state['difficulty']}x", True, TEXT_COLOR
    )

    screen.blit(fps_text, (TEXT_OFFSET_X, TEXT_OFFSET_X))
    screen.blit(count_text, (TEXT_OFFSET_X, TEXT_OFFSET_X + TEXT_LINE_HEIGHT))
    screen.blit(score_text, (TEXT_OFFSET_X, TEXT_OFFSET_X + TEXT_LINE_HEIGHT * 2))
    screen.blit(timer_text, (TEXT_OFFSET_X, TEXT_OFFSET_X + TEXT_LINE_HEIGHT * 3))
    screen.blit(diff_text, (TEXT_OFFSET_X, TEXT_OFFSET_X + TEXT_LINE_HEIGHT * 4))

    if game_state["paused"]:
        p_font = pygame.font.SysFont(None, PAUSE_FONT_SIZE)
        p_text = p_font.render("PAUSED", True, PAUSE_TEXT_COLOR)
        screen.blit(
            p_text,
            (
                WIDTH // 2 - p_text.get_width() // 2,
                HEIGHT // 2 - p_text.get_height() // 2,
            ),
        )


def render(
    screen: pygame.Surface,
    squares: List[Square],
    game_state: GameState,
    font: pygame.font.Font,
    clock: pygame.time.Clock,
    bg_image: Optional[pygame.Surface] = None,
) -> None:
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(BG_COLOR)

    for s in squares:
        pygame.draw.rect(screen, s["color"], s["rect"])
        pygame.draw.rect(screen, SQUARE_OUTLINE_COLOR, s["rect"], SQUARE_OUTLINE_WIDTH)

    render_text_overlays(screen, squares, game_state, font, clock)
    pygame.display.flip()


# ============================================================================
# MAIN
# ============================================================================


def main() -> None:
    screen, clock = init_pygame()
    font = pygame.font.SysFont(None, FONT_SIZE)

    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill(BG_BASE_COLOR)
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(bg, BG_GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(bg, BG_GRID_COLOR, (0, y), (WIDTH, y))

    squares = create_squares(NUM_SQUARES)
    game_state: GameState = {
        "paused": False,
        "score": 0,
        "start_time": pygame.time.get_ticks(),
        "difficulty": 1.0,
    }

    running = True
    while running:
        running = handle_events(squares, game_state)
        update_squares(squares, game_state)
        render(screen, squares, game_state, font, clock, bg_image=bg)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
