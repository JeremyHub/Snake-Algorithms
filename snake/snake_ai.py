import random
import a_star

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
    if directions.get(vector_to_food, None):
        direction_choice =  directions[vector_to_food]
    else:
        direction_choice =  diagnols[vector_to_food][0]
        if intersects(direction_choice, snake, board_size):
            direction_choice = diagnols[vector_to_food][1]
    possible_directions = list(directions.values())
    possible_directions.remove(direction_choice)
    while True:
        # if intersects(direction_choice, snake, board_size) or not has_path_to_food(direction_choice, snake, board_size, food):
        if intersects(direction_choice, snake, board_size) or not can_see_tail(direction_choice, snake, board_size):
            direction_choice = random.choice(possible_directions)
            possible_directions.remove(direction_choice)
            if possible_directions == []:
                print("No possible directions")
                while True:
                    pass
        else:
            return direction_choice

# we want to check if the direction has enough open space for the snake or has the snake's tail
def can_see_tail(direction, snake, board_size):
    """
    Returns True if the snake can move in the given direction and see the tail.
    """
    # if (snake[-1][0], snake[-1][1]) in get_open_spaces(direction, snake, board_size):
    print(len(snake))
    return snake[-1] in get_open_spaces(direction, snake, board_size)

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

def get_open_spaces(direction, snake, board_size):
    """
    Returns the number of open spaces in the given direction.
    """
    x = snake[0][0] + opposite_directions[direction][0]
    y = snake[0][1] + opposite_directions[direction][1]
    open_spaces = []
    spaces_to_check = [(x, y)]
    while spaces_to_check != []:
        x, y = spaces_to_check.pop()
        if (x, y) in open_spaces:
            continue
        if x < 0 or x >= board_size[0]:
            continue
        if y < 0 or y >= board_size[1]:
            continue
        if (x, y) in snake[1:]:
            continue
        if (x, y) == snake[-1]:
            continue
        open_spaces.append((x, y))
        spaces_to_check.append((x + 1, y))
        spaces_to_check.append((x - 1, y))
        spaces_to_check.append((x, y + 1))
        spaces_to_check.append((x, y - 1))
    return open_spaces

def intersects(direction, snake, board_size):
    """
    Returns True if the snake will intersect itself if it moves in the given direction.
    """
    head_x, head_y = snake[0]
    new_head_x = opposite_directions[direction][0] + head_x
    new_head_y = opposite_directions[direction][1] + head_y
    if new_head_x < 0 or new_head_x >= board_size[0]:
        return True
    if new_head_y < 0 or new_head_y >= board_size[1]:
        return True
    if (new_head_x, new_head_y) in snake[1:]:
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