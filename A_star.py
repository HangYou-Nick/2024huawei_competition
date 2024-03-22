# import numpy as np

# def manhattan_distance(point1, point2):
#     return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# def is_valid_point(point, grid):
#     rows, cols = grid.shape
#     return 0 <= point[0] < rows and 0 <= point[1] < cols and grid[point[0], point[1]] == 0

# def reconstruct_path(came_from, current):
#     path = [current]
#     while current in came_from:
#         current = came_from[current]
#         path.insert(0, current)
#     return path

# def get_neighbors(point, grid, avoid_points, current_idx, path):
#     neighbors = []
#     rows, cols = grid.shape
#     for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
#         neighbor = (point[0] + move[0], point[1] + move[1])
#         if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0], neighbor[1]] == 0:
#             if 0 <= neighbor[0] <= rows - 1 and 0 <= neighbor[1] <= cols - 1:
#                 if not any(avoid_idx == current_idx and avoid_coord == neighbor for avoid_idx, avoid_coord in avoid_points):
#                     neighbors.append(neighbor)
#     return neighbors

# def astar_search(start, goal, grid, avoid_points, path):

#     open_set = []
#     closed_set = set()
#     came_from = {}
#     g_score = {tuple(start): 0}
#     f_score = {tuple(start): manhattan_distance(start, goal)}
#     open_set.append((f_score[tuple(start)], tuple(start)))
#     path = []   

#     while open_set:
#         _, current = open_set.pop(0)
#         if current == tuple(goal):
#             path = reconstruct_path(came_from, current)

#             final_path = []
#             for idx, point in enumerate(path):
#                 final_path.append(point)

#             return final_path
#         closed_set.add(current)
#         current_idx = path.index(current) if current in path else None
#         for neighbor in get_neighbors(current, grid, avoid_points, current_idx, path):
#             if neighbor in closed_set:
#                 continue
#             tentative_g_score = g_score[current] + 1
#             if tuple(neighbor) not in [item[1] for item in open_set] or tentative_g_score < g_score.get(tuple(neighbor), float('inf')):
#                 came_from[tuple(neighbor)] = current
#                 g_score[tuple(neighbor)] = tentative_g_score
#                 f_score[tuple(neighbor)] = tentative_g_score + manhattan_distance(neighbor, goal)
#                 open_set.append((f_score[tuple(neighbor)], tuple(neighbor)))
#         open_set.sort(key=lambda x: x[0])

#     return None

# def is_obstacle(avoid_coord, point, path, idx):
#     if abs(idx - avoid_coord[0]) == 1:
#         direction = avoid_coord[1]
#         target_direction = get_direction_from_point(point, path, idx)
#         if target_direction is not None and direction == get_opposite_direction(target_direction):
#             return True
#     return False

# def get_opposite_direction(direction):
    
#     opposite_directions = {0: 1, 1: 0, 2: 3, 3: 2}
#     return opposite_directions.get(direction)
                                                                                                                                               
# def get_direction_from_point(point, path, idx):
#     if idx < len(path) - 1:
#         next_point = path[idx + 1]
#         if next_point[0] == point[0] and next_point[1] == point[1] + 1:
#             return 0
#         elif next_point[0] == point[0] and next_point[1] == point[1] - 1:
#             return 1
#         elif next_point[0] == point[0] + 1 and next_point[1] == point[1]:
#             return 2
#         elif next_point[0] == point[0] - 1 and next_point[1] == point[1]:
#             return 3
#     return None


# starts = [[0, 0],[0, 1],[4,  0]]
# goals =  [[4, 4],[2, 3],[0, 4]]
# grid = np.array([
#     [0, 0, 0, 0, 0],
#     [0, 1, 1, 1, 0],
#     [0, 1, 0, 0, 0],
#     [0, 1, 1, 1, 0],
#     [0, 0, 0, 0, 0]
# ])
# avoid_points = set()
# for start, goal in zip(starts, goals):
#     path = astar_search(start, goal, grid, avoid_points, [])
#     if path:
#         for idx, point in enumerate(path):
#             avoid_points.add((idx, point))
#         print("Path from", start, "to", goal, ":", path)

# print("Avoid points:", avoid_points)

# import numpy as np

# def manhattan_distance(point1, point2):
#     return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# def is_valid_point(point, grid):
#     rows, cols = grid.shape
#     return 0 <= point[0] < rows and 0 <= point[1] < cols and grid[point[0], point[1]] == 0

# def get_neighbors(point, grid):
#     neighbors = []
#     rows, cols = grid.shape
#     for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
#         neighbor = (point[0] + move[0], point[1] + move[1])
#         if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0], neighbor[1]] == 0:
#             neighbors.append(neighbor)
#     return neighbors

# def reconstruct_path(came_from, current):
#     path = [current]
#     while current in came_from:
#         current = came_from[current]
#         path.insert(0, current)
#     return path

# def astar_search(start, goal, grid, avoid_points):
#     open_set = []
#     closed_set = set()
#     came_from = {}
#     g_score = {tuple(start): 0}
#     f_score = {tuple(start): manhattan_distance(start, goal)}
#     open_set.append((f_score[tuple(start)], tuple(start)))
#     while open_set:
#         _, current = open_set.pop(0)
#         if current == tuple(goal):
#             path = reconstruct_path(came_from, current)
            
#             numbered_path = [(point, idx) for idx, point in enumerate(path)]
#             numbered_path.sort(key=lambda x: x[1])
#             path = [point for point, _ in numbered_path]
            
#             path = [point for point in path if point not in avoid_points and (point, path.index(point)) not in avoid_points]
#             return path
#         closed_set.add(current)
#         for neighbor in get_neighbors(current, grid):
#             if neighbor in avoid_points:
#                 continue
#             tentative_g_score = g_score[current] + 1
#             if neighbor in closed_set or (tuple(neighbor) in g_score and tentative_g_score >= g_score[tuple(neighbor)]):
#                 continue
#             if tuple(neighbor) not in [item[1] for item in open_set] or tentative_g_score < g_score.get(tuple(neighbor), float('inf')):
#                 came_from[tuple(neighbor)] = current
#                 g_score[tuple(neighbor)] = tentative_g_score
#                 f_score[tuple(neighbor)] = tentative_g_score + manhattan_distance(neighbor, goal)
#                 open_set.append((f_score[tuple(neighbor)], tuple(neighbor)))
#                 open_set.sort(key=lambda x: x[0])
#     return None


# starts = [[0, 0], [0, 1]]
# goals = [[4, 4], [2, 3]]
# grid = np.array([
#     [0, 0, 0, 0, 0],
#     [0, 1, 1, 1, 0],
#     [0, 1, 0, 0, 0],
#     [0, 1, 1, 1, 0],
#     [0, 1, 0, 0, 0]
# ])
# avoid_points = set()
# for start, goal in zip(starts, goals):
#     path = astar_search(start, goal, grid, avoid_points)
#     if path:
#         avoid_points.update(path)
#         print("Path from", start, "to", goal, ":", path)
# print("Avoid points:", avoid_points)
import numpy as np
import random
import time
# start_time = time.time()  
class Node:
    def __init__(self, position, parent=None, g=0):
        self.position = position  #  
        self.parent = parent
        self.g = g
        self.h = 0

def manhattan_distance(start, end):
    return np.sum(np.abs(np.array(end) - np.array(start)))

def get_adjacent_positions(current_position, avoid):
    x, y = current_position
    possible_moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]  
    #  
    valid_moves = [move for move in possible_moves if move not in avoid]
    return valid_moves

def astar_search(start_point, end_point, avoid, goods, id):
    open_list = [Node(tuple(start_point))]  #  
    closed_set = set()
    searched_nodes_count = 0
    while open_list:
        current_node = min(open_list, key=lambda node: node.g + node.h)
        open_list.remove(current_node)
        searched_nodes_count += 1
        if goods == 0 and searched_nodes_count > 80:
        #  
            return [[start_point,i+id] for i in range(20)]  #  
        if current_node.position == tuple(end_point):  #  
            path = []
            while current_node:
                path.append((current_node.position, current_node.g))
                current_node = current_node.parent
            
            return path[::-1]  #  

        closed_set.add(current_node.position)

        for adjacent_position in get_adjacent_positions(current_node.position, avoid):
            if adjacent_position in closed_set:
                continue
            new_node = Node(adjacent_position, current_node, current_node.g + 1)
            new_node.h = manhattan_distance(adjacent_position, tuple(end_point))  #  

            if not any(node.position == adjacent_position and new_node.g >= node.g for node in open_list):
                open_list.append(new_node)

    return None

def update_paths_if_shared_steps(paths):
    #  
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            #  
            for point_i in paths[i]:
                if point_i in paths[j]:
                    #  
                    update_path_index = i  # 
                    update_path = paths[update_path_index]
                    point_index = update_path.index(point_i)

                    #  
                    if point_index > 0:
                        # 
                        prev_point = (update_path[point_index - 1][0], update_path[point_index - 1][1] + 1)
                        #  
                        update_path.insert(point_index, prev_point)
                        #  
                        for k in range(point_index + 1, len(update_path)):
                            update_path[k] = (update_path[k][0], update_path[k][1] + 1)
                        #  
                        break  #  

#####---------------------------------------------------------------------------------------------------------------------      
#####nnext is fangzhen can delete
# map_size = 200
# map_grid = np.zeros((map_size, map_size), dtype=int)
# num_obstacles = map_size * map_size * 30 // 100
# avoid = set()
# #while len(avoid) < num_obstacles:
# #    obstacle = (random.randint(0, map_size-1), random.randint(0, map_size-1))
#  ##   avoid.add(obstacle)
# for ob in avoid:
#     map_grid[ob] = 1
# start_points = []
# end_points = []
# for _ in range(10):
#     # 
#     while True:
#         start = (random.randint(0, map_size-1), random.randint(0, map_size-1))
#         if map_grid[start] == 0:
#             start_points.append(start)
#             break
#     while True:
#         end = (start[0] + random.randint(-20, 20), start[1] + random.randint(-20, 20))
#         if map_grid[end] == 0 and end not in start_points and 0 <= end[0] < map_size and 0 <= end[1] < map_size:
#             end_points.append(end)
#             break    

    
    # while True:
    #     end = (start[0] + random.randint(-20, 20), start[1] + random.randint(-20, 20))
    #     if map_grid[end] == 0 and end not in start_points and 0 <= end[0] < map_size and 0 <= end[1] < map_size:
    #         end_points.append(end)
    #         break
# start_points = [(4, 2), (0, 2)]
# end_points = [(0, 4), (4, 4)]
# #  
# avoid = [(1, 1), (1, 2), (1, 3),(2, 1), (3, 1), (3, 2),(3, 3),(4, 1)]
        
###above could deleted
###------------------------------------------------------------------------------------------------------------------------------
## youhua suanfa
# paths = []
# goods = 0
# for start_point, end_point in zip(start_points, end_points):
#     path = astar_search(start_point, end_point, avoid, goods)
#     paths.append(path)
     
# update_paths_if_shared_steps(paths)
# for i, path in enumerate(paths):

#     print(f"Path from {start_points[i]} to {end_points[i]}: {path}")


# end_time = time.time() 
# print(f"time: {end_time - start_time}  s")
#     [0, 0, 0, 0, 0],
#     [0, 1, 1, 1, 0],
#     [0, 1, 0, 0, 0],
#     [0, 1, 1, 1, 0],
#     [0, 1, 0, 0, 0]
    