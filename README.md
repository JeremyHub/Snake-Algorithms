# How to play
Run the snake.py file. It is setup to play 100 games (visually) where the AI is controlling the snake.
If you want to play the game for yourself, change the "running_type" variable to "human" rather than "ai".
It will automatically create a debug file everytime you run the code (overwriting any previous log file). You can turn this off by changing the global variable at the top of the snake_ai.py file.

# Results
The algorithm is faily good. It is also fairly expensive to run, especially on large boards.
To test the algorithm I ran it a few hundred times on a board of 10x10.
There was a move limit of 2300 ((board_size**3) * 2.3), if it exeeded the move limit and had not won the game yet, it moved on to the next game.
The average board coverage was 95%, and the average win rate was ~20%.
As you can tell from the above numbers, the algorithm struggles to get the last few foods but is quite consitent in reaching that point.

# How the AI works
It has a lot of logic in it that is hard to explain but the code is commented with reasons for most descisions listed, so check out the code.
Esentially, it is based on the principle of keeping the tail in sight at all times.
As long as the tail is in sight at all times, the snake will never die (it will never make a move that leads to a situation in which the tail is not in sight or the head intersects the body or a wall).
At any point, there are many directions that fit the above condition, so the task then is to choose the best direction.
First and foremost, direction chosen will be the direction that goes in the direction of the snake.
If there is no path to the food, it will choose the direction that is opposite of the food (this is to free up space near the food so that when it loops around it will be able to get it).
There are also optimizations to favor directions that stick close to the body of the snake as well as directions that dont create voids (squares that the head cant get to).
There are many further optimizations to prevent the snake from getting stuck in loops, even so, it does happen about 1-2% of the time (before ~90% coverage of the board).
