import sys
import random
import time
n = 200
robot_num = 10
berth_num = 10
N = 210
class Robot:
    def __init__(self, robot_idx, startX=0, startY=0, goods=0, status=0, mbx=0, mby=0):
        self.robot_idx = robot_idx
        self.x = startX
        self.y = startY
        self.goods = goods
        self.status = status
        self.mbx = mbx
        self.mby = mby

    # 机器人的移动行为
    def move(self, id, direction):
        if isinstance(id, int) and 0 <= id <= 9:
            if direction == 0:
                self.x = self.x
                self.y = self.y + 1
            if direction == 1:
                self.x = self.x
                self.y = self.y - 1
            if direction == 2:
                self.x = self.x - 1
                self.y = self.y
            if direction == 3:
                self.x = self.x + 1
                self.y = self.y
        print("move", id, direction)

    # 机器人获取物品的行为
    def get(self, id):
        if isinstance(id, int) and 0 <= id <= 9:
            print("get", id)

    # 机器人卸载物品的行为
    def pull(self, id):
        if isinstance(id, int) and 0 <= id <= 9:
            print("pull", id)

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
        self.current_load = 0
    def ship(self, berth_idx):
        print("ship", self.boat_idx, berth_idx)
    def go(self):
        if self.current_load == boat_capacity:
            print("go", self.boat_idx)
    def load(self):
        if self.pos != -1 and self.status == 1:
            self.current_load += berth[self.pos].loading_speed
    def unload(self):
        if self.pos == -1 and self.status == 1:
            self.current_load = 0
boat = [Boat(i) for i in range(5)]


money = 0
boat_capacity = 0
id = 0
ch = []
gds = [[0 for _ in range(N)] for _ in range(N)]

def Init():
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
    okk = input()
    print("OK")
    sys.stdout.flush()

def offlineInit():
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
    sys.stdout.flush()

def Input():
    global id
    global money
    global gds
    id, money = map(int, input().split(" "))
    num = int(input())
    for i in range(num):
        x, y, val = map(int, input().split())
        gds[x][y] = val
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
            gds[x][y] = val
        for i in range(robot_num):
            robot[i].goods, robot[i].x, robot[i].y, robot[i].status = map(int, f.readline().split())
        for i in range(5):
            boat[i].status, boat[i].pos = map(int, f.readline().split())
    return id

if __name__ == "__main__":
    # Init()
    offlineInit()
    for zhen in range(1, 15001):
        id = offlineInput()
        # id = Input()
        for i in range(robot_num):
            print("move", i, random.randint(0, 3))
            sys.stdout.flush()
        print("OK")
        sys.stdout.flush()
