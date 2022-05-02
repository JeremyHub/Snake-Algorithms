# How to play
Run the main.py file. It is setup to play games (visually) where the path AI is controlling the snake.\\
If you want to play the game for yourself, change the "running_type" variable to "human" rather than "ai".\\
If you want it to run conccurently without drawing, change the use_pypy to True and run the main with pypy (or normally but its much slower).\\
Libraries used: multiprocessing, pygame, plotille.
\\\\
# What we did
We made an algorithm that plays snake and wins 100% of the time.\\
Obviously that on its own is faily boring, so we also made it able to sometimes cut off blocks of the path so that it doesnt just always follow the pre-determined hamiltonian path. On a 12x11 board it finishes in an average moves of ~4875, where the expected if you only followed the hamiltonian path would be ~8500, so we got some optimization out of our approach.
