##Exercise 1: Mix of Squares
I will change my create_single_square() function so it can take a size number. In main(), I will delete the simple loop. I will make three new loops: 
    - 5 squares with 25px size
    - 10 squares with 10px size
    - 30 squares with 4px size

##Exercise 2: Same Size Respawn
In the update_simulation function, when a square is too old and dies, I need to save its size. Then I pass this size to create_single_square(size=sq['size']). This way, the new square is the same size as the old one.
