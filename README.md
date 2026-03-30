# Lab 8: Random Moving Squares

A simple Python game built with Pygame featuring physics-based movement, collisions, and interactive gameplay. Practice core game development patterns: event handling, game state management, physics simulation, and rendering.

## Features
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
├── test_main.py         # Comprehensive test suite (29 tests)
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
   - Apply physics (acceleration, friction)
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
- **Collision:** Simple elastic collision via velocity swapping
- **Wall Bouncing:** Velocity reversal at screen boundaries

## Testing

The project includes **29 comprehensive tests** covering:
- Square creation (valid counts, color ranges, velocity ranges)
- Physics behavior (wall bouncing, friction, collisions)
- Event handling (pause, difficulty, clicking, adding squares)
- Integration scenarios

Tests use pytest with mocked pygame to avoid display dependencies:
```bash
pytest test_main.py -v        # Verbose output
pytest test_main.py -q        # Quiet output
pytest test_main.py::test_*   # Run specific test pattern
```

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