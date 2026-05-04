# Architecture Overview

This project is a single-file Pygame simulation with a companion test suite. The runtime centers on a standard game loop that initializes Pygame, builds the square population, processes input, updates simulation state, and renders the frame.

## Module Dependencies

```mermaid
graph TD
    A["main.py"] --> B["pygame"]
    A --> C["random"]
    A --> D["math"]
    A --> E["typing"]
    F["test_main.py"] --> A
    F --> G["pytest"]
    F --> H["unittest.mock"]
```

`main.py` owns the runtime. `test_main.py` imports the game logic and isolates Pygame behavior with mocks.

## Runtime Flow

```mermaid
graph TD
    A["main()"] --> B["init_pygame()"]
    B --> C["Create window and clock"]
    A --> D["Create background grid surface"]
    A --> E["create_squares(NUM_SQUARES)"]
    A --> F["Initialize game_state"]
    A --> G["Main loop"]
    G --> H["handle_events()"]
    H --> I["QUIT event? return False"]
    H --> J["Keyboard and mouse input"]
    G --> K["update_squares()"]
    K --> L["Lifespan expiration"]
    K --> M["Chase and flee steering"]
    K --> N["Velocity damping and speed cap"]
    K --> O["Wall bounce and collisions"]
    G --> P["render()"]
    P --> Q["Draw background and squares"]
    P --> R["render_text_overlays()"]
    R --> S["FPS, count, score, timer, difficulty, pause"]
    G --> T["clock.tick(FPS)"]
    G --> U["pygame.quit()"]
```

The simulation runs until `handle_events()` returns `False` after a quit event.

## Function Call Graph

```mermaid
graph TD
    A["main()"] --> B["init_pygame()"]
    A --> C["create_squares()"]
    A --> D["handle_events()"]
    A --> E["update_squares()"]
    A --> F["render()"]
    F --> G["render_text_overlays()"]
    E --> H["bounce_off_wall()"]
    D --> C
    E --> C
```

`main()` is the orchestration point. `update_squares()` also calls `create_squares()` when a square expires and needs to be replaced.

## Primary Execution Sequence

```mermaid
sequenceDiagram
    participant M as "main()"
    participant I as "init_pygame()"
    participant C as "create_squares()"
    participant H as "handle_events()"
    participant U as "update_squares()"
    participant R as "render()"
    participant T as "render_text_overlays()"
    participant P as "pygame"

    M->>I: initialize display, font, and clock
    I->>P: pygame.init(), pygame.font.init(), set_mode()
    I-->>M: screen, clock
    M->>C: create initial population
    C-->>M: squares
    M->>M: build game_state and background grid

    loop until quit
        M->>H: poll events
        H->>P: pygame.event.get()
        alt quit event
            H-->>M: False
        else input event
            H->>C: spawn square on Space
            H->>H: toggle pause / set difficulty / remove clicked square
            H-->>M: True
        end

        M->>U: advance simulation
        alt paused
            U-->>M: no state changes
        else active simulation
            U->>P: pygame.time.get_ticks()
            U->>U: lifespan, steering, friction, speed limit, bounce, collisions
            alt square expired
                U->>C: replace expired square
            end
            U-->>M: updated squares
        end

        M->>R: draw frame
        R->>T: draw HUD and pause overlay
        R->>P: pygame.display.flip()
        M->>P: clock.tick(FPS)
    end

    M->>P: pygame.quit()
```

## Data Model

Two typed dictionaries drive the runtime state:

- `Square`: stores `rect`, `pos`, `color`, `vel`, `size`, `birth_time`, and `life_span`.
- `GameState`: stores `paused`, `score`, `start_time`, and `difficulty`.

The simulation keeps `pos` as floats for smooth motion, while `rect` is updated from those floats for collision detection and rendering.

## Notes

- Lifespan checks happen inside the update loop, so expired squares are replaced without stopping the simulation.
- Smaller squares flee larger squares within `FLEE_RADIUS`; larger squares chase smaller squares within `CHASE_RADIUS`.
- Tests focus on creation, event handling, and movement behavior rather than rendering.