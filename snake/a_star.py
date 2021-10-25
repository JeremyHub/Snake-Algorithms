# function reconstruct_path(cameFrom, current)
#     total_path := {current}
#     while current in cameFrom.Keys:
#         current := cameFrom[current]
#         total_path.prepend(current)
#     return total_path

# // A* finds a path from start to goal.
# // h is the heuristic function. h(n) estimates the cost to reach goal from node n.
# function A_Star(start, goal, h)
#     // The set of discovered nodes that may need to be (re-)expanded.
#     // Initially, only the start node is known.
#     // This is usually implemented as a min-heap or priority queue rather than a hash-set.
#     openSet := {start}

#     // For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
#     // to n currently known.
#     cameFrom := an empty map

#     // For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
#     gScore := map with default value of Infinity
#     gScore[start] := 0

#     // For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to
#     // how short a path from start to finish can be if it goes through n.
#     fScore := map with default value of Infinity
#     fScore[start] := h(start)

#     while openSet is not empty
#         // This operation can occur in O(1) time if openSet is a min-heap or a priority queue
#         current := the node in openSet having the lowest fScore[] value
#         if current = goal
#             return reconstruct_path(cameFrom, current)

#         openSet.Remove(current)
#         for each neighbor of current
#             // d(current,neighbor) is the weight of the edge from current to neighbor
#             // tentative_gScore is the distance from start to the neighbor through current
#             tentative_gScore := gScore[current] + d(current, neighbor)
#             if tentative_gScore < gScore[neighbor]
#                 // This path to neighbor is better than any previous one. Record it!
#                 cameFrom[neighbor] := current
#                 gScore[neighbor] := tentative_gScore
#                 fScore[neighbor] := gScore[neighbor] + h(neighbor)
#                 if neighbor not in openSet
#                     openSet.add(neighbor)

#     // Open set is empty but goal was never reached
#     return failure

def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.insert(0, current)
    return total_path

def a_Star(start, goal, board_size, snake_body, debug=False):
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