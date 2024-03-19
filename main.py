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
            print("move", id, direction)

    # 机器人获取物品的行为
    def get(self, id):
        if isinstance(id, int) and 0 <= id <= 9:
            # self.status = 1
            print("get", id)

    # 机器人卸载物品的行为
    def pull(self, id):
        if isinstance(id, int) and 0 <= id <= 9:
            # self.status = 0
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
    def ship(self, berth_idx):
        if self.status == 1 and self.pos != berth_idx:
            print("ship", self.boat_idx, berth_idx)
            sys.stdout.flush()
    def go(self):
        # print(f"boat {self.boat_idx}", self.num, file=sys.stderr)
        # sys.stderr.flush()
        if boat_capacity - self.num < berth[self.pos].loading_speed:
        # if boat_capacity == self.num and self.pos != -1 and self.status == 1:
            print("go", self.boat_idx)
            sys.stdout.flush()
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


def getDirection():
    a = 1


if __name__ == "__main__":
    #Init()
    offlineInit()

    sorted_berth = sorted(berth, key=lambda x: x.loading_speed, reverse=True) # 按照搬运速度进行降序排序
    berth_pos = []
    for i in range(5):
        berth_pos.append([sorted_berth[i].x, sorted_berth[i].y])

    # for i in range(len(berth)):
    #     print(sorted_berth[i].x, sorted_berth[i].y, sorted_berth[i].transport_time, sorted_berth[i].loading_speed)

    for zhen in range(1, 15001):
        id = offlineInput()
        # id = Input()

         # 货物的位置如何表示
        goods_pos  = [(i, j) for i in range(len(gds)) for j in range(len(gds[i])) if gds[i][j] != 0]

        directionList = getDirection() # y由算法得到每个机器人应该朝着什么方向前进
        for i in range(robot_num):
            robot[i].move(i, directionList[i])
            robot_pos = [robot[i].x, robot[i].y]
            
            if robot_pos in goods_pos:
                robot[i].get(i)
            if robot_pos in berth_pos:
                robot[i].pull(i)

        for i in range(5):
            boat[i].ship(i)
            boat[i].go()
        print("OK")
        sys.stdout.flush()