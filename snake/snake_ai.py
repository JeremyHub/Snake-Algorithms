import random
import a_star
import pygame
import math

debug = False

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

def get_action(snake, food, board_size):
    """
    Returns the move to be made by the snake.
    """
    if debug: print("-------------------")
    path_to_food = a_star.a_Star(snake[0], food, board_size, snake)
    if not path_to_food:
        vector_to_food = reverse_vector(normalize(get_vector(snake, food)))
        if debug: print("reverse vector to food: ", vector_to_food)
    else:
        vector_to_food = normalize(get_vector(snake, path_to_food[1]))
        if debug: print("vector to first path: ", vector_to_food)
    # if len(snake) > board_size[0] * board_size[1] * 0.8 and not path_to_food:
    #     vector_to_food = reverse_vector(normalize(get_vector(snake, food)))
    #     if debug: print("vector to food (lategame)")
    # vector_to_food = normalize(get_vector(snake, food))
    direction_choice = None
    if debug: print("snake head: ", snake[0])
    if debug: print("snake tail: ", snake[-1])
    if debug: print("food :", food)
    if directions.get(vector_to_food, None):
        direction_choice =  directions[vector_to_food]
    else:
        direction_choice =  best_rand_direction(diagnols[vector_to_food], snake, board_size, food)
    possible_directions = list(directions.values())
    possible_directions.remove(direction_choice)
    while True:
        if debug: print("direction choice: ", direction_choice)
        # if intersects(direction_choice, snake, board_size) or not has_path_to_food(direction_choice, snake, board_size, food):
        if good_direction(direction_choice, snake, board_size):
            if debug: print("chosen direction: ", direction_choice)
            return direction_choice
        else:
            if possible_directions == []:
                if debug: print("No possible directions")
                while True:
                    pass
            direction_choice = best_rand_direction(possible_directions, snake, board_size, food)
            possible_directions.remove(direction_choice)

def best_rand_direction(possible_directions, snake, board_size, food):
    """
    Returns the best random direction. It works if this function just returns a random choice
    but, its better for this function returned a direction that sticks close to the body of the snake.
    """
    # lategame = len(snake) > (board_size[0] * board_size[1]) / 2
    # if debug: print("lategame: ", lategame)
    if debug: print("possible directions: ", possible_directions)

    good_directions_from_direction = {}
    for direction in possible_directions:
        if not good_direction(direction, snake, board_size):
            continue
        for second_direction in directions.values():
            if debug: print("looking at direction: ", second_direction, " from direction :", direction)
            # making a copy of snake and taking away the tail
            snake_copy = snake.copy()[:len(snake)-2]
            # putting in the new head for the first direction
            snake_copy.insert(0, get_square_in_direction(snake[0], direction))
            # putting in the new head for the second direction
            snake_copy.insert(0, get_square_in_direction(snake_copy[0], second_direction))
            if good_direction(second_direction, snake_copy, board_size):
                good_directions_from_direction[direction] = good_directions_from_direction.get(direction, 0) + 1
            else:
                good_directions_from_direction[direction] = good_directions_from_direction.get(direction, 0)
    if debug: print("good directions from direction: ", good_directions_from_direction)
    max_good_directions = 0
    max_good_directions_direction = []
    for direction in good_directions_from_direction.keys():
        if good_directions_from_direction[direction] > max_good_directions:
            max_good_directions = good_directions_from_direction[direction]
            max_good_directions_direction = [direction]
        elif good_directions_from_direction[direction] == max_good_directions:
            max_good_directions_direction.append(direction)
    if len(max_good_directions_direction) == 1:
        if debug: print("best direction: ", max_good_directions_direction[0])
        return max_good_directions_direction[0]
    
    if len(max_good_directions_direction) > 1:
        possible_directions = max_good_directions_direction
        for direction in possible_directions:
            if out_of_bounds(get_square_in_direction(get_square_in_direction(snake[0], direction), direction), board_size):
                if debug: print("removed direction: ", direction)
                possible_directions.remove(direction)

    best_num = float("-inf")
    best_direction = None
    for direction in possible_directions:
        num_neighbors_in_snake = 0
        square = get_square_in_direction(snake[0], direction)
        num_neighbors_in_snake = get_num_neighbors_in_snake(square, snake, board_size)
        num = 0
        # num neighbors in snake should be incentivized, therefore its added
        num += num_neighbors_in_snake
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

def good_direction(direction, snake, board_size):
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

def reverse_vector(vector):
    return (-vector[0], -vector[1])

def get_vector(snake, food):
    """
    Returns the vector to the food.
    """
    vector = (food[0] - snake[0][0], food[1] - snake[0][1])
    x_sign = 1 if vector[0] >= 0 else -1
    y_sign = 1 if vector[1] >= 0 else -1
    print("vector: ", vector)
    x = x_sign * math.ceil(abs(vector[0]))
    y = y_sign * math.ceil(abs(vector[1]))
    return (x, y)

def normalize(vector):
    """
    Returns the normalized vector.
    """
    x, y = vector
    x_component = int(x / abs(x)) if vector[0] != 0 else 0
    y_component = int(y / abs(y)) if vector[1] != 0 else 0
    print(x_component, y_component)
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