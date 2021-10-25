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
    vector_to_food = get_vector_to_food(snake, food)
    direction_choice = None
    if debug: print("-------------------")
    if directions.get(vector_to_food, None):
        direction_choice =  directions[vector_to_food]
    else:
        # this randomess below is crucial to it not getting stuck in loops
        direction_choice =  best_rand_direction(diagnols[vector_to_food], snake, board_size)
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
            direction_choice = best_rand_direction(possible_directions, snake, board_size)
            possible_directions.remove(direction_choice)

def best_rand_direction(possible_directions, snake, board_size):
    """
    Returns the best random direction. It works if this function just returns a random choice
    but, its better for this function returned a direction that sticks close to the body of the snake.
    """
    best_direction = None
    best_num_neighbors = float("-inf")
    for square in get_neighbors(snake[0], snake, board_size):
        for direction in possible_directions:
            num_neighbors = get_num_neighbors(get_square_in_direction(square, direction), snake, board_size)
            if num_neighbors > best_num_neighbors:
                best_direction = direction
                best_num_neighbors = num_neighbors
    return best_direction if not best_direction == None else random.choice(possible_directions)
    # return best_direction

def get_square_in_direction(square, direction):
    x = square[0] + opposite_directions[direction][0]
    y = square[1] + opposite_directions[direction][1]
    return (x, y)
    
def get_num_neighbors(square, snake, board_size):
    return len(get_neighbors(square, snake, board_size))

def get_neighbors(square, snake, board_size):
    """
    Returns the number of neighbors that are part of the snake of the given coordinate.
    """
    x, y = square
    neighbors = []
    for direction in list(directions.keys()) + list(diagnols.keys()):
        neighbor = (x + direction[0], y + direction[1])
        if neighbor in snake or out_of_bounds(neighbor, board_size):
            continue
        neighbors.append(neighbor)
    return neighbors

# def food_enclosed(snake, food, board_size):
#     """
#     Returns True if the food is enclosed by the snake.
#     """
#     for square in get_neighbors(food):
#         if square not in snake or not out_of_bounds(square, board_size):
#             return False
#     return True

def out_of_bounds(square, board_size):
    """
    Returns True if the square is out of bounds.
    """
    x, y = square
    return x < 0 or x >= board_size[0] or y < 0 or y >= board_size[1]

def good_direction(direction, snake, board_size, debug=False):
    does_intersect = intersects(direction, snake, board_size)
    see_tail = can_see_tail_a_star(get_square_in_direction(snake[0], direction), snake, board_size)
    # enough_space = get_open_space(direction, snake, board_size)
    if debug: print(direction, ": does intersect: ", does_intersect," can see tail: ", see_tail)
    return not does_intersect and see_tail
    # return (not intersects(direction, snake, board_size)) and (can_see_tail_a_star(direction, snake, board_size) or get_open_space(direction, snake, board_size)>len(snake))


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