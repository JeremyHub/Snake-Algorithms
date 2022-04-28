# How to play
Run the main.py file. It is setup to play games (visually) where the path AI is controlling the snake.
If you want to play the game for yourself, change the "running_type" variable to "human" rather than "ai".
If you want the tail AI to play the game, change the ai_type to "tail".
If you want it to run conccurently without drawing, change the use_pypy to True and run the main with pypy (or normally but its much slower).
Libraries used: multiprocessing, pygame, plotille.

# What we did
We made an algorithm that plays snake and wins 100% of the time.
Obviously that on its own is faily boring, so we also made it able to sometimes cut off blocks of the path so that it doesnt just always follow the pre-determined hamiltonian path.
