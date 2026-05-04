import pygame
import random
import math
from typing import List, Tuple, Optional, TypedDict

# ============================================================================
# CONSTANTS
# ============================================================================
# Using named constants avoids "magic numbers," making the game rules
# easy to find and modify in one place.
WIDTH, HEIGHT = 800, 600
FPS = 60

# Square properties
SIZE_RANGE = (15, 80)
NUM_SQUARES = 15
OUTLINE_WIDTH = 2

# Lifespan in milliseconds (30s to 180s)
LIFESPAN_RANGE = (30000, 180000)

# Physics & AI
FRICTION = 0.995
JITTER_RANGE = (-0.1, 0.1)
FLEE_RADIUS, FLEE_FORCE = 150.0, 0.8
CHASE_RADIUS, CHASE_FORCE = 200.0, 0.5
BASE_SPEED_FACTOR = 100.0  # Speed is inversely proportional to size

# Visuals
COLOR_MIN_MAX = (50, 255)
BG_BASE = (20, 25, 30)
BG_GRID = (35, 40, 45)
GRID_STEP = 40
UI_COLOR = (255, 255, 255)
PAUSE_COLOR = (255, 50, 50)

# Gameplay
DIFFICULTY_MODS = {pygame.K_1: 1.0, pygame.K_2: 1.5, pygame.K_3: 2.0}
SCORE_VAL = 100

# ============================================================================
# DATA MODELS
# ============================================================================


class Square(TypedDict):
    """
    TypedDict describes the 'shape' of our data.
    This helps beginners see exactly what attributes a 'Square' has.
    """

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
# HELPER FUNCTIONS (Decomposition)
# ============================================================================


def create_single_square(fixed_size: Optional[int] = None) -> Square:
    """
    Factory function: Encapsulates the logic of creating one object.
    Separation of concerns: main logic doesn't need to know how to build a square.
    """
    size = fixed_size if fixed_size is not None else random.randint(*SIZE_RANGE)
    x = random.randint(0, WIDTH - size)
    y = random.randint(0, HEIGHT - size)

    # Speed logic: Smaller squares move faster (inversely proportional)
    max_v = BASE_SPEED_FACTOR / size
    angle = random.uniform(0, 2 * math.pi)
    speed = random.uniform(max_v * 0.5, max_v)

    return {
        "rect": pygame.Rect(x, y, size, size),
        "pos": [float(x), float(y)],
        "color": (
            random.randint(*COLOR_MIN_MAX),
            random.randint(*COLOR_MIN_MAX),
            random.randint(*COLOR_MIN_MAX),
        ),
        "vel": [math.cos(angle) * speed, math.sin(angle) * speed],
        "size": size,
        "birth_time": pygame.time.get_ticks(),
        "life_span": random.randint(*LIFESPAN_RANGE),
    }


def handle_wall_collision(square: Square):
    """Resets position to boundary and reverses velocity to prevent sticking."""
    if square["rect"].left <= 0 or square["rect"].right >= WIDTH:
        square["pos"][0] = float(square["rect"].x)
        square["vel"][0] *= -1
    if square["rect"].top <= 0 or square["rect"].bottom >= HEIGHT:
        square["pos"][1] = float(square["rect"].y)
        square["vel"][1] *= -1


def apply_steering(
    sq: Square, other: Square, ax: float, ay: float
) -> Tuple[float, float]:
    """
    Calculates Chase/Flee vectors.
    Abstracting this reduces 'noise' in the main update loop.
    """
    dx = (other["pos"][0] + other["size"] / 2) - (sq["pos"][0] + sq["size"] / 2)
    dy = (other["pos"][1] + other["size"] / 2) - (sq["pos"][1] + sq["size"] / 2)
    dist = math.hypot(dx, dy) or 0.1

    # Fleeing: Smaller flees from larger
    if sq["size"] < other["size"] and dist < FLEE_RADIUS:
        force = ((FLEE_RADIUS - dist) / FLEE_RADIUS) * FLEE_FORCE
        ax -= (dx / dist) * force
        ay -= (dy / dist) * force
    # Chasing: Larger chases smaller
    elif sq["size"] > other["size"] and dist < CHASE_RADIUS:
        force = ((CHASE_RADIUS - dist) / CHASE_RADIUS) * CHASE_FORCE
        ax += (dx / dist) * force
        ay += (dy / dist) * force

    return ax, ay


# ============================================================================
# CORE GAME LOGIC
# ============================================================================


def update_simulation(squares: List[Square], state: GameState):
    """The 'Brain' of the app: Updates state based on rules."""
    if state["paused"]:
        return

    now = pygame.time.get_ticks()
    diff = state["difficulty"]

    for sq in squares[:]:
        # 1. Lifespan check
        if now - sq["birth_time"] > sq["life_span"]:
            squares.remove(sq)
            squares.append(create_single_square())
            continue

        # 2. Physics & AI Steering
        ax = random.uniform(*JITTER_RANGE) * diff
        ay = random.uniform(*JITTER_RANGE) * diff

        for other in squares:
            if sq is not other:
                ax, ay = apply_steering(sq, other, ax, ay)

        # Apply Acceleration & Friction
        sq["vel"][0] = (sq["vel"][0] + ax) * FRICTION
        sq["vel"][1] = (sq["vel"][1] + ay) * FRICTION

        # Speed Limiting
        limit = (BASE_SPEED_FACTOR / sq["size"]) * diff
        curr_speed = math.hypot(*sq["vel"])
        if curr_speed > limit:
            sq["vel"] = [(v / curr_speed) * limit for v in sq["vel"]]

        # 3. Position Update
        sq["pos"][0] += sq["vel"][0]
        sq["pos"][1] += sq["vel"][1]
        sq["rect"].topleft = (int(sq["pos"][0]), int(sq["pos"][1]))

        handle_wall_collision(sq)

    # 4. Simple Elastic Collision (Swap velocities on hit)
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


def draw_ui(
    screen: pygame.Surface,
    squares: List[Square],
    state: GameState,
    font: pygame.font.Font,
    clock: pygame.time.Clock,
):
    """Separation of concerns: Handles all text/HUD elements separately from game world."""
    elapsed = (pygame.time.get_ticks() - state["start_time"]) // 1000

    # List of strings to render dynamically
    stats = [
        f"FPS: {int(clock.get_fps())}",
        f"Squares: {len(squares)}",
        f"Score: {state['score']}",
        f"Time: {elapsed}s",
        f"Difficulty: {state['difficulty']}x",
    ]

    for i, text in enumerate(stats):
        img = font.render(text, True, UI_COLOR)
        screen.blit(img, (10, 10 + i * 25))

    if state["paused"]:
        p_font = pygame.font.SysFont(None, 72)
        p_img = p_font.render("PAUSED", True, PAUSE_COLOR)
        rect = p_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(p_img, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab 8: Pygame Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # Pre-render grid background for performance
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill(BG_BASE)
    for x in range(0, WIDTH, GRID_STEP):
        pygame.draw.line(bg, BG_GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_STEP):
        pygame.draw.line(bg, BG_GRID, (0, y), (WIDTH, y))

    squares: List[Square] = []
    # Exercise 1: A Mix of Squares
    for _ in range(5):
        squares.append(create_single_square(25))
    for _ in range(10):
        squares.append(create_single_square(10))
    for _ in range(30):
        squares.append(create_single_square(4))

    state: GameState = {
        "paused": False,
        "score": 0,
        "start_time": pygame.time.get_ticks(),
        "difficulty": 1.0,
    }

    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    state["paused"] = not state["paused"]
                if event.key == pygame.K_SPACE:
                    squares.append(create_single_square())
                if event.key in DIFFICULTY_MODS:
                    state["difficulty"] = DIFFICULTY_MODS[event.key]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Remove squares from top (last drawn) to bottom
                for s in reversed(squares):
                    if s["rect"].collidepoint(event.pos):
                        squares.remove(s)
                        state["score"] += SCORE_VAL
                        break

        # Logic & Rendering
        update_simulation(squares, state)

        screen.blit(bg, (0, 0))
        for s in squares:
            pygame.draw.rect(screen, s["color"], s["rect"])
            pygame.draw.rect(screen, UI_COLOR, s["rect"], OUTLINE_WIDTH)

        draw_ui(screen, squares, state, font, clock)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
