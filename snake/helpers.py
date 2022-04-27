import math

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


def get_cardinal_neighbors(square):
    x, y = square
    neighbors = []
    for direction in list(cardinals.keys()):
        neighbor = (x + direction[0], y + direction[1])
        neighbors.append(neighbor)
    return neighbors

def get_all_neighbors(square):
    """
    Returns the neighbors at the given coordinate.
    """
    x, y = square
    neighbors = []
    for direction in list(cardinals.keys()) + list(diagnols.keys()):
        neighbor = (x + direction[0], y + direction[1])
        neighbors.append(neighbor)
    return neighbors

def out_of_bounds(square, board_size):
    """
    Returns True if the square is out of bounds.
    """
    x, y = square
    return x < 0 or x >= board_size[0] or y < 0 or y >= board_size[1]


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

def get_cardinal_vector_from_head(snake, point):
    """
    Returns the vector from the head of the snake to the point.
    """
    return (point[0] - snake[0][0], point[1] - snake[0][1])

def get_diagnol_vector_from_head(snake, point):
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
