## Project: Pygame Moving Squares - Part III

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