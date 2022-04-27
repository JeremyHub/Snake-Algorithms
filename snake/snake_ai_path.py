import main
import helpers
debug = main.debug

if debug:
    import os
    from os.path import exists
    import logging
    file_path = "path_ai_log.txt"
    if exists(file_path):
        os.remove(file_path)
    logging.basicConfig(filename=file_path,
                                filemode='a',
                                format='',
                                datefmt='',
                                level=logging.INFO)


def get_action(snake, food, board_size):
    if debug: logging.info("snake: {}".format(snake))
    if debug: logging.info("food: {}".format(food))
    if debug: logging.info("board_size: {}".format(board_size))

    if not check_hamiltonian(board_size):
        raise Exception("Hamiltonian path is not possible")

    cycle = create_cycle(board_size, snake[0])
    if debug: logging.info("cycle: {}".format(cycle))

    next_cell = find_next_cell_in_cycle(snake[0], cycle)
    if debug: logging.info("next_cell: {}".format(next_cell))

    direction = helpers.cardinals[helpers.normalize(helpers.get_cardinal_vector_from_head(snake, next_cell))]
    if debug: logging.info("direction: {}".format(direction))
    return direction
    

def create_cycle(board_size, start):
    # must be even x and odd y (can work on others later)
    assert(not board_size[0]%2 and board_size[1]%2)

    current_cell = (start[0], start[1])
    cycle = [current_cell]
    cycle_index = 0
    while cycle_index < (board_size[0]+1)*(board_size[1]+1):
        # if debug: logging.info("current_cell: {}".format(current_cell))
        if current_cell[1] == 0 and not current_cell[0]%2:
            # if debug: logging.info("first row, column is odd, going right")
            direction = 'right'
        elif current_cell[1] == board_size[1]-1 and not current_cell[0] == 0:
            # if debug: logging.info("last row, not first column, going left")
            direction = 'left'
        elif current_cell[1] == board_size[1]-2 and current_cell[0]%2 and not current_cell[0] == board_size[0]-1:
            # if debug: logging.info("second to last row, column is odd, and not last column going right")
            direction = 'right'
        elif not current_cell[0]%2:
            # if debug: logging.info("column is even, going up")
            direction = 'up'
        else:
            # if debug: logging.info("else, column is odd, going down")
            direction = 'down'
        current_cell = add_cells(current_cell, direction)
        cycle.append(current_cell)
        cycle_index += 1
    return cycle


def find_next_cell_in_cycle(current_cell, cycle):
    try:
        index = cycle.index(current_cell)
    except ValueError:
        index = 0
    return cycle[(index+1)%len(cycle)]

def add_cells(current_cell, direction):
    x = current_cell[0] + helpers.opposite_directions[direction][0]
    y = current_cell[1] + helpers.opposite_directions[direction][1]
    return (x, y)


def check_hamiltonian(board_size):
    if board_size[0] > 1 and board_size[1] > 1:
        if not board_size[0]%2 or not board_size[1]%2:
            return True
    return False