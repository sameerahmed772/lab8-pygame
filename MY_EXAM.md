##Exercise 1: Mix of Squares**
I will change my `create_single_square()` function so it can take a `size` number. In `main()`, I will delete the simple loop. I will make three new loops: 
    - 5 squares with 25px size
    - 10 squares with 10px size
    - 30 squares with 4px size

*##Exercise 2: Same Size Respawn**
In the `update_simulation` function, when a square is too old and dies, I need to save its size. Then I pass this size to `create_single_square(size=sq['size'])`. This way, the new square is the same size as the old one.

##Exercise 3: Screen Wrapping
I have to rewrite `handle_wall_collision`. The squares will not bounce off the walls anymore. If a square goes out one side of the screen, I put it on the other side. The speed stays the same.

##Exercise 4 & 5: Collision Detection & Eating
I will write a new function called `def check_collision(a: Square, b: Square) -> bool:`. It will just return `a["rect"].colliderect(b["rect"])`. I will change the old bounce code. If two squares touch, I check which one is bigger. The big square eats the small square. The small square dies and respawns.

##Exercise 6: Eating++
When the big square eats a small square, the big square gets bigger. I will add a little bit of the small square's size to the big square. I must remember to also update the `pygame.Rect` so the drawing gets bigger too.

##Exercise 7: Trails
I will update the `Square` dictionary to add a `history` list. Every frame, I will add the square's position to this list. If the list is longer than `TRAILS_LENGTH = 30`, I will delete the oldest position. When I draw the game, I will read this history list and use `pygame.draw.line()` to connect the points so it looks like a trail.