# Pygame Lab 8: Life Span and Rebirth

A real-time Pygame simulation where colorful squares move with dynamic behavior, age over time, and are reborn after reaching their lifespan.

## Overview

This project demonstrates:
- Real-time animation and frame-based updates
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
- Life Span + Rebirth system:
  - Each square stores its own birth time
  - Age is computed in the update loop
  - When age exceeds life span, the square is removed and a new square is spawned
- Movement behavior:
  - Random acceleration
  - Friction-based damping
  - Speed caps based on size
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

## Life Span + Rebirth Logic

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

- main.py: Core game loop, event handling, simulation, and rendering
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

## Future Improvements

- Replace dictionary-based square data with dataclass or TypedDict for stronger typing
- Add configurable spawn profiles and lifespan presets
- Add automated tests for expiry and rebirth edge cases
- Add sound and visual effects for rebirth events

## License

Use according to your course or repository policy.