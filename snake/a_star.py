def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.insert(0, current)
    return total_path

def a_Star(start, goal, board_size, snake_body, *, debug=False):
    openSet = [start]
    cameFrom = {}
    gScore = {}
    gScore[start] = 0
    fScore = {}
    fScore[start] = get_cost(start, goal)

    while openSet:
        current = min(openSet, key=lambda x: fScore[x])
        
        if current == goal:
            if debug: print("can! get from here: ", start, " to here: ", goal)
            if debug: print("with the above path, the head of the snake is: ", snake_body[0])
            path = reconstruct_path(cameFrom, current)
            if debug: print("the path is: ", path)
            return path

        openSet.remove(current)
        for neighbor in get_neighbors(current, board_size, snake_body):
            tentative_gScore = gScore[current] + get_cost(current, neighbor)
            if tentative_gScore < gScore.get(neighbor, float('inf')):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + get_cost(current, neighbor)
                if neighbor not in openSet:
                    openSet.append(neighbor)

    # Open set is empty but goal was never reached
    if debug: print("cant get from here: ", start, " to here: ", goal)
    return None

directions = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]

# get_neighbors returns a list of neighbors of the current node that are not walls or snake body and it cannot travel diagonally
def get_neighbors(current, board_size, snake_body):
    neighbors = []
    for direction in directions:
        neighbor = (current[0] + direction[0], current[1] + direction[1])
        if neighbor[0] < 0 or neighbor[0] >= board_size[0] or neighbor[1] < 0 or neighbor[1] >= board_size[1]:
            continue
        if neighbor in snake_body:
            continue
        neighbors.append(neighbor)
    return neighbors

def get_cost(current, neighbor):
    current_x, current_y = current
    neighbor_x, neighbor_y = neighbor
    distance = abs(current_x - neighbor_x) + abs(current_y - neighbor_y)
    return distance
