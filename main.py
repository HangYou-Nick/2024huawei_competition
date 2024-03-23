import sys
import numpy as np


n = 200
robot_num = 10
berth_num = 10
N = 200


class Robot:
    def __init__(self, robot_idx, startX=0, startY=0, goods=0, status=0, mbx=0, mby=0):
        self.robot_idx = robot_idx
        self.x = startX
        self.y = startY
        self.goods = goods
        self.status = status
        self.mbx = mbx
        self.mby = mby
        self.stop = False

    def move(self, direction):
        print("move", self.robot_idx, direction)

    def get(self):
        print("get", self.robot_idx)

    def pull(self, id):
        print("pull", self.robot_idx)

robot = [Robot(i) for i in range(robot_num)]


class Berth:
    def __init__(self, berth_idx, x=0, y=0, transport_time=0, loading_speed=0, all_goods=0):
        self.berth_idx = berth_idx
        self.x = x
        self.y = y
        self.transport_time = transport_time
        self.loading_speed = loading_speed
        self.all_goods = all_goods

berth = [Berth(i) for i in range(berth_num)]


class Boat:
    def __init__(self, boat_idx, num=0, pos=0, status=0, flag=0):
        self.boat_idx = boat_idx
        self.num = num
        self.pos = pos
        self.status = status
        self.flag = flag
    def ship(self, berth_idx):
        print("ship", self.boat_idx, berth_idx)
    def go(self):
        print("go", self.boat_idx)
boat = [Boat(i) for i in range(5)]


money = 0
boat_capacity = 0
id = 0
ch = []
gds = [[0 for _ in range(N)] for _ in range(N)]
semantic_map = np.zeros((N, N), dtype=int)  # get initial semantic_map
goods_list = []
destination = []
obstacle_list = []

def extreme_point(start_, end_):
    start_point = [(item.x, item.y) for item in start_]
    start = np.repeat(start_point, len(end_), axis = 0)
    end = np.tile(end_, (len(start_), 1))[:, :2]

    row_sums = np.sum(np.abs(start -  end), axis = 1)

    sub_arrays = row_sums.reshape(-1, len(end_))
    min_indices = np.argmin(sub_arrays, axis = 1)
    min_values = np.min(sub_arrays, axis=1)

    new_matrix = np.zeros((10, 2))
    unique_indices, counts = np.unique(min_indices, return_counts=True)
    sub_arrays = sub_arrays.astype(np.float32)
    for idx, count in zip(unique_indices, counts):
        if count > 1:
            sub_array = sub_arrays[idx]
            sub_array[min_indices[idx]] = np.inf
            new_min_value = np.min(sub_array)
            new_min_index = np.argmin(sub_array)
            new_matrix[idx, 0] = new_min_value
            new_matrix[idx, 1] = new_min_index
        else:
            new_matrix[idx, 0] = min_values[idx]
            new_matrix[idx, 1] = min_indices[idx]
    robot_start = np.zeros((len(start_), 3))
    robot_end = np.zeros((len(start_), 3))
    robot_start[:,0] = np.arange(new_matrix.shape[0])
    robot_start[:,1:] = start_point 
    robot_end[:,0] = new_matrix[:,1]
    indices = robot_end[:, 0].astype(int)
    robot_end[:, 1:] = end[indices, :]
    return (robot_start, robot_end)

def manhattan_distance(start, end):
    return np.sum(np.abs(np.array(end) - np.array(start)))

def get_adjacent_positions(current_position, avoid):
    x, y = current_position
    possible_moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]  
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
    return None  # 

def astar_search(start_point, end_point, avoid, goods, id):
    open_list = [Node(tuple(start_point))]
    closed_set = set()
    searched_nodes_count = 0
    while open_list:
        current_node = min(open_list, key=lambda node: node.g + node.h)
        open_list.remove(current_node)
        searched_nodes_count += 1
        if goods == 0 and searched_nodes_count > 80:
            return [[start_point,i+id] for i in range(20)], True
        if current_node.position == tuple(end_point):
            path = []
            while current_node and current_node.parent:
                direction = get_direction(current_node.parent.position, current_node.position)
                path.append((current_node.position, current_node.g, direction))
                current_node = current_node.parent
            path.append((start_point, 0, 'Start'))  # 'Start'
            return path[::-1], False  # 
            
        closed_set.add(current_node.position)
        for adjacent_position in get_adjacent_positions(current_node.position, avoid):
            if adjacent_position in closed_set:
                continue
            new_node = Node(adjacent_position, current_node, current_node.g + 1)
            new_node.h = manhattan_distance(adjacent_position, tuple(end_point))  #  
            if not any(node.position == adjacent_position and new_node.g >= node.g for node in open_list):
                open_list.append(new_node)
    return None

def read_map():
    global ch
    global semantic_map
    robot_num = 0
    goods = 0
    boat_wharf = 0
    first_contact = 1
    for i in range(N):
        for j in range(N):
            char = ch[i][0][j]
            if char == '.' or char == 'A':  # for land, we give them 1.
                semantic_map[i][j] = 1

def renew_semantic_map(is_intial):
    global semantic_map
    global destination
    global obstacle_list
    if is_intial:
        for i in range(berth_num):
            start_pos = (berth[i].x, berth[i].y)
            for j in range(16):
                if j//4 == 0:
                    try:
                        is_land = ch[start_pos[0]+(j%4)][0][start_pos[1]-1] == "."
                        if is_land:
                            semantic_map[start_pos[0]+(j%4)][start_pos[1]] = 1
                            destination.append((start_pos[0]+(j%4), start_pos[1]))
                    except:
                        pass
                elif j//4 == 1:
                    try:
                        is_land = ch[start_pos[0]+4][0][start_pos[1]+(j%4)] == "."
                        if is_land:
                            semantic_map[start_pos[0]+3][start_pos[1]+(j%4)] = 1
                            destination.append((start_pos[0]+3, start_pos[1]+(j%4)))
                    except:
                        pass
                elif j//4 == 2:
                    try:
                        is_land = ch[start_pos[0]+(j%4)][0][start_pos[1]+4] == "."
                        if is_land:
                            semantic_map[start_pos[0]+(j%4)][start_pos[1]+3] = 1
                            destination.append((start_pos[0]+(j%4), start_pos[1]+3))
                    except:
                        pass
                elif j//4 == 3:
                    try:
                        is_land = ch[start_pos[0]-1][0][start_pos[1]+(j%4)] == "."
                        if is_land:
                            semantic_map[start_pos[0]][start_pos[1]+(j%4)] = 1
                            destination.append((start_pos[0], start_pos[1]+(j%4)))
                    except:
                        pass
        tmp = np.argwhere(semantic_map == 0).tolist()
        is_target = 0
        for item in tmp:
            neighbors = [(item[0]-1, item[1]), (item[0]+1, item[1]), (item[0], item[1]-1), (item[0], item[1]+1)]
            for one_neighbor in neighbors:
                if one_neighbor[0] < 0 or one_neighbor[1] < 0 or one_neighbor[0] >= N or one_neighbor[1] >= N:
                    continue
                if semantic_map[one_neighbor] == 1:
                    is_target = 1
                    break
            if is_target:
                obstacle_list.append(item)
                is_target = 0

def Init():
    global ch
    for i in range(0, n):
        line = input()
        ch.append([c for c in line.split(sep=" ")])
    for i in range(berth_num):
        line = input()
        berth_list = [int(c) for c in line.split(sep=" ")]
        id = berth_list[0]
        berth[id].x = berth_list[1]
        berth[id].y = berth_list[2]
        berth[id].transport_time = berth_list[3]
        berth[id].loading_speed = berth_list[4]
    global boat_capacity
    boat_capacity = int(input())
    read_map()
    renew_semantic_map(is_intial=True)
    okk = input()
    print("OK")
    sys.stdout.flush()

def offlineInit():
    global ch
    with open("maps/map1.txt", "r") as f:
        content = f.readlines()
    for i in range(0, n):
        line = content[i].replace("\n", "")
        ch.append([c for c in line.split(sep=" ")])
    with open("maps/meta1.txt", "r") as f:
        content = f.readlines()
    for i in range(berth_num):
        line = content[i].replace("\n", "")
        berth_list = [int(c) for c in line.split(sep=" ")]
        id = berth_list[0]
        berth[id].x = berth_list[1]
        berth[id].y = berth_list[2]
        berth[id].transport_time = berth_list[3]
        berth[id].loading_speed = berth_list[4]
    global boat_capacity
    boat_capacity = int(content[i+1])
    read_map()
    renew_semantic_map(is_intial=True)
    
    sys.stdout.flush()

def Input():
    global id
    global money
    global gds
    global goods_list
    id, money = map(int, input().split(" "))
    num = int(input())
    for i in range(num):
        x, y, val = map(int, input().split())
        # gds[x][y] = val\
        goods_list.append((x, y, val))
    for i in range(robot_num):
        robot[i].goods, robot[i].x, robot[i].y, robot[i].status = map(int, input().split())
    for i in range(5):
        boat[i].status, boat[i].pos = map(int, input().split())
    okk = input()
    return id

def offlineInput():
    global id
    global money
    global gds
    with open("maps/first_output1.txt", "r") as f:
        id, money = map(int, f.readline().split(" "))
        num = int(f.readline())
        for i in range(num):
            x, y, val = map(int, f.readline().split())
            goods_list.append((x,y,val))
        for i in range(robot_num):
            robot[i].goods, robot[i].x, robot[i].y, robot[i].status = map(int, f.readline().split())
        for i in range(5):
            boat[i].status, boat[i].pos = map(int, f.readline().split())
    return id

if __name__ == "__main__":
    Init()
    # offlineInit()

    paths = []
    robot_instructions_num = np.zeros(10, dtype=int)

    flag = 0
    
    for zhen in range(1, 15001):
        
        # id = offlineInput()
        id = Input()
        _, goal_for_each_robot = extreme_point(robot, goods_list)
        robot_pos = [(item.x, item.y) for item in robot]
        if zhen == 1:
            for idx, start_point, end_point in zip(range(10), robot_pos, goal_for_each_robot[:, 1:]):
                path, robot[idx].stop = astar_search(start_point, end_point, obstacle_list, 0, zhen)
                paths.append(path)
            for i in range(10):
                robot_instructions_num[i] = len(paths[i])
        # move robots
        for idx, path in enumerate(paths):
            if path[0][1] == zhen:
                if len(path[0]) == 3:
                    robot[idx].move(path[0][-1])
                path.pop(0)
                robot_instructions_num[idx] -= 1
        robot_finished = np.argwhere(robot_instructions_num == 0)
        robot_finished_num = robot_finished.shape[0]
        if robot_finished_num != 0:
            for i in range(robot_finished_num):
                robot_idx = robot_finished[i][0]
                if robot[robot_idx].stop:
                    _, goal_for_each_robot = extreme_point([robot[robot_idx]], goods_list)
                elif robot[robot_idx].goods:
                    robot[robot_idx].pull()
                    _, goal_for_each_robot = extreme_point([robot[robot_idx]], goods_list)
                else:
                    robot[robot_idx].get()
                    for idx, item in enumerate(goods_list):
                        if robot[robot_idx].x == item[0] and robot[robot_idx].y == item[1]:
                            goods_idx = idx
                            break
                    goods_list.pop(goods_idx)
                    _, goal_for_each_robot = extreme_point([robot[robot_idx]], destination)
                paths[robot_idx] = astar_search(robot_pos[robot_idx], goal_for_each_robot, obstacle_list, 0, zhen)
        # update_paths_if_shared_steps(paths)
        
        for i in range(5):
            if boat[i].flag % 2 == 0:
                j = i
            else:
                j = i + 5
            

            # 每次都是由虚拟点发往0-4号港口
            if boat[i].status == 1 and boat[i].pos == -1:
                boat[i].ship(j)
                boat[i].num = 0
                boat[i].flag += 1

            # 如果船到了某个港后且正在装载货物，则维护穿上的货物数量，并且判断是否需要运往虚拟点
            if boat[i].status == 1 and boat[i].pos != -1:
                # 判断是否需要将货物运往虚拟点
                if boat_capacity - boat[i].num < berth[j].loading_speed or zhen >= 15000 - max_transport_time - 1:
                    boat[i].go()

                # 更新船只上的货物数量
                if berth[i].all_goods >= berth[i].loading_speed:
                    boat[i].num += berth[i].loading_speed
                    berth[i].all_goods -= berth[i].loading_speed
                else:
                    boat[i].num += berth[i].all_goods
                    berth[i].all_goods = 0
        print("OK")
        sys.stdout.flush()
