import random
import a_star
import math

debug = True

if debug:
    import os
    from os.path import exists
    import logging

    if exists("log.txt"):
        os.remove("log.txt")
    file_path = "log.txt"
    logging.basicConfig(filename=file_path,
                                filemode='a',
                                format='',
                                datefmt='',
                                level=logging.INFO)

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

# TODO comment this function
# TODO dissuade it from making squares which are blocked in on three sides (make sure to include edges)
def get_action(snake, food, board_size):
    """
    Returns the move to be made by the snake.
    """
    if debug: logging.info("---------finding new move----------")
    path_to_food = a_star.a_Star(snake[0], food, board_size, snake)
    if not path_to_food:
        vector_to_food = reverse_vector(normalize(get_vector_diagnols_from_head(snake, food)))
        if debug: logging.info(f"reverse vector to food: {vector_to_food}")
    elif len(path_to_food) == 1:
        vector_to_food = normalize(get_vector_diagnols_from_head(snake, path_to_food[0]))
        if good_direction(directions[vector_to_food], snake, board_size):
            return directions[vector_to_food]
    else:
        vector_to_food = normalize(get_vector_diagnols_from_head(snake, food))
        if debug: logging.info(f"reverse vector to food: {vector_to_food}")
    direction_choice = None
    if debug: logging.info(f"snake head: {snake[0]}")
    if debug: logging.info(f"snake tail: {snake[-1]}")
    if debug: logging.info(f"food: {food}")
    if directions.get(vector_to_food, None):
        direction_choice =  directions[vector_to_food]
    else:
        direction_choice =  best_rand_direction(diagnols[vector_to_food], snake, board_size, path_to_food, food)

    if path_to_food and len(path_to_food) < 5:
        vector_to_food = get_direction_names_from_vector(normalize(get_vector_diagnols_from_head(snake, food)))
        vector_away_from_tail = get_direction_names_from_vector(reverse_vector(normalize(get_vector_diagnols_from_head(snake, snake[-1]))))
        intersection = get_same_directions(vector_to_food, vector_away_from_tail)
        if debug: logging.info(f"itnersections: {intersection}")
        if len(intersection) == 1:
            possible_directions = [intersection]
            direction_choice = intersection[0]
        if len(intersection) > 0:
            possible_directions = intersection
            direction_choice = best_rand_direction(possible_directions, snake, board_size, path_to_food, food)
        if debug: logging.info(f"small path to food, doing vector away from tail, here are directions from that vector: {direction_choice}")

    possible_directions = list(directions.values())
    possible_directions.remove(direction_choice)
    while True:
        if debug: logging.info(f"direction choice: {direction_choice}")
        if good_direction(direction_choice, snake, board_size):
            if debug: logging.info(f"chosen direction: {direction_choice}")
            return direction_choice
        else:
            if possible_directions == []:
                if debug:
                    logging.info("No possible directions")
                    while True:
                        pass
                return("none")
            direction_choice = best_rand_direction(possible_directions, snake, board_size, path_to_food, food)
            possible_directions.remove(direction_choice)

def best_rand_direction(original_options, snake, board_size, path_to_food, food):
    # re-assign possible directions
    possible_directions = original_options
    if debug: logging.info(f"possible directions: {possible_directions}")
    good_directions_from_direction = {}

    # loop over every direction given in the function
    for direction in possible_directions:
        # if its not a good direction then dont even look at it
        if not good_direction(direction, snake, board_size):
            continue
        # if it is a good direction, check all directions given that you go in that direction
        for second_direction in directions.values():
            if debug: logging.info(f"looking at direction: {second_direction} from direction : {direction}")
            # making a copy of snake and taking away the tail
            snake_copy = snake.copy()[:len(snake)-1]
            # putting in the new head for the first direction
            snake_copy.insert(0, get_square_in_direction(snake[0], direction))
            # if that direction is good, add 1 to the dict where the key is the original direction
            if good_direction(second_direction, snake_copy, board_size):
                # add another 1 if it has a path to the food (just incentivzes this)
                if has_path_to_food(second_direction, snake_copy, food, board_size):
                    good_directions_from_direction[direction] = good_directions_from_direction.get(direction, 0) + 1
                good_directions_from_direction[direction] = good_directions_from_direction.get(direction, 0) + 1
            else:
                good_directions_from_direction[direction] = good_directions_from_direction.get(direction, 0)

    if debug: logging.info(f"good directions from direction: {good_directions_from_direction}")
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
        if debug: logging.info("no good directions")
        return random.choice(possible_directions)
    
    # if there is one direction, return it
    elif len(best_directions) == 1:
        if debug: logging.info(f"best direction: {best_directions[0]}")
        return best_directions[0]
    
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
    if debug: logging.info(f"best direction: {best_direction}")
    return best_direction

def check_for_any_blocked_off_squares(direction, snake, board_size):
    goal = get_square_in_direction(snake[0], direction)
    # for every neighbor
    for square in get_all_neighbors(goal):
        if square in snake or square == goal or out_of_bounds(square, board_size):
            continue
        # check if its enclosed
        if square_is_enclosed(square, snake, board_size):
            return True
    return False

def square_is_enclosed(square, snake, board_size):
    sides_block = 0
    for neighbor in get_cardinal_neighbors(square):
        if neighbor in snake or out_of_bounds(neighbor, board_size):
            sides_block += 1
    return sides_block >= 3

def get_same_directions(directiosn1, directions2):
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
    for neighbor in get_all_neighbors(square):
        if neighbor in snake:
            num += 1
    return num

def get_cardinal_neighbors(square):
    x, y = square
    neighbors = []
    for direction in list(directions.keys()):
        neighbor = (x + direction[0], y + direction[1])
        neighbors.append(neighbor)
    return neighbors

def get_all_neighbors(square):
    """
    Returns the neighbors at the given coordinate.
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
    if does_intersect:
        if debug: logging.info(f"{direction} intersects")
        return False
    see_tail = can_see_tail_a_star(get_square_in_direction(snake[0], direction), snake, board_size)
    if not see_tail:
        if debug: logging.info(f"{direction} cant see tail")
        return False
    # probably cant have this here, as in there will be times where it has to block off a square
    # if check_for_any_blocked_off_squares(direction, snake, board_size):
    #     if debug: logging.info(f"{direction} has block off squares")
    #     return False
    return True

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
        return True
    if (new_head_x, new_head_y) in snake[1:len(snake)-1]:
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