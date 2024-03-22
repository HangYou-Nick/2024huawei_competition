import sys
import numpy as np
import random
import time
from route import extreme_point
from A_star import astar_search, update_paths_if_shared_steps


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
    def __init__(self, berth_idx, x=0, y=0, transport_time=0, loading_speed=0):
        self.berth_idx = berth_idx
        self.x = x
        self.y = y
        self.transport_time = transport_time
        self.loading_speed = loading_speed

berth = [Berth(i) for i in range(berth_num)]


class Boat:
    def __init__(self, boat_idx, num=0, pos=0, status=0):
        self.boat_idx = boat_idx
        self.num = num
        self.pos = pos
        self.status = status
    def ship(self, berth_idx):
        if self.status == 1 and self.pos != berth_idx:
            print("ship", self.boat_idx, berth_idx)
    def go(self):
        # print(f"boat {self.boat_idx}", self.num, file=sys.stderr)
        # sys.stderr.flush()
        if boat_capacity - self.num < berth[self.pos].loading_speed:
        # if boat_capacity == self.num and self.pos != -1 and self.status == 1:
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
        pass



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
    # Init()
    offlineInit()
    
    # sorted_berth = sorted(berth, key=lambda x: x.loading_speed, reverse=True) # 按照搬运速度进行降序排序
    # berth_pos = []
    # for i in range(5):
    #     berth_pos.append([sorted_berth[i].x, sorted_berth[i].y])

    # for i in range(len(berth)):
    #     print(sorted_berth[i].x, sorted_berth[i].y, sorted_berth[i].transport_time, sorted_berth[i].loading_speed)
    paths = []
    robot_instructions_num = np.zeros(10, dtype=int)
    for zhen in range(1, 15001):
        
        id = offlineInput()
        # id = Input()
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
            if path[-1] == id:
                robot[idx].move(path[0])
                paths[idx] = path.pop(0)
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
                    _, goal_for_each_robot = extreme_point([robot[robot_idx]], destination)
                paths[robot_idx] = astar_search(robot_pos[robot_idx], goal_for_each_robot, obstacle_list, 0, zhen)
        pass
        # update_paths_if_shared_steps(paths)
        print("OK")
        sys.stdout.flush()
