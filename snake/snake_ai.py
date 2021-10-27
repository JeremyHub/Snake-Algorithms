from os import path
import random
import a_star
import pygame
import math

debug = True

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
    if debug: print("---------finding new move----------")
    path_to_food = a_star.a_Star(snake[0], food, board_size, snake)
    if not path_to_food:
        vector_to_food = reverse_vector(normalize(get_vector_diagnols_from_head(snake, food)))
        if debug: print("reverse vector to food: ", vector_to_food)
    else:
        vector_to_food = normalize(get_vector_diagnols_from_head(snake, food))
        if debug: print("vector to food: ", vector_to_food)
    direction_choice = None
    if debug: print("snake head: ", snake[0])
    if debug: print("snake tail: ", snake[-1])
    if debug: print("food :", food)
    if directions.get(vector_to_food, None):
        direction_choice =  directions[vector_to_food]
    else:
        direction_choice =  best_rand_direction(diagnols[vector_to_food], snake, board_size, path_to_food, food)

    if path_to_food and len(path_to_food) < 5:
        vector_to_food = get_direction_names_from_vector(normalize(get_vector_diagnols_from_head(snake, food)))
        vector_away_from_tail = get_direction_names_from_vector(reverse_vector(normalize(get_vector_diagnols_from_head(snake, snake[-1]))))
        intersection = get_same_directions(vector_to_food, vector_away_from_tail)
        print(intersection)
        if len(intersection) == 1:
            possible_directions = [intersection]
            direction_choice = intersection[0]
        if len(intersection) > 0:
            possible_directions = intersection
            direction_choice = best_rand_direction(possible_directions, snake, board_size, path_to_food, food)
        if debug: print("small path to food, doing vector away from tail, here are directions from that vector: ", direction_choice)

    possible_directions = list(directions.values())
    possible_directions.remove(direction_choice)
    while True:
        if debug: print("direction choice: ", direction_choice)
        if good_direction(direction_choice, snake, board_size):
            if debug: print("chosen direction: ", direction_choice)
            return direction_choice
        else:
            if possible_directions == []:
                if debug:
                    print("No possible directions")
                    while True:
                        pass
                return("none")
            direction_choice = best_rand_direction(possible_directions, snake, board_size, path_to_food, food)
            possible_directions.remove(direction_choice)

def best_rand_direction(original_options, snake, board_size, path_to_food, food):
    # re-assign possible directions
    possible_directions = original_options
    if debug: print("possible directions: ", possible_directions)
    good_directions_from_direction = {}

    # loop over every direction given in the function
    for direction in possible_directions:
        # if its not a good direction then dont even look at it
        if not good_direction(direction, snake, board_size):
            continue
        # if it is a good direction, check all directions given that you go in that direction
        for second_direction in directions.values():
            if debug: print("looking at direction: ", second_direction, " from direction :", direction)
            # making a copy of snake and taking away the tail
            snake_copy = snake.copy()[:len(snake)-1]
            # putting in the new head for the first direction
            snake_copy.insert(0, get_square_in_direction(snake[0], direction))
            # if that direction is good, add 1 to the dict where the key is the original direction
            if good_direction(second_direction, snake_copy, board_size):
                good_directions_from_direction[direction] = good_directions_from_direction.get(direction, 0) + 1
            else:
                good_directions_from_direction[direction] = good_directions_from_direction.get(direction, 0)

    if debug: print("good directions from direction: ", good_directions_from_direction)
    best_direction_num = 0
    best_directions = []

    # loop over the keys of the dict (the given directions that are good)
    for direction in good_directions_from_direction.keys():
        # if the number of good directions from that direction is greater than the best direction num then add it to the lsit and set the best direction num to that number
        if good_directions_from_direction[direction] > best_direction_num:
            best_direction_num = good_directions_from_direction[direction]
            best_directions = [direction]
        # otherwise if its equal then append that direction because its still in the running
        elif good_directions_from_direction[direction] == best_direction_num:
            best_directions.append(direction)

    # if there are no good directions then return a random one just so the function thats calling this doesnt break, but its gonna move on anyway
    if best_directions == []:
        return random.choice(possible_directions)

    # # if there is more than one good direction
    # elif len(best_directions) > 1:
    #     # re-assigning possilbe directions here because it means there is more than one direction in best directions
    #     possible_directions = best_directions
    #     # loop over the goood directions
    #     for direction in best_directions:
    #         square = get_square_in_direction(snake[0], direction)
    #         # check if that square is next to a wall, if it is, remove it from the list
    #         for neighbor in get_neighbors(square):
    #             if out_of_bounds(neighbor, board_size):
    #                 possible_directions.remove(direction)
    #                 break
    
    # if there is one direction, return it
    elif len(best_directions) == 1:
        if debug: print("best direction: ", best_directions[0])
        return best_directions[0]
    
    # if all options were pruned at this point (probably for all touching the wall), then just use the oginial options)
    elif len(best_directions) == 0:
        possible_directions = original_options
    
    best_num = float("-inf")
    best_direction = None
    # loop over the possible directions to check which has the most neighbors
    for direction in possible_directions:
        num_neighbors_in_snake = 0
        square = get_square_in_direction(snake[0], direction)
        num_neighbors_in_snake = get_num_neighbors_in_snake(square, snake, board_size)
        num = 0
        # num neighbors in snake should be incentivized, therefore its added
        num += num_neighbors_in_snake
        # best directions are ones with large nums
        if num > best_num:
            best_direction = direction
            best_num = num
    return best_direction

def get_same_directions(directiosn1, directions2):
    print(directiosn1, directions2)
    intersection = []
    for direction in directiosn1:
        if direction in directions2:
            intersection.append(direction)
    return intersection

def get_direction_names_from_vector(direction):
    if directions.get(direction, None):
        return [directions[direction]]
    else:
        return diagnols[direction]

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
    return a_star.a_Star(square, snake[-1], board_size, snake[:len(snake)-1]) != None


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

def get_vector_nodiagnols_from_head(snake, food):
    """
    Returns the vector from the head of the snake to the food.
    """
    return (food[0] - snake[0][0], food[1] - snake[0][1])

def get_vector_diagnols_from_head(snake, point):
    """
    Returns the vector to the point from the head, prefers diagnols.
    """
    vector = (point[0] - snake[0][0], point[1] - snake[0][1])
    x_sign = 1 if vector[0] >= 0 else -1
    y_sign = 1 if vector[1] >= 0 else -1
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