# Lab 8: Random Moving Squares

A Python game built with Pygame featuring size-based movement, fleeing behavior, collisions, and interactive gameplay.

## Features
- **Size-Dependent Speed:** Each square has a random size and a max speed computed from its size
- **Fleeing Behavior:** Smaller squares steer away from larger nearby squares
- **Randomized Trajectories:** All squares keep natural drift through random acceleration
- **Physics Engine:** Realistic bouncing, friction, acceleration, and collision detection
- **Interactive Gameplay:** Click squares to destroy them and earn points
- **Difficulty Levels:** Adjust game speed with keyboard controls
- **Pause System:** Pause and resume at any time
- **UI Overlay:** Real-time display of FPS, score, timer, and game state
- **Procedural Background:** Grid-based background for visual polish

## Controls
| Control | Action |
|---------|--------|
| **Left Click** | Destroy a square and earn +100 points |
| **SPACE** | Add a new random square to the screen |
| **P** | Pause or unpause the game |
| **1** | Set difficulty to Normal (1.0x) |
| **2** | Set difficulty to Hard (1.5x) |
| **3** | Set difficulty to Extreme (2.0x) |

## How to Run

### Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the Game
```bash
python main.py
```
*(Note: You may need to use `python3` depending on your setup)*

### Run Tests
```bash
pytest test_main.py -v
```

## Project Structure
```
lab8-pygame/
├── main.py              # Main game code with physics and rendering
├── test_main.py         # Pytest suite for game logic
├── requirements.txt     # Project dependencies
├── README.md           # This file
└── JOURNAL.md          # Development log
```

## Code Architecture

The project follows the standard **Pygame Game Loop** pattern:

1. **Event Handling** (`handle_events`)
   - Process user input (mouse clicks, keyboard)
   - Update game state

2. **Game Logic** (`update_squares`)
   - Apply random acceleration and fleeing acceleration
   - Enforce size-based speed caps
   - Handle wall bouncing
   - Detect square-to-square collisions

3. **Rendering** (`render` + `render_text_overlays`)
   - Draw background and squares
   - Render UI text overlays

4. **Frame Rate Management**
   - Maintain consistent 60 FPS

## Physics Implementation

- **Friction:** 0.995 multiplier per frame (gradual velocity decay)
- **Acceleration:** Random drift (-0.1 to +0.1) per frame
- **Fleeing:** Smaller squares repel from larger squares inside `FLEE_RADIUS`
- **Collision:** Simple elastic collision via velocity swapping
- **Wall Bouncing:** Velocity reversal at screen boundaries

## Size-Speed Model

Squares now use an inverse size-to-speed relationship:

- Square size range: 15 to 80 pixels
- Max speed formula: `max_speed = SPEED_BASE_CONSTANT / size`
- Current base constant: `SPEED_BASE_CONSTANT = 100.0`
- Initial speed is randomized in `[0.5 * max_speed, max_speed]`

This means smaller squares are naturally faster, while larger squares move more slowly.

## Testing

Tests use pytest with mocked pygame to avoid display dependencies:
```bash
pytest test_main.py -v        # Verbose output
pytest test_main.py -q        # Quiet output
pytest test_main.py::test_*   # Run specific test pattern
```

Recommended focus areas for movement logic:
- Unit tests for fleeing direction (distance from larger squares should increase)
- Deterministic tests with patched randomness to avoid flaky results
- Invariant checks (speed cap respected, squares remain in bounds)

## Dependencies

- **pygame-ce** (Community Edition) — Cross-platform game development library
- **pytest** — Testing framework

## Learning Outcomes

After completing this project, you'll understand:
- Pygame initialization and the main game loop
- Event-driven programming patterns
- Physics simulation basics
- Type hints and mypy compliance
- Test-driven development practices
- Code organization and refactoring

## Development Notes

All physics constants, colors, and UI parameters are defined at the top of `main.py` for easy customization. See the `# CONSTANTS` section for adjustable values like screen size, FPS, and physics parameters.