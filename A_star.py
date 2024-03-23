import numpy as np
import random
import time
start_time = time.time()  
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

def get_direction(from_node, to_node):
    dx = to_node[0] - from_node[0]
    dy = to_node[1] - from_node[1]
    if dx == 1 and dy == 0:
        return 0  # right
    elif dx == -1 and dy == 0:
        return 1  # left
    elif dx == 0 and dy == -1:
        return 2  # up
    elif dx == 0 and dy == 1:
        return 3  # down
    elif dx == 0 and dy == 0:
        return 5  # stop
    return 9  # 

def direction_to_delta(direction):
    if direction == 0:  #  
        return (1, 0)
    elif direction == 1:  #  
        return (-1, 0)
    elif direction == 2:  #  
        return (0, -1)
    elif direction == 3:  #  
        return (0, 1)
    elif direction == 5: 
        return (0, 0)
    return False  #  

def astar_search(start_point, end_point, avoid, goods):
    global moving_path
    global id
    open_list = [Node(tuple(start_point))]  #  
    closed_set = set()
    searched_nodes_count = 0
    while open_list:
        current_node = min(open_list, key=lambda node: node.g + node.h)
        open_list.remove(current_node)
        searched_nodes_count += 1
        if goods == 0 and searched_nodes_count > 400:
        #  
            return [[(start_point,i+id),5] for i in range(20)], True #  1-huo-matou-----2-huo-matou-huo+shijian-  gobal time  *hang*
        if current_node.position == tuple(end_point):  #  
            path = []

            while current_node and current_node.parent:
                direction = get_direction(current_node.parent.position, current_node.position)
                path.append(((current_node.position, current_node.g), direction))
                #print("siyuanzu",path)
                current_node = current_node.parent
            #returnpath = path[::-1]
            
            moving_path.append(path[::-1])
            #print("eee",moving_path)
            #returnpath = path[::-1]
            if len(moving_path ) > 1:
                update_paths_if_shared_steps(moving_path)
                print("sha",len(moving_path),len(moving_path[0]))
                now_path = moving_path[-1]
                 
                return now_path, moving_path, False  # 
            else:
                now_path = moving_path
                return now_path,moving_path,False
            
        closed_set.add(current_node.position)
        for adjacent_position in get_adjacent_positions(current_node.position, avoid):
            if adjacent_position in closed_set:
                continue
            new_node = Node(adjacent_position, current_node, current_node.g + 1)
            new_node.h = manhattan_distance(adjacent_position, tuple(end_point))  #  
            if not any(node.position == adjacent_position and new_node.g >= node.g for node in open_list):
                open_list.append(new_node)

def update_paths_if_shared_steps(paths):
    ## print( "path",path)
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            updated = False  #  
            for index_i, ((point_i, cost_i), direction_i) in enumerate(paths[i]):
                for (point_j, cost_j), direction_j in paths[j]:
                    #print ("position_j",point_i,point_j)
                    # if cost_j < id :
                    #     paths.pop(i)
                        ## 
                    if (point_i == point_j and cost_j == cost_i) or (point_i + direction_to_delta(direction_i)== point_j and point_j+direction_to_delta(direction_j) == point_i): #  
                        #   
                        if index_i > 0:  #  
                            #  
                            new_cost = paths[i][index_i - 1][0][1] + 1
                            paths[i][index_i - 1] = ((point_i, cost_i), 5)  #  
                            paths[i].insert(index_i, ((point_i, new_cost), direction_i))  #  
                            
                            #  
                            for k in range(index_i + 1, len(paths[i])):
                                old_position, old_cost = paths[i][k][0]
                                old_direction = paths[i][k][1]
                                paths[i][k] = ((old_position, old_cost + 1), old_direction)
                            
                            updated = True  #  
                            
                            break  #  
                if updated:
                    break  #  
            if updated:
                break  #  
#####---------------------------------------------------------------------------------------------------------------------      
#####nnext is fangzhen can delete
map_size = 200
map_grid = np.zeros((map_size, map_size), dtype=int)
num_obstacles = map_size * map_size * 30 // 100
avoid = set()
#while len(avoid) < num_obstacles:
#    obstacle = (random.randint(0, map_size-1), random.randint(0, map_size-1))
 ##   avoid.add(obstacle)
for ob in avoid:
    map_grid[ob] = 1
start_points = []
end_points = []
for _ in range(10):
    # 
    while True:
        start = (random.randint(50, map_size-51), random.randint(50, map_size-51))
        if map_grid[start] == 0:
            start_points.append(start)
            break
    while True:
        end = (start[0] + random.randint(-10, 10), start[0] + random.randint(-10, 10))
        if map_grid[end] == 0 and end not in start_points and 0 <= end[0] < map_size and 0 <= end[1] < map_size:
            end_points.append(end)
            break    

paths = []
goods = 0
id = 1
pre_time = time.time() 
moving_path= []
### youhangzhixing
for start_point, end_point in zip(start_points, end_points):

    Apath,_ = astar_search(start_point, end_point, avoid, goods)

    ##print("mmm",astar_search(start_point, end_point, avoid, goods,id))
    ##print("yinyongpath",Apath)
#paths.append(Apath)
# 
ptime = time.time() 
print("shicha",ptime-pre_time)
pre_time = ptime
mid_time = time.time() 
## 
update_paths_if_shared_steps(moving_path)## 
#
for i, Apath in enumerate(paths):

    print(f"Path from {start_points[i]} to {end_points[i]}: {Apath}")


end_time = time.time() 
print(f"time: {end_time - mid_time}  s")
print(f"time: {mid_time - start_time}  s")
#     [0, 0, 0, 0, 0],
#     [0, 1, 1, 1, 0],
#     [0, 1, 0, 0, 0],
#     [0, 1, 1, 1, 0],
#     [0, 1, 0, 0, 0]
    
