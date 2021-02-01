import pygame
from pygame.draw import *
from random import randint
import math
import pygame.freetype
pygame.init()

FPS = 30 # Кол-во кадров в секунду
SCREEN_WIDTH = 1200 # Ширина экрана
SCREEN_HEIGHT = 900 # Высота экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

''' Значения цветов '''
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

MAX_BALLS = 5 # Максимальное кол-во шариков на экране

SCORE_CIRCLE = 1
SCORE_SQUARE = 2

try:
    file = open('scoreboard.txt', 'r')
except:
    print("Scoreboard file not found. Creating a new one")
    file = open('scoreboard.txt', 'w')
    file.close()
    file = open('scoreboard.txt', 'r')

def open_file(file):
	Data = dict()
	lines = file.readlines()
	for line in lines:
		name, score = line.split()
		score = int(score)
		Data[name] = score

	file.close()
	return Data


'''   lines = file.readlines()
    data = [[], []]
    for i in lines:
        data[0].append(list(i.split())[0])
        data[1].append(list(i.split())[1])
    file.close()
    return data
'''
def save_file(data, file): 
   for name in data:
        print(name, str(data[name]), file=file)

Data = open_file(file)
file = open('scoreboard.txt', 'w')
player_name = input("Enter your name: ")
if not (player_name in Data):
    Data[player_name] = 0



#def test(data):
#    data = 0
#test(data)
#print(data)

def display_score(score):
    FONT = pygame.freetype.Font("Calibri.ttf", 50)
    FONT.render_to(screen, (50, 50), "Score: " + str(score), (70, 70, 0))

def display_scoreboard(file_data, x, y):
    FONT = pygame.freetype.Font("Calibri.ttf", 50)
    FONT.render_to(screen, (x, y), "Scoreboard", (0, 200, 0))
    i = 0
    for name in file_data:
        #print(data)
        FONT.render_to(screen, (x, y + 55 * (i + 1)), name + " " + str(file_data[name]), (0, 150, 0))
        i += 1
def draw_ball(x, y, r, color):
    '''рисует шарик '''
    circle(screen, color, (x, y), r)

def draw_square(x, y, r, color):
    polygon(screen, color, [(x - r, y - r), (x - r, y + r), (x + r, y + r), (x + r, y - r)])

def check_ball_click(ball_x, ball_y, ball_r, mouse_pos):
    '''Функция принимает координаты и радиус шарика, координаты мыши. Если мышь нажала на шарик,
    то возращает True, в противном случае False'''

    #print("Checking ball click", ball_x, ball_y, ball_r, mouse_pos)
    distance = math.sqrt(abs(ball_x - mouse_pos[0]) ** 2 + abs(ball_y - mouse_pos[1]) ** 2)
    if distance <= ball_r:
        return True
    return False

def check_square_click(square_x, square_y, square_r, mouse_pos):
    if abs(square_x - mouse_pos[0]) <= square_r and abs(square_y - mouse_pos[1]) <= square_r:
        return True
    return False

def check_balls_click(balls, mouse_pos):
    ''' Функция возвращает номера всех нажатых шариков и квадратов '''
    ans = []
    for i in range(len(balls) - 1, -1, -1):
        if balls[i][7] == 1:
            if check_ball_click(balls[i][3], balls[i][4], balls[i][5], mouse_pos):
                ans.append(i)
        else:
            if check_square_click(balls[i][3], balls[i][4], balls[i][5], mouse_pos):
                ans.append(i)
    #print(ans)
    return ans


pygame.display.update()
clock = pygame.time.Clock()
finished = False
score = Data[player_name] # Счет игрока
balls = [] # Этот массив содержит данные всех шариков и квадратов

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in check_balls_click(balls, event.pos):
                #print(i, len(balls))
                if balls[i][7] == 1:
                    score += SCORE_CIRCLE
                else:
                    score += SCORE_SQUARE
                balls.pop(i)
            Data[player_name] = str(score)
            #print(data, player_number)
                #print(score)
    for i in range(len(balls), MAX_BALLS): # Заполнить масив шариков
        ball_frames = 1
        ball_speed_x = randint(-8, 8)
        ball_speed_y = randint(-8, 8)
        ball_r = randint(40, 100)
        ball_x = randint(ball_r + 50, SCREEN_WIDTH - ball_r - 50)
        ball_y = randint(ball_r + 50, SCREEN_HEIGHT - ball_r - 50)
        color = COLORS[randint(0, 5)]
        shape = randint(30, 70) // 30
        balls.append([ball_frames, ball_speed_x, ball_speed_y, ball_x, ball_y, ball_r, color, shape])
        #print("Ball added", len(balls))
    for i in range(len(balls)):
        #print("Ball scanned")
        ball = balls[i]
        ball_frames = ball[0]
        ball_speed_x = ball[1]
        ball_speed_y = ball[2]
        ball_x = ball[3]
        ball_y = ball[4]
        ball_r = ball[5]
        color = ball[6]
        shape = ball[7]

        ball_frames += 1

        # Если шарик врезается в стену, его скорость нужно перевернуть
        if ball_x <= ball_r or ball_x >= SCREEN_WIDTH - ball_r:
            ball_speed_x *= -1
        elif ball_y <= ball_r or ball_y >= SCREEN_HEIGHT - ball_r:
            ball_speed_y *= -1

        # Перемещение шарика
        ball_x += ball_speed_x
        ball_y += ball_speed_y
        if color[0] >= 255:
            color = (0, color[1], color[2])
        else:
            color = (color[0] + 1, color[1], color[2])
        #print(color[0])

        # Отрисовка шарика
        if shape == 1:
            draw_ball(ball_x, ball_y, ball_r, color)
        else:
            draw_square(ball_x, ball_y, ball_r, color)

        balls[i] = [ball_frames, ball_speed_x, ball_speed_y, ball_x, ball_y, ball_r, color, shape]
    display_score(score)
    display_scoreboard(Data, SCREEN_WIDTH - 350, 50)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
save_file(Data, file)
print("Scoreboard saved")
file.close()