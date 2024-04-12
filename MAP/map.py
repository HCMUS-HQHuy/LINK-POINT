import numpy as np
from math import sqrt
from random import randint
from copy import copy
from copy import deepcopy

gray = (105,105,105)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0) 
blue = (0, 0, 255)
Lime = (0,255,0)
green = (0,128,0)
pink = (255,0,255)
purple = (128,0,128)
orange = (255,69,0)
yellow = (255,255,0)
darkred = (139,0,0)
Aqua = (0,255,255)
light_green = (0, 255, 127)
Brown = (244, 164, 96)
darkblue = (0, 0, 139)

background = (224, 255, 255)
orange_red = (255, 69, 0)

dx = np.array([1, -1, 0, 0])
dy = np.array([0, 0, 1, -1])

class Map:
    MAX_POINT = 12
    SIZE_BLOCK = 30
    color = np.array([purple, blue, green, yellow, pink, orange_red, Lime, darkblue, Brown, darkred, Aqua, light_green])
    n_pos_need_mask = 0
    cur_x = 0
    cur_y = 0
    is_picked = False

    def __init__(self, width, height, n_point):
        self.width = width
        self.height = height
        self.n_point = n_point
        self.n_point_rem = n_point
        self.done_node = np.zeros(n_point)
        self.array_map = np.zeros((width, height))
        self.done_pos = np.zeros((width, height))
        
        while True:
            for i in range(self.width):
                for j in range(self.height):
                    self.array_map[i, j] = -1

            array_tmp = copy(self.array_map)

            self.pos_color = [] 
            que = []

            for i in range(self.n_point):
                x = randint(0, width - 1)
                y = randint(0, height - 1)
                while self.array_map[x, y] != -1:
                    x = randint(0, width - 1)
                    y = randint(0, height - 1)
                self.pos_color.append([x, y])
                self.array_map[x, y] = i
                array_tmp[x, y] = i
                que.append([x, y])
                self.cur_x = x
                self.cur_y = y

            while len(que) != 0:
                u = que[randint(0, len(que) - 1)]
                que.remove(u)
                self.n_pos_need_mask = self.n_pos_need_mask + 1
                tmp = []
                for i in range(4):
                    v = [u[0] + dx[i], u[1] + dy[i]]
                    if (self.is_in_map(v[0], v[1]) and self.array_map[v[0], v[1]] == -1):
                        tmp.append(v)
                if (len(tmp) == 0):
                    self.array_map[u[0], u[1]] = array_tmp[u[0], u[1]]
                else:
                    v = tmp[randint(0, len(tmp) - 1)]
                    self.array_map[v[0], v[1]] = self.n_point
                    array_tmp[v[0], v[1]] = array_tmp[u[0], u[1]]
                    que.append(v)     
            if (self.posible_map() == True):
                break

    def roll_back(self, tmp):
        self = deepcopy(tmp)

    def posible_map(self):
        cnt = np.zeros(self.n_point)
        for i in range(self.width):
            for j in range(self.height):
                if self.array_map[i, j] != -1 and self.array_map[i, j] != self.n_point:
                    cnt[int(self.array_map[i, j])] += 1
                    for t in range(4):
                        if (self.is_in_map(i + dx[t], j + dy[t]) and self.array_map[i + dx[t], j + dy[t]] == self.array_map[i, j]):
                            return False
        for c in cnt:
            if (c != 2):
                return False
        return True

    def is_in_map(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def is_ok_pick(self):
        return self.array_map[self.cur_x, self.cur_y] != self.n_point and not self.done_node[int(self.array_map[self.cur_x, self.cur_y])] and self.array_map[self.cur_x, self.cur_y] != -1

    def is_can_move(self, pre_x, pre_y):
        x = self.cur_x
        y = self.cur_y
        if (not self.is_picked): return True
        if (self.array_map[x, y] == -1): return False
        if (self.done_pos[x, y] == True): return False
        if (self.array_map[x, y] == self.n_point): return True
        if (self.array_map[x, y] == self.array_map[pre_x, pre_y]): return True
        return False

    def move_point(self, move):
        if (move != 'LEFT' and move != 'RIGHT' and move != 'UP' and move != 'DOWN'):
            return
        pre_x = self.cur_x
        pre_y = self.cur_y       
    
        if (move == 'LEFT'):
            self.cur_x = self.cur_x - 1
        if (move == 'RIGHT'):
            self.cur_x = self.cur_x + 1
        if (move == 'UP'):
            self.cur_y = self.cur_y - 1
        if (move == 'DOWN'):
            self.cur_y = self.cur_y + 1

        if (not self.is_in_map(self.cur_x, self.cur_y) or not self.is_can_move(pre_x, pre_y)):
            self.cur_x = pre_x
            self.cur_y = pre_y
        elif self.is_picked: 
            self.done_pos[self.cur_x, self.cur_y] = True
            if self.array_map[self.cur_x, self.cur_y] == self.array_map[pre_x, pre_y]:
                self.is_picked = False
                self.done_node[int(self.array_map[pre_x, pre_y])] = True
                self.n_point_rem = self.n_point_rem - 1
            self.array_map[self.cur_x, self.cur_y] = self.array_map[pre_x, pre_y]
            self.n_pos_need_mask = self.n_pos_need_mask - 1
             
        # print(pre_x, pre_y, self.cur_x, self.cur_y)
 

    def can_go_to(self, x, y):
        que = [[x, y]]
        done = np.zeros((self.width, self.height))
        done[x][y] = True
        
        cur_color = self.array_map[x, y]
        while len(que) != 0:
            u = que[0] 
            que.pop(0)
            for i in range(4):
                v = [u[0] + dx[i], u[1] + dy[i]]
                if not self.is_in_map(v[0], v[1]) or self.done_pos[v[0], v[1]] or done[v[0], v[1]] == True:
                    continue
                done[v[0], v[1]] = True

                if self.array_map[v[0], v[1]] == cur_color:
                    return True
                if self.array_map[v[0], v[1]] == self.n_point:
                    que.append([v[0], v[1]])
        return False
    
    def exist_path_for_all_pair(self):
        state = True
        if self.is_picked: 
            state = self.can_go_to(self.cur_x, self.cur_y)
        if (state == False):
            print("có cặp không tìm được thấy nhau thỏa mãn mau hien tai")
            return False
        for [i, j] in self.pos_color:
            if self.array_map[i, j] != self.array_map[self.cur_x, self.cur_y]:
                if (not self.done_pos[i, j] and not self.can_go_to(i, j)):
                    print("có cặp không tìm được thấy nhau thỏa mãn", i, j, self.array_map[i, j])
                    return False
        return True

    def exit_pos_have_less_2_point_adj(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.array_map[i, j] == self.n_point:
                    cnt = 0
                    flag = 0
                    for t in range(4):
                        v = [i + dx[t], j + dy[t]]
                        if (self.is_in_map(v[0], v[1]) and self.array_map[v[0], v[1]] != -1 and (not self.done_pos[v[0], v[1]] or (v[0] == self.cur_x and v[1] == self.cur_y and self.is_picked))): 
                            cnt += 1
                            if (v[0] == self.cur_x and v[1] == self.cur_y and self.is_picked):
                                flag += 1
                    if cnt < 2: 
                        print("Tồn tại ô bé hơn 2 cạnh kề", i, j)
                        return True
                    elif (flag > 1): 
                        print("Tồn tại 2 ô mà không thể đến cùng lúc kề", i, j)
                        return True
                    
        return False

    def exist_block_imposible_to_paint(self):
        que = []
        done = np.zeros((self.width, self.height))
        
        for i in range(self.width):
            for j in range(self.height):
                if 0 <= self.array_map[i][j] < self.n_point and self.done_pos[i, j] == False:
                    que.append([i, j])

        while len(que) != 0:
            u = que[0] 
            que.pop(0)
            for i in range(4):
                v = [u[0] + dx[i], u[1] + dy[i]]
                if self.is_in_map(v[0], v[1]) and self.array_map[v[0], v[1]] == self.n_point and  done[v[0], v[1]] == False:
                    done[v[0], v[1]] = True
                    que.append([v[0], v[1]])
        for i in range(self.width):
            for j in range(self.height):
                if self.array_map[i][j] == self.n_point and done[i, j] == False:
                    print("NANI5")
                    return True
        return False

    def is_lost(self):
        
        if (self.exit_pos_have_less_2_point_adj()):
            return True
        if (not self.exist_path_for_all_pair()):
            return True
        if (self.exist_block_imposible_to_paint()):
            return True
        
        return False
    
    def print(self, pygame, screen): 
        T = self.SIZE_BLOCK
        gap = 50
        for i in range(self.width):
            for j in range(self.height):
                if self.array_map[i, j] == -1:
                    pygame.draw.rect(screen, gray, (gap + T * i + 1, gap * 2 + T * j + 1, T - 2, T - 2))
                elif self.array_map[i, j] == self.n_point:
                    pygame.draw.rect(screen, background, (gap + T * i + 1, gap * 2 + T * j + 1, T - 2, T - 2))
                else: 
                    pygame.draw.rect(screen, self.color[int(self.array_map[i, j])], (gap + T * i + 1, gap * 2 + T * j + 1, T - 2, T - 2))

                if (0 <= self.array_map[i, j] < self.n_point and not self.done_node[int(self.array_map[i, j])]):
                    tmp = sqrt(T * T * 2.0) / 2.0
                    if (self.array_map[i, j] == self.array_map[self.cur_x, self.cur_y]): 
                        pygame.draw.circle(screen, red, (gap + T * i + tmp - 6, gap * 2 + T * j + tmp - 6), tmp - 12)
                    

                if (i == self.cur_x and j == self.cur_y):
                    tmp = sqrt(T * T * 2.0) / 2.0
                    
                    if self.is_picked == True: pygame.draw.circle(screen, red, (gap + T * i + tmp - 6, gap * 2 + T * j + tmp - 6), tmp - 7)
                    else: pygame.draw.circle(screen, red, (gap + T * i + tmp - 6, gap * 2 + T * j + tmp - 6), tmp - 7, 5)
        
