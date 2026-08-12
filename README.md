# Pygame Predator–Prey Simulation

A real-time Pygame simulation of autonomous agents with predator–prey steering, lifespan management, rebirth, collision handling, and interactive difficulty controls.

## Features

- Real-time 60 FPS simulation
- Size-based predator–prey behavior
- Distance-weighted chase and flee steering
- Individual entity lifespans
- Automatic rebirth of expired entities
- Velocity, acceleration, friction, and wall-bounce physics
- Collision response
- Score and simulation HUD
- Pause and difficulty controls
- Mouse interaction for removing entities

## Controls

| Key / Input | Action |
|---|---|
| `P` | Pause / resume |
| `Space` | Spawn an additional square |
| `1` | Difficulty 1.0× |
| `2` | Difficulty 1.5× |
| `3` | Difficulty 2.0× |
| Left click | Remove a square and gain score |
| Window close | Exit |

## Requirements

- Python 3.10+
- Pygame

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Technical Concepts

The simulation uses frame-based updates and `pygame.time.get_ticks()` for per-entity lifecycle tracking. Smaller entities flee from larger nearby entities, while larger entities chase smaller ones. Steering strength is weighted by distance to create more responsive interactions.

## Project Structure

```text
.
├── main.py
├── requirements.txt
├── test_main.py
└── README.md
```

## Future Improvements

- Predictive interception for smarter pursuit
- Configurable spawn and lifespan profiles
- Expanded automated tests for steering edge cases
- Performance improvements for larger populations

## License

Educational project.