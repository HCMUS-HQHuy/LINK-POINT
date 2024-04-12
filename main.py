import pygame
from time import sleep
from MAP.map import Map
from copy import deepcopy
from time import time

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

pygame.init()

width = 400
height = 500
time_limit = 30

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Link point')
# icon = pygame.image.load('IMAGE\imagination.png')
# pygame.display.set_icon(icon)

def clear_screen():
    screen.fill(black)
    print_on_game("CREATOR: HQH", 190, 470, white)

def Get_Control(): 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "EXIT GAME"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "END GAME"
            if event.key == pygame.K_r:
                return "RE_GAME"
            if event.key == pygame.K_SPACE:
                return 'PICK'
            if event.key == pygame.K_LEFT:
                return 'LEFT'
            if event.key == pygame.K_RIGHT:
                return 'RIGHT'
            if event.key == pygame.K_UP:
                return 'UP'
            if event.key == pygame.K_DOWN:
                return 'DOWN'
            if event.key == pygame.K_y:
                return 'YES'
            if event.key == pygame.K_n:
                return 'NO'
    return 'NUL'
 
def print_on_game(TEXT, x, y, color): 
    font = pygame.font.Font(None, 36)
    text = font.render(TEXT, True, color)
    # Vẽ chữ lên màn hình
    screen.blit(text, (x, y))
    pygame.display.update()

class Link_points:

    def __init__(self, n_point):
        self.fps = 30
        self.clock = pygame.time.Clock() 
        self.game_map = Map(10, 10, n_point)
        self.game_backup = deepcopy(self.game_map)


    def get_statement(self, is_checked):
        if is_checked and self.game_map.is_lost():
            return "YOU LOST"
        
        if self.game_map.n_point_rem == 0:
            return "YOU WIN"
        return "NUL"
    
    def roll_back(self):
        self.game_map = deepcopy(self.game_backup)

    def start_game(self): 
        clear_screen()
        print_on_game("Time remain:", 10, 60, green)
        start = time()
        while True:
            rem = time_limit - (time() - start)
            for  i in range(time_limit):
                if i < rem: pygame.draw.rect(screen, green, (50 + 10 * i + 1, 89, 9, 10))
                else: pygame.draw.rect(screen, black, (50 + 10 * i + 1, 89, 9, 10))
            if rem <= 0:
                print_on_game("TIME'S UP..", 10, 10, red)
                return True
            
            Command = Get_Control()
            if (Command == "EXIT GAME"):
                exit()
            
            if (Command == 'END GAME'):
                return False

            if (Command == 'PICK' and self.game_map.is_ok_pick()): 
                self.game_map.is_picked = True
                self.game_map.done_pos[self.game_map.cur_x, self.game_map.cur_y] = True
                self.game_map.n_pos_need_mask = self.game_map.n_pos_need_mask - 1
            save_is_picked = self.game_map.is_picked
            self.game_map.move_point(Command)
            self.game_map.print(pygame, screen)
            FINISH_GAME = self.get_statement(save_is_picked)
            if FINISH_GAME != "NUL":
                if FINISH_GAME == "YOU LOST": print_on_game(FINISH_GAME, 10, 10, red)
                if FINISH_GAME == "YOU WIN": print_on_game(FINISH_GAME, 10, 10, green)
                if (FINISH_GAME == "YOU LOST"):
                    return True
                sleep(2.0)
                return False
            pygame.display.update()
            # self.clock.tick(self.fps)    

NUM_POINT_GAME = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]] 
TEXT_NUM_POINT_GAME = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]

clear_screen() 
print_on_game("TRAIN HOW TO PLAY?(Y/N)", 10, 10, white)

train = False

while True:
    T = Get_Control()
    if T == "YES":
        train = True
        break
    elif T == "NO":
        break
    elif T == "EXIT GAME":
        exit()

if train:
    clear_screen() 
    print_on_game("* space", 10, 10, green)
    print_on_game(": to choose", 100, 10, white)
    print_on_game("* arrow", 10, 40, green)
    print_on_game(": to move", 100, 40, white)
    print_on_game("* ESC", 10, 70, green)
    print_on_game(": to escape game", 100, 70, white)
    print_on_game("cannot undo step", 10, 110, red)
    print_on_game("your target:", 10, 150, red)
    print_on_game("fill every cell in map.", 150, 150, white)
    print_on_game("by linking points of same color", 10, 180, white)
    print_on_game("press space to start game :D", 10, 300, blue)
    while True:
        T = Get_Control()
        if T == "EXIT GAME":
            exit()
        if T == "PICK":
            break



while True:
    
    clear_screen()

    print_on_game("CHOSE YOUR 'BRAIN':", 10, 10, green)
    pos = [0, 0]
    start_game = True
    while True:
        dir = Get_Control()  
        if (dir == "EXIT GAME"):
            exit()
        if (dir == "END GAME" or dir == "PICK"):
            if (dir == "END GAME"): 
                start_game = False
            break
        if (dir == "LEFT"):
            pos[0] -= 1
        if (dir == "RIGHT"):
            pos[0] += 1
        if (dir == "UP"):
            pos[1] -= 1
        if (dir == "DOWN"):
            pos[1] += 1
        if (pos[0] < 0): pos[0] += 1
        if (pos[1] < 0): pos[1] += 1
        if (pos[0] >= 3): pos[0] -= 1
        if (pos[1] >= 4): pos[1] -= 1
        for i in range(3):
            for j in range(4):
                color = white
                if (pos == [i, j]): color = red
                print_on_game(TEXT_NUM_POINT_GAME[NUM_POINT_GAME[i][j]], 50 + i * 100, 100 + j * 100, color)

    if (start_game):
        game = Link_points(NUM_POINT_GAME[pos[0]][pos[1]])
        while True:
            T = game.start_game()
            again = False
            if (T == True):
                while True:
                    print_on_game("REPLAY? (Y/N)", 130, 410, white)
                    T = Get_Control()
                    if T == "YES":
                        again = True
                        break
                    elif T == "NO":
                        break
                    elif T == "EXIT GAME":
                        exit()
            if (again): 
                # print(game_backup.game_map)
                game.roll_back()
            else: break    

    clear_screen()
    print_on_game("PRESS ESC TO EXIT", 10, 10, white)
    print_on_game("R TO REGAME", 10, 40, white)
    re_game = Get_Control()
    while True:
        if (re_game == "RE_GAME" or re_game == "END GAME" or re_game == "EXIT GAME"):
            break
        re_game = Get_Control()
    if (re_game == "RE_GAME"): 
        continue
    break