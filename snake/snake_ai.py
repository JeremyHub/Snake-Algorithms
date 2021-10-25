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

def get_action(snake, food, board_size):
    """
    Returns the move to be made by the snake.
    """
    vector_to_food = get_vector_to_food(snake, food)
    direction_choice = None
    print("-------------------")
    if directions.get(vector_to_food, None):
        direction_choice =  directions[vector_to_food]
    else:
        direction_choice =  random.choice(diagnols[vector_to_food])
    possible_directions = list(directions.values())
    possible_directions.remove(direction_choice)
    while True:
        print("direction choice: ", direction_choice)
        # if intersects(direction_choice, snake, board_size) or not has_path_to_food(direction_choice, snake, board_size, food):
        if good_direction(direction_choice, snake, board_size):
            print("chosen direction: ", direction_choice)
            return direction_choice
        else:
            if possible_directions == []:
                print("No possible directions")
                while True:
                    pass
            direction_choice = random.choice(possible_directions)
            possible_directions.remove(direction_choice)

def good_direction(direction, snake, board_size):
    does_intersect = intersects(direction, snake, board_size)
    # see_tail = can_see_tail(direction, snake, board_size)
    see_tail = True
    if len(snake) >5: see_tail = can_see_tail_a_star(direction, snake, board_size)
    print(direction, ": does intersect: ", does_intersect," can see tail: ", see_tail)
    return (not does_intersect) and see_tail

# we want to check if the direction has enough open space for the snake or has the snake's tail

# def get_direction_with_most_open_space(snake, board_size):
#     """
#     Returns the direction with the most open space.
#     """
#     possible_directions = list(directions.values())
#     best_direction = None
#     best_open_space = -1
#     for direction in possible_directions:
#         open_space = get_open_space(direction, snake, board_size)
#         if open_space > best_open_space:
#             best_open_space = open_space
#             best_direction = direction
#     return best_direction

# def get_open_space(direction, snake, board_size):
#     return len(get_open_spaces(direction, snake, board_size))

def can_see_tail_a_star(direction, snake, board_size):
    x = snake[0][0] + opposite_directions[direction][0]
    y = snake[0][1] + opposite_directions[direction][1]
    return a_star.a_Star((x,y), snake[-1], board_size, snake[:len(snake)-1]) != None

def can_see_tail(direction, snake, board_size):
    """
    Returns True if the snake can move in the given direction and see the tail.
    """
    x = snake[0][0] + opposite_directions[direction][0]
    y = snake[0][1] + opposite_directions[direction][1]
    print("checking squre:" , x, y)
    checked_spaces = []
    spaces_to_check = [(x, y)]
    while spaces_to_check != []:
        x, y = spaces_to_check.pop()
        if (x, y) in checked_spaces:
            continue
        if x < 0 or x >= board_size[0]:
            continue
        if y < 0 or y >= board_size[1]:
            continue
        if (x, y) in snake[1:len(snake)-1]:
            continue
        if (x, y) == snake[-1]:
            return True
        checked_spaces.append((x, y))
        spaces_to_check.append((x + 1, y))
        spaces_to_check.append((x - 1, y))
        spaces_to_check.append((x, y + 1))
        spaces_to_check.append((x, y - 1))
    # print(direction)
    return False

def intersects(direction, snake, board_size):
    """
    Returns True if the snake will intersect itself if it moves in the given direction.
    """
    head_x, head_y = snake[0]
    new_head_x = opposite_directions[direction][0] + head_x
    new_head_y = opposite_directions[direction][1] + head_y
    if new_head_x < 0 or new_head_x >= board_size[0]:
        # print(direction)
        return True
    if new_head_y < 0 or new_head_y >= board_size[1]:
        # print(direction)
        return True
    if (new_head_x, new_head_y) in snake[1:len(snake)-1]:
        # print(direction)
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