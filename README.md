# Lab 8: Random Moving Squares

A simple Python application built with Pygame for Lab 8. This project features a window with squares of random sizes and colors that bounce off the walls. 

## Features
* **Bouncing Physics:** Squares move around and bounce off the edges of the screen.
* **Interactive:** You can click on the squares to destroy them and earn points.
* **Physics:** Includes basic gravity and friction that you can adjust.

## Controls
* **Left Click:** Destroy a square (and get +10 points!)
* **Spacebar:** Add a new random square to the screen.
* **P:** Pause or unpause the game.
* **F:** Toggle Fullscreen mode.
* **1, 2, 3:** Change the gravity/difficulty level (1 is normal, 3 is heavy).

## How to Run the Project

**1. Install Pygame**
Make sure you have Pygame installed. We recommend the Community Edition (`pygame-ce`) for better compatibility, especially on Macs. Open your terminal and run:
```bash
pip install -r requirements.txt
```

**2. Start the Game**
Run the main Python file to start the application:
```bash
python main.py
```
*(Note: You might need to use `python3` or `pip3` depending on your setup).*

## About the Code
This project was built to practice the standard Pygame loop:
1. Handling User Events (Clicks and Keypresses)
2. Updating Game Logic (Math, movement, and collisions)
3. Rendering (Drawing the background and shapes to the screen)