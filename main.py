import pygame
import random
from typing import List, Dict, Tuple, Optional

# ============================================================================
# CONSTANTS
# ============================================================================
WIDTH: int = 800
HEIGHT: int = 600
SQUARE_SIZE: int = 40
FPS: int = 60
NUM_SQUARES: int = 10

# Type alias for clarity
Square = Dict[
    str, any
]  # {"rect": Rect, "pos": List[float], "color": Tuple, "vel": List[float]}


# ============================================================================
# INITIALIZATION
# ============================================================================


def init_pygame(fullscreen: bool = False) -> Tuple[pygame.Surface, pygame.time.Clock]:
    """
    Initialize Pygame and return the screen and clock objects.
    """
    try:
        pygame.init()
        # Ensure fonts are initialized for the text overlay
        pygame.font.init()

        flags = pygame.FULLSCREEN if fullscreen else 0
        screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        pygame.display.set_caption("Lab 8: Random Moving Squares")
        clock = pygame.time.Clock()

        return screen, clock
    except pygame.error as e:
        print(f"Critical Error: Failed to initialize Pygame display. Details: {e}")
        raise SystemExit


def create_squares(
    num_squares: int,
    color_range: Tuple[int, int] = (50, 255),
    vel_range: Tuple[float, float] = (-3.0, 3.0),
) -> List[Square]:
    """
    Create a list of square dictionaries with random positions, colors, and velocities.
    """
    if num_squares <= 0:
        raise ValueError("Parameter num_squares must be greater than 0.")

    squares = []
    for _ in range(num_squares):
        rect = pygame.Rect(
            random.randint(0, WIDTH - SQUARE_SIZE),
            random.randint(0, HEIGHT - SQUARE_SIZE),
            SQUARE_SIZE,
            SQUARE_SIZE,
        )
        color = (
            random.randint(*color_range),
            random.randint(*color_range),
            random.randint(*color_range),
        )

        # Ensure initial velocity isn't zero
        vel_x, vel_y = 0.0, 0.0
        while vel_x == 0.0:
            vel_x = random.uniform(*vel_range)
        while vel_y == 0.0:
            vel_y = random.uniform(*vel_range)

        squares.append(
            {
                "rect": rect,
                "pos": [
                    float(rect.x),
                    float(rect.y),
                ],  # Float position for accurate friction/acceleration math
                "color": color,
                "vel": [vel_x, vel_y],
            }
        )
    return squares


# ============================================================================
# UPDATE LOGIC
# ============================================================================


def handle_events(squares: List[Square], game_state: Dict[str, any]) -> bool:
    """
    Handle all pygame events.

    Returns:
        False if quit event detected, True otherwise
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.KEYDOWN:
            # Spacebar to add a new square
            if event.key == pygame.K_SPACE:
                squares.extend(create_squares(1))
            # 'P' to pause/resume
            elif event.key == pygame.K_p:
                game_state["paused"] = not game_state["paused"]
            # 1, 2, 3 for difficulty levels
            elif event.key == pygame.K_1:
                game_state["difficulty"] = 1.0
            elif event.key == pygame.K_2:
                game_state["difficulty"] = 1.5
            elif event.key == pygame.K_3:
                game_state["difficulty"] = 2.0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Left click to remove squares and increase score
            if event.button == 1:
                mouse_pos = event.pos
                for s in squares[:]:
                    if s["rect"].collidepoint(mouse_pos):
                        squares.remove(s)
                        game_state["score"] += 100

    return True


def update_squares(squares: List[Square], game_state: Dict[str, any]) -> None:
    """
    Update square positions, handle wall bouncing, collision, friction, and acceleration.
    """
    if game_state["paused"]:
        return

    diff_multiplier = game_state["difficulty"]

    for square in squares:
        # 1. Apply constant acceleration (a slight random drift)
        accel_x = random.uniform(-0.1, 0.1) * diff_multiplier
        accel_y = random.uniform(-0.1, 0.1) * diff_multiplier
        square["vel"][0] += accel_x
        square["vel"][1] += accel_y

        # 2. Apply friction/deceleration
        friction = 0.995
        square["vel"][0] *= friction
        square["vel"][1] *= friction

        # 3. Move square using float positions for accuracy
        square["pos"][0] += square["vel"][0] * diff_multiplier
        square["pos"][1] += square["vel"][1] * diff_multiplier

        # Sync rect to float position
        square["rect"].x = int(square["pos"][0])
        square["rect"].y = int(square["pos"][1])

        # 4. Bounce off walls
        if square["rect"].left <= 0:
            square["rect"].left = 0
            square["pos"][0] = float(square["rect"].x)
            square["vel"][0] *= -1
        elif square["rect"].right >= WIDTH:
            square["rect"].right = WIDTH
            square["pos"][0] = float(square["rect"].x)
            square["vel"][0] *= -1

        if square["rect"].top <= 0:
            square["rect"].top = 0
            square["pos"][1] = float(square["rect"].y)
            square["vel"][1] *= -1
        elif square["rect"].bottom >= HEIGHT:
            square["rect"].bottom = HEIGHT
            square["pos"][1] = float(square["rect"].y)
            square["vel"][1] *= -1

    # 5. Collision detection between squares (AABB)
    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            if squares[i]["rect"].colliderect(squares[j]["rect"]):
                # Simple elastic collision: swap velocities
                squares[i]["vel"], squares[j]["vel"] = (
                    squares[j]["vel"],
                    squares[i]["vel"],
                )

                # Push apart slightly to prevent getting stuck inside each other
                squares[i]["pos"][0] += squares[i]["vel"][0]
                squares[i]["pos"][1] += squares[i]["vel"][1]


# ============================================================================
# RENDERING
# ============================================================================


def render(
    screen: pygame.Surface,
    squares: List[Square],
    game_state: Dict[str, any],
    font: pygame.font.Font,
    clock: pygame.time.Clock,
    bg_image: Optional[pygame.Surface] = None,
) -> None:
    """
    Render all squares, backgrounds, outlines, and text overlays to the screen.
    """
    # 1. Background rendering
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((30, 30, 30))  # Clear screen with dark grey

    # 2. Square rendering
    for square in squares:
        # Fill
        pygame.draw.rect(screen, square["color"], square["rect"])
        # Outline/Border (White, 2px thick)
        pygame.draw.rect(screen, (255, 255, 255), square["rect"], 2)

    # 3. Text Overlay Rendering
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    count_text = font.render(
        f"Squares: {len(squares)} (Press SPACE to add)", True, (255, 255, 255)
    )
    score_text = font.render(
        f"Score: {game_state['score']} (Click squares)", True, (255, 255, 255)
    )

    # Calculate elapsed timer
    elapsed_seconds = (pygame.time.get_ticks() - game_state["start_time"]) // 1000
    timer_text = font.render(f"Timer: {elapsed_seconds}s", True, (255, 255, 255))

    diff_text = font.render(
        f"Difficulty [1,2,3]: {game_state['difficulty']}x", True, (255, 255, 255)
    )

    screen.blit(fps_text, (10, 10))
    screen.blit(count_text, (10, 35))
    screen.blit(score_text, (10, 60))
    screen.blit(timer_text, (10, 85))
    screen.blit(diff_text, (10, 110))

    if game_state["paused"]:
        pause_font = pygame.font.SysFont(None, 72)
        pause_text = pause_font.render("PAUSED", True, (255, 50, 50))
        screen.blit(
            pause_text,
            (
                WIDTH // 2 - pause_text.get_width() // 2,
                HEIGHT // 2 - pause_text.get_height() // 2,
            ),
        )

    pygame.display.flip()


# ============================================================================
# MAIN GAME LOOP
# ============================================================================


def main() -> None:
    """
    Main game loop orchestration.
    """
    screen, clock = init_pygame(fullscreen=False)

    # Initialize font system
    font = pygame.font.SysFont(None, 24)

    # Create a procedural background surface to satisfy the bg image requirement
    bg_surface = pygame.Surface((WIDTH, HEIGHT))
    bg_surface.fill((20, 25, 30))
    # Draw a subtle grid on the background
    for x in range(0, WIDTH, 40):
        pygame.draw.line(bg_surface, (35, 40, 45), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(bg_surface, (35, 40, 45), (0, y), (WIDTH, y))

    squares = create_squares(NUM_SQUARES)

    # State management dictionary
    game_state = {
        "paused": False,
        "score": 0,
        "start_time": pygame.time.get_ticks(),
        "difficulty": 1.0,  # Multiplier for movement
    }

    running = True
    while running:
        # A. Event Handling
        running = handle_events(squares, game_state)

        # B. Update Logic
        update_squares(squares, game_state)

        # C. Rendering
        render(screen, squares, game_state, font, clock, bg_image=bg_surface)

        # D. Maintain frame rate
        clock.tick(FPS)

    pygame.quit()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
