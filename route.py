# -*- coding: utf-8 -*-
import numpy as np
import random
# def read_map(filename):
#     with open(filename, 'r') as file:
#         lines = file.readlines()
#     robot_num = 0
#     goods = 0
#     boat_wharf = 0
#     nrows, ncols = len(lines), len(lines[0].strip())
#     map_data = np.ones((nrows, ncols), dtype=np.float32) * np.inf  # ��ʼ����ͼ���ݣ��ϰ��ﴦΪ�����?
#     start, end ,mid= None, None,  None# �����յ�
#  ## ��ʼ�������˵�λ�ã������ͷ������½��
#     for i, line in enumerate(lines):
#         for j, char in enumerate(line.strip()):
#             if char == 'A':
#                 start[robot_num] = (robot_num,i, j)
#                 robot_num = robot_num+1
#             #elif char == 'O':
#  ##               directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
# ##                for dx, dy in directions:
#  ##                   x = i + dx
#   ##                  y = j + dy
#   ##                  if char(x,y) == ".":   
#   ##              mid[goods] = (i, j)
#    ##             goods=goods+1
#                 #mid[goods].money =Ӧ�ø�ֵ�Ķ���
#             elif char == 'B':
#                 directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#                 for dx, dy in directions:
#                     x = i + dx
#                     y = j + dy
#                     if char(x,y) == ".":                       
#                         end[boat_wharf] = (boat_wharf,i, j)
#                         boat_wharf = boat_wharf  + 1
#             elif char == '#':       #char.isdigit():  # ����ͨ�������ϰ���
#                 map_data[i, j] = 0  # �������ٶȵĵ�����ȡ���ھ�������
#             elif char == '*':       #char.isdigit():  # ����ͨ�����򣬺�   ���ֱ�ʾ�ٶ�
#                 map_data[i, j] = 0
    

#     return map_data, start, end,mid ,robot_num , goods, boat_wharf

# # ��ȡ��ͼ
# # map_data, start, end = read_map('maps/map1.txt')

# #start[robot_num] = (i, j)
# #mid[goods] = (i, j)
# # ���ǽ������ǰ�������ݴ��?λ��i,j��������Ԫ��Ϊ��ֵ��

# def extreme_point(start_, end_):   
#     min_values = []
#     start_point = [item for item in start_]
#     start = np.repeat(start_point, len(end_), axis = 0)# 
#     end = np.tile(end_, (len(start_), 1))[:, :2]   ## 

#     row_sums = np.sum(np.abs(start -  end), axis = 1)## 
#     # with_money = row_sums * mid[: , 3]     ## 

#     sub_arrays = row_sums.reshape(-1, len(end_))
#     min_indices = np.argmin(sub_arrays, axis = 1)## 
#     #  
#     min_values = np.min(sub_arrays, axis=1) 
    
#     #  
#     new_matrix = np.zeros((10, 2))
#     #  
#     unique_indices, counts = np.unique(min_indices, return_counts=True)
#     sub_arrays = sub_arrays.astype(np.float32)
#     for idx, count in zip(unique_indices, counts):
#         if count > 1:
#          #  
#             sub_array = sub_arrays[idx]
#             sub_array[min_indices[idx]] = np.inf

#             # 
#             new_min_value = np.min(sub_array)
#             new_min_index = np.argmin(sub_array)

#             #  
#             new_matrix[idx, 0] = new_min_value
#             new_matrix[idx, 1] = new_min_index
#         else:
#             new_matrix[idx, 0] = min_values[idx]
#             new_matrix[idx, 1] = min_indices[idx]
#     robot_start = np.zeros((len(start_), 3))
#     robot_end = np.zeros((len(start_), 3))
#     robot_start[:,0] = np.arange(new_matrix.shape[0])
#     robot_start[:,1:] = start_point 
#     robot_end[:,0] = new_matrix[:,1]
#     indices = robot_end[:, 0].astype(int)
#     robot_end[:, 1:] = end[indices, :]
#     return (robot_start, robot_end)
import numpy as np

def extreme_point(start_, end_):
    #  
    start_point = np.array(start_)
    end_point = np.array(end_)
    
    #  
    start_expanded = np.repeat(start_point, len(end_), axis=0)
    end_expanded = np.tile(end_point, (len(start_), 1))
    
    #  
    distances = np.linalg.norm(start_expanded - end_expanded, axis=1, ord=1).reshape(len(start_), len(end_))
    
    #  
    min_indices = np.argmin(distances, axis=1)
    min_values = np.min(distances, axis=1)
    
    #  
    unique_end_indices = set()
    for i in range(len(min_indices)):
        #  
        while min_indices[i] in unique_end_indices:
            distances[i, min_indices[i]] = np.inf  #  
            min_indices[i] = np.argmin(distances[i])
            min_values[i] = distances[i, min_indices[i]]
        unique_end_indices.add(min_indices[i])
    
    #  
    robot_start = np.hstack([np.arange(len(start_)).reshape(-1, 1), start_point])
    robot_end = np.hstack([min_indices.reshape(-1, 1), end_point[min_indices]])
    
    return robot_start, robot_end






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

A,B = extreme_point(start_points,end_points)
print("A",A,"B",B)



# def extreme_point(start_, end_):  ##Ѱ����ͷ����(ȥ�ظ����?)
#     start_point = start_ [: ,1,2]
#     end_point = end_[: ,1,2]
#     start = np.repeat(start_point, end_.shape[0], axis = 0)#Ŀ�������?
#     end = np.tile(end_point, (start_.shape[0], 1))   ##�յ�����

#     row_sums = np.sum(np.abs(start -  end), axis = 1)##���㲽��֮��
#     # with_money = row_sums * mid[: , 3]     ##��Ǯ��

#     sub_arrays = row_sums.reshape(-1, end_.shape[0])
#     min_indices = np.argmin(sub_arrays, axis = 1)##��i�����ݶ�Ӧ������������Ҫ�ҵĸۿ�
#     # �ҵ�ÿ���������е���Сֵ��������
#     min_values = np.min(sub_arrays, axis=1)

#     # �����µľ���
#     new_matrix = np.zeros((10, 2))
#     # �����ظ���ֵ�����?
#     unique_indices, counts = np.unique(min_indices, return_counts=True)
#     for idx, count in zip(unique_indices, counts):
#         if count > 1:
#          # �ڷָ���г�ȥ��Ӧ��?
#             sub_array = sub_arrays[idx]
#             sub_array[min_indices[idx]] = np.inf

#             # �����ҵ���Сֵ��������
#             new_min_value = np.min(sub_array)
#             new_min_index = np.argmin(sub_array)

#             # �����µľ���
#             new_matrix[idx, 0] = new_min_value
#             new_matrix[idx, 1] = new_min_index
#         else:
#             new_matrix[idx, 0] = min_values[idx]
#             new_matrix[idx, 1] = min_indices[idx]
#     robot_start = np.zeros((start_, 3))
#     robot_end = np.zeros((start_, 3))
#     robot_start[:,0] = np.arange(new_matrix)
#     robot_start[:,1:] = start_point 
#     robot_end[:,0] = new_matrix[:,1]
#     indices = robot_end[:, 0].astype(int)
#     robot_end[:, 1:] = end_point[indices, :]
#     return (robot_start, robot_end)


# def bfs_find_nearest(grid, start ): ##Ѱ�һ������?
#     global aim_goods
#     # �����ƶ������ϣ��£����ң�
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#     # �������У��������������?
#     queue = np.array([start])
#     # ��¼�ѷ��ʵ�λ��
#     visited = np.zeros_like(grid)
#     visited[start[0], start[1]] = 1
#     # �����?ʼ����
#     while queue:
#         x, y = queue.popleft()
#         # ��鵱ǰλ���Ƿ��?Ŀ��
#         if grid[x][y] == 'T' and (x,y) not in aim_goods:
#             aim_goods.append[(x, y)]
#             return ((x, y))  # �����ҵ���Ŀ��λ��
#         # �����ڵ�λ�ü������?
#         for dx, dy in directions:
#             nx, ny = x + dx, y + dy
#             # ȷ����λ��������Χ�ڣ���δ�����ʣ��Ҳ���ǽ��
#             if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and (nx, ny) not in visited :
#                 queue.append((nx, ny))
#                 visited.add((nx, ny))
#     return None  # ���û���ҵ�Ŀ��?����None

# def bfs_all (start_,grid):
#     start_positions = start_[:,1:]
#     robot_goods = []
#     for start in start_positions:
#         point = start + [bfs_find_nearest(grid, start)]
#         robot_goods.append(point)
#     ##robot_goods
#     return (robot_goods)
