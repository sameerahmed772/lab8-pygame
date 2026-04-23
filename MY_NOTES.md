## Project: Pygame Moving Squares

### New Feature: Life Span and Rebirth

**What is the idea?**
I want to make the squares "live" and "die." Each square is like a little person. It is born, it moves for a short time, and then it goes away. When one square goes away, a new square is born immediately. This keeps the number of squares the same.

**How to do it?**
1.  **Give them a timer:** When I create a square, I will give it a "birthday" (the time it starts) and a "life span" (how many seconds it stays on the screen).
2.  **Random numbers:** The life span is not the same for every square. Some live for 30 seconds, and some live for 180 seconds. I will use `random.randint` for this.
3.  **Check the age:** In every frame of the game, I will check the age. If "Current Time - Birthday > Life Span," the square dies.
4.  **Rebirth:** When the square is removed from the list, I will call the `create_squares(1)` function. This makes a new square in a random place.

**Why is this good?**
The game looks more active. The colors and sizes of the squares change over time because old ones die and new ones appear.

**Coding Reminders:**
* Use milliseconds for the timer (1 second = 1000ms).
* Add `birth_time` and `life_span` to the dictionary.
* Don't forget **Type Hints** like `: int` or `: Dict`.
* Test the timer in the REPL to make sure it works before adding it to the game.

I've drafted the notes for your **Flee** and **Chase** features using the exact same format and A2-level English. This will look perfect in your `MY_Notes.md` alongside the Life Span section.

---

### New Feature: Fleeing Behavior (Run Away)

**What is the idea?**
I want the small squares to be "scared" of the big squares. If a big square comes close, the small square should detect the danger and run away in the opposite direction. This makes the squares look like they are alive.

**How to do it?**
1.  **Check the distance:** For every square, I look at the other squares. I use `math.hypot` to find the distance between them.
2.  **Size comparison:** If "My Size < Other Size," then the other square is a predator.
3.  **The Flee Zone:** I use a `FLEE_RADIUS` (like 150 pixels). If the distance is smaller than this radius, the square starts to flee.
4.  **Opposite Vector:** I calculate the direction from the big square to the small one. I add this "push" to the small square's acceleration so it moves away.

**Why is this good?**
It adds "AI" to the game. Instead of just bouncing randomly, the squares react to each other. It creates a "prey" behavior that looks very natural.

**Coding Reminders:**
* Use a unit vector (`dx / dist`) so the flee speed is smooth.
* Use a `FLEE_FORCE` constant to control how fast they run.
* Only flee from squares that are bigger, not the same size.


### New Feature: Chasing Behavior (The Hunter)

**What is the idea?**
The big squares are now "predators." When they see a smaller square nearby, they don't just move randomly—they actively try to follow and "catch" the smaller square. 

**How to do it?**
1.  **Identify the prey:** If "My Size > Other Size," the current square is a hunter and the other is the target.
2.  **The Chase Zone:** I use a `CHASE_RADIUS`. Predators have "eyes" and can see prey within this distance.
3.  **Target Vector:** I calculate the direction from the big square toward the small square's center.
4.  **Apply Force:** I add this direction vector to the big square's acceleration. This "pulls" the big square toward its prey.

**Why is this good?**
It completes the ecosystem. Now you have a real "cat and mouse" game happening on the screen. It makes the simulation much more interesting to watch.

**Coding Reminders:**
* The `CHASE_RADIUS` should be a bit bigger than the flee radius so hunters can find targets.
* Don't forget the **Speed Limit**. If a big square chases too many things, it might move too fast!
* Use `math.atan2` or simple vector addition to get the direction.
