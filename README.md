# Pygame Lab 11: Chase, Flee, and Lifespan

A real-time Pygame simulation where autonomous squares exhibit predator-prey behavior, age over time, and are reborn after reaching their lifespan.

## Overview

This project demonstrates:
- Real-time animation and frame-based updates
- Predator-prey steering based on size hierarchy
- Per-object lifespan tracking using millisecond timers
- Automatic rebirth of expired entities
- Keyboard and mouse interactivity
- Difficulty scaling and pause control

## Features

- Randomly generated squares with:
  - Variable size
  - Random color
  - Independent velocity and acceleration
  - Individual life span
- Predator-prey hierarchy:
  - Smaller squares flee from larger squares within a flee radius
  - Larger squares chase smaller squares within a chase radius
  - Steering force scales with distance (stronger when closer)
- Life Span + Rebirth system:
  - Each square stores its own birth time
  - Age is computed in the update loop
  - When age exceeds life span, the square is removed and a new square is spawned
- Movement behavior:
  - Random acceleration jitter to avoid perfectly deterministic paths
  - Friction-based damping
  - Speed caps based on size (smaller squares can move faster)
  - Wall bounce handling
  - Basic collision response between squares
- HUD display:
  - FPS
  - Number of active squares
  - Score
  - Elapsed timer
  - Current difficulty multiplier
  - Pause overlay

## Controls

- P: Pause or resume simulation
- Space: Spawn one additional square
- 1: Set difficulty to 1.0x
- 2: Set difficulty to 1.5x
- 3: Set difficulty to 2.0x
- Left Mouse Click: Remove a clicked square and gain score
- Window Close: Exit the game

## Predator-Prey Logic

Each square checks nearby squares and compares size:
- If current square is smaller, it applies a flee acceleration away from bigger neighbors.
- If current square is larger, it applies a chase acceleration toward smaller neighbors.
- Force magnitude is distance-weighted:
  - Flee: `((FLEE_RADIUS - dist) / FLEE_RADIUS) * FLEE_FORCE`
  - Chase: `((CHASE_RADIUS - dist) / CHASE_RADIUS) * CHASE_FORCE`

This creates an emergent hierarchy where big squares pressure small ones while small ones attempt to escape.

## Lifespan + Rebirth Logic

Each square has two lifespan fields:
- birth_time: Timestamp (milliseconds) when the square was created
- life_span: Randomized duration (milliseconds) the square may live

During each update:
1. current_time is read from pygame.time.get_ticks()
2. age is evaluated as current_time - birth_time
3. If age exceeds life_span:
   - remove the old square
   - immediately spawn a replacement square

This keeps the simulation population continuously renewing over time.

## Project Structure

- main.py: Core game loop, event handling, AI steering simulation, lifespan rebirth, and rendering
- requirements.txt: Python dependencies
- test_main.py: Automated tests (if present in your workflow)

## Requirements

- Python 3.10+
- pygame

## Run

Install dependencies:

pip install -r requirements.txt

Start the game:

python main.py

## Notes

- Timing uses milliseconds from pygame.time.get_ticks(), which is suitable for per-entity lifecycle tracking in a frame loop.
- Lifespan constants are configured in milliseconds for consistency.
- Pause mode freezes simulation updates, including lifespan progression.
- Difficulty multiplier scales acceleration and speed cap pressure, making chase/flee interactions more intense at higher levels.

## Future Improvements

- Add predictive interception (lead pursuit) for smarter predator behavior
- Add steering force caps per frame to reduce swarm spikes in dense clusters
- Add configurable spawn profiles and lifespan presets
- Add automated tests for chase/flee edge cases and collision overlap handling

## License

Use according to your course or repository policy.