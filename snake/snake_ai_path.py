import main

debug = main.debug

if debug:
    import os
    from os.path import exists
    import logging
    file_path = "ai_log.txt"
    if exists(file_path):
        os.remove(file_path)
    logging.basicConfig(filename=file_path,
                                filemode='a',
                                format='',
                                datefmt='',
                                level=logging.INFO)

cardinals = {
    (0, 1): 'down',
    (0, -1): 'up',
    (1, 0): 'right',
    (-1, 0): 'left'
}

opposite_directions = dict([(value, key) for key, value in cardinals.items()])

diagnols = {
    (1, 1): ("down", "right"),
    (1, -1): ("up", "right"),
    (-1, 1): ("down", "left"),
    (-1, -1): ("up", "left")
}

def get_action(snake, food, board_size):
    pass