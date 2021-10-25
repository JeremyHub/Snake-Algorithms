import random
import a_star
import pygame

directions = {
    (0, 1): 'down',
    (0, -1): 'up',
    (1, 0): 'right',
    (-1, 0): 'left'
}

opposite_directions = dict([(value, key) for key, value in directions.items()])

diagnols = {
    (1, 1): ("down", "right"),
    (1, -1): ("up", "right"),
    (-1, 1): ("down", "left"),
    (-1, -1): ("up", "left")
}

def get_action(snake, food, board_size, debug=False):
    """
    Returns the move to be made by the snake.
    """
    path_to_food = a_star.a_Star(snake[0], food, board_size, snake)
    if not path_to_food:
        vector_to_food = get_vector_to_food(snake, food)
    else:
        vector_to_food = get_vector_to_food(snake, path_to_food[1])
    direction_choice = None
    if debug: print("-------------------")
    if directions.get(vector_to_food, None):
        direction_choice =  directions[vector_to_food]
    else:
        direction_choice =  best_rand_direction(diagnols[vector_to_food], snake, board_size, food, debug)
    possible_directions = list(directions.values())
    possible_directions.remove(direction_choice)
    while True:
        if debug: print("direction choice: ", direction_choice)
        # if intersects(direction_choice, snake, board_size) or not has_path_to_food(direction_choice, snake, board_size, food):
        if good_direction(direction_choice, snake, board_size, debug):
            if debug: print("chosen direction: ", direction_choice)
            return direction_choice
        else:
            if possible_directions == []:
                if debug: print("No possible directions")
                while True:
                    pass
            direction_choice = best_rand_direction(possible_directions, snake, board_size, food, debug)
            possible_directions.remove(direction_choice)

def best_rand_direction(possible_directions, snake, board_size, food, debug=False):
    """
    Returns the best random direction. It works if this function just returns a random choice
    but, its better for this function returned a direction that sticks close to the body of the snake.
    """
    best_direction = None
    lategame = len(snake) > (board_size[0] * board_size[1]) / 2
    if debug: print("lategame: ", lategame)
    best_num = float("-inf")

    for direction in possible_directions:
        num_neighbors_in_snake = 0
        square = get_square_in_direction(snake[0], direction)
        path_to_food = a_star.a_Star(square, food, board_size, snake)
        # TODO find the best value for if no path
        # if no path it is larrrge which means it will incetivze directions that have a path to food
        # if_no_path = (board_size[0] * board_size[1])/5
        len_path_to_food = len(path_to_food) if path_to_food else 1
        num_neighbors_in_snake = get_num_neighbors_in_snake(square, snake, board_size)
        # TODO find best value for num
        num = 0
        # num neighbors in snake should be incentivized, therefore its added
        num += num_neighbors_in_snake
        # len_path_to_food should be decentivzed, therefore its subtracted
        # as the game goes on this should matter less and less
        # percent_through_game = len(snake) - (board_size[0]+1 * board_size[1]+1) / (board_size[0]+1 * board_size[1]+1)
        # num -= len_path_to_food * percent_through_game

        # best paths are ones with large nums
        if num > best_num:
            best_direction = direction
            best_num = num
    return best_direction

def get_square_in_direction(square, direction):
    x = square[0] + opposite_directions[direction][0]
    y = square[1] + opposite_directions[direction][1]
    return (x, y)
    
def get_num_neighbors_in_snake(square, snake, board_size):
    num = 0
    for neighbor in get_neighbors(square):
        if neighbor in snake:
            num += 1
    return num

def get_neighbors(square):
    """
    Returns the number of neighbors that are part of the snake of the given coordinate.
    """
    x, y = square
    neighbors = []
    for direction in list(directions.keys()) + list(diagnols.keys()):
        neighbor = (x + direction[0], y + direction[1])
        neighbors.append(neighbor)
    return neighbors

def out_of_bounds(square, board_size):
    """
    Returns True if the square is out of bounds.
    """
    x, y = square
    return x < 0 or x >= board_size[0] or y < 0 or y >= board_size[1]

def good_direction(direction, snake, board_size, debug=False):
    does_intersect = intersects(direction, snake, board_size)
    see_tail = can_see_tail_a_star(get_square_in_direction(snake[0], direction), snake, board_size)
    if debug: print(direction, ": does intersect: ", does_intersect," can see tail: ", see_tail)
    return not does_intersect and see_tail

def can_see_tail_a_star(square, snake, board_size):
    x, y = square
    return a_star.a_Star((x,y), snake[-1], board_size, snake[:len(snake)-1]) != None


def intersects(direction, snake, board_size):
    """
    Returns True if the snake will intersect itself if it moves in the given direction.
    """
    head_x, head_y = snake[0]
    new_head_x = opposite_directions[direction][0] + head_x
    new_head_y = opposite_directions[direction][1] + head_y
    if out_of_bounds((new_head_x, new_head_y), board_size):
        # if debug: print(direction)
        return True
    if (new_head_x, new_head_y) in snake[1:len(snake)-1]:
        # if debug: print(direction)
        return True
    return False

def get_vector_to_food(snake, food):
    """
    Returns the vector to the food.
    """
    return normalize([food[0] - snake[0][0], food[1] - snake[0][1]])

def normalize(vector):
    """
    Returns the normalized vector.
    """
    x_component = int(vector[0] / abs(vector[0])) if vector[0] != 0 else 0
    y_component = int(vector[1] / abs(vector[1])) if vector[1] != 0 else 0
    return (x_component, y_component)

def has_path_to_food(direction, snake, board_size, food):
    """
    Returns True if the snake can move in the given direction and reach the food.
    """
    x = snake[0][0] + opposite_directions[direction][0]
    y = snake[0][1] + opposite_directions[direction][1]
    if x == food[0] and y == food[1]:
        return True
    return a_star.a_Star((x,y), food, board_size, snake[1:]) == None