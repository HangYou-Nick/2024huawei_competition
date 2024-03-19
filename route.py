import numpy as np

def read_map(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    robot_num = 0
    goods = 0
    boat_wharf = 0
    nrows, ncols = len(lines), len(lines[0].strip())
    map_data = np.ones((nrows, ncols), dtype=np.float32) * np.inf  # 初始化地图数据，障碍物处为无穷大
    start, end ,mid= None, None,  None# 起点和终点
 ## 初始化机器人的位置，货物，码头，海，陆地
    for i, line in enumerate(lines):
        for j, char in enumerate(line.strip()):
            if char == 'A':
                start[robot_num] = (robot_num,i, j)
                robot_num = robot_num+1
            #elif char == 'O':
 ##               directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
##                for dx, dy in directions:
 ##                   x = i + dx
  ##                  y = j + dy
  ##                  if char(x,y) == ".":   
  ##              mid[goods] = (i, j)
   ##             goods=goods+1
                #mid[goods].money =应该赋值的东西
            elif char == 'B':
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for dx, dy in directions:
                    x = i + dx
                    y = j + dy
                    if char(x,y) == ".":                       
                        end[boat_wharf] = (boat_wharf,i, j)
                        boat_wharf = boat_wharf  + 1
            elif char == '#':       #char.isdigit():  # 不可通行区域，障碍物
                map_data[i, j] = 0  # 或者是速度的倒数，取决于具体问题
            elif char == '*':       #char.isdigit():  # 不可通行区域，海   数字表示速度
                map_data[i, j] = -1
    

    return map_data, start, end,mid ,robot_num , goods, boat_wharf

# 读取地图
map_data, start, end = read_map('map.txt')

#start[robot_num] = (i, j)
#mid[goods] = (i, j)
# 考虑将货物的前两个数据存为位置i,j，第三个元素为价值；
def extreme_point(start_, end_):  ##寻找码头代码(去重复点的)
    start_point = start_ [: ,1,2]
    end_point = end_[: ,1,2]
    start = np.repeat(start_point, end_.shape[0], axis = 0)#目标点膨胀
    end = np.tile(end_point, (start_.shape[0], 1))   ##终点膨胀

    row_sums = np.sum(np.abs(start -  end), axis = 1)##计算步数之和
    # with_money = row_sums * mid[: , 3]     ##和钱乘

    sub_arrays = row_sums.reshape(-1, end_.shape[0])
    min_indices = np.argmin(sub_arrays, axis = 1)##第i个数据对应的数字是它需要找的港口
    # 找到每个子数组中的最小值及其索引
    min_values = np.min(sub_arrays, axis=1)

    # 构建新的矩阵
    new_matrix = np.zeros((10, 2))
    # 处理重复数值的情况
    unique_indices, counts = np.unique(min_indices, return_counts=True)
    for idx, count in zip(unique_indices, counts):
        if count > 1:
         # 在分割块中除去对应行
            sub_array = sub_arrays[idx]
            sub_array[min_indices[idx]] = np.inf

            # 重新找到最小值及其索引
            new_min_value = np.min(sub_array)
            new_min_index = np.argmin(sub_array)

            # 更新新的矩阵
            new_matrix[idx, 0] = new_min_value
            new_matrix[idx, 1] = new_min_index
        else:
            new_matrix[idx, 0] = min_values[idx]
            new_matrix[idx, 1] = min_indices[idx]
    robot_start = np.zeros((start_, 3))
    robot_end = np.zeros((start_, 3))
    robot_start[:,0] = np.arange(new_matrix)
    robot_start[:,1:] = start_point 
    robot_end[:,0] = new_matrix[:,1]
    indices = robot_end[:, 0].astype(int)
    robot_end[:, 1:] = end_point[indices, :]
    return (robot_start, robot_end)


def bfs_find_nearest(grid, start ): ##寻找货物代码
    global aim_goods
    # 定义移动方向（上，下，左，右）
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # 创建队列，并将起点加入队列
    queue = np.array([start])
    # 记录已访问的位置
    visited = np.zeros_like(grid)
    visited[start[0], start[1]] = 1
    # 从起点开始搜索
    while queue:
        x, y = queue.popleft()
        # 检查当前位置是否为目标
        if grid[x][y] == 'T' and (x,y) not in aim_goods:
            aim_goods.append[(x, y)]
            return ((x, y))  # 返回找到的目标位置
        # 将相邻的位置加入队列
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # 确保新位置在网格范围内，且未被访问，且不是墙壁
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and (nx, ny) not in visited :
                queue.append((nx, ny))
                visited.add((nx, ny))
    return None  # 如果没有找到目标，返回None

def bfs_all (start_,grid):
    start_positions = start_[:,1:]
    robot_goods = []
    for start in start_positions:
        point = start + [bfs_find_nearest(grid, start)]
        robot_goods.append(point)
    ##robot_goods
    return (robot_goods)
##A*算法
    #启发函数
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_numpy(grid, start, goal):
    nrows, ncols = len(grid), len(grid[0])
    open_set_flag = np.zeros((nrows, ncols), dtype=bool)  # 表示是否在open set中
    came_from = {}
    g_score = np.full((nrows, ncols), np.inf)  # 默认为无限大
    f_score = np.full((nrows, ncols), np.inf)
    g_score[start] = 0
    f_score[start] = manhattan_distance(start, goal)
    open_set_flag[start] = True

    while np.any(open_set_flag):  # 如果open set不为空
        # 找到f_score最小的点
        current = np.unravel_index(np.argmin(f_score + (1 - open_set_flag) * np.max(f_score)), (nrows, ncols))
        if current == goal:
            # 重建路径
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        open_set_flag[current] = False  # 从open set中移除
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < nrows and 0 <= neighbor[1] < ncols and grid[neighbor[0]][neighbor[1]] != 'X':
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    # 这是到该邻居的更好路径
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)
                    open_set_flag[neighbor] = True

    return None

def map_restar(map_data, positions):
    
    map_data = [[-1 if (i, j) in positions and 0 <= i < len(map_data) and 0 <= j < len(map_data[0]) else val for j, val in enumerate(row)] for i, row in enumerate(map_data)]

    return map_data