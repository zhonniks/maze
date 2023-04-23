
import os
import sys
import random
import pygame
from pygame import mixer
import random, time 
 
pygame.init()

# цвета
BLACK = (0, 0, 0)
GREY = (66, 73, 73)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
BLUE = (31, 97, 141)
YELLOW = (241, 196, 15)

#переменные для размеров 
WIDTH = 500
HEIGHT = 500
BLOCK_SIZE = 16 # размер  одной стороны каждого блока

# фонт для конца игры
font = pygame.font.SysFont("Verdana", 35) 
game_over = font.render("Game Over", True, BLACK)

# бэкграунд музыка
pygame.mixer.music.load("background.ogg")
pygame.mixer.music.set_volume(0.18)
mixer.music.play(-1)

# функция для создания разметки клеток на заднем плане
def draw_grid():
    for i in range(0, 500, BLOCK_SIZE): # для х: с 0 до 500 пикселей и через каждые 20 пикселей(блок-сайз)
        for j in range(0, 560, BLOCK_SIZE): # для у: с 0 до 500 пикселей и через каждые 20 пикселей(блок-сайз)
            pygame.draw.rect(screen, GREY, (i, j, BLOCK_SIZE, BLOCK_SIZE), 1) # рисует квадраты на координатах i и j c шириной и высотой равные  BLOCK_SIZE, и с толщиной стенки равный 1

# класс для желтка ( игрока )
class Player(object):
    
    def __init__(self):
        self.rect = pygame.Rect(32, 32, 16, 16)
 
    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy
 
        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
 
# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
 
# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
 
# Set up the display
pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((320, 240))
 
clock = pygame.time.Clock()
walls = [] # List to hold the walls
player = Player() # Create the player


level = [1,2]
with open(f'levels/level{random.choice(level)}.txt', 'r') as f: # читает с папки levels  файлы с названием level{порядковый номер}
    W_body = f.readlines()

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in W_body:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 16, 16)
        x += 16
    y += 16
    x = 0
 
running = True

#время за которое игрок должен пройти игру
counter, text = 100, '100'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
clock = pygame.time.Clock()

#запуск!
while running:
    
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    if counter == 0:
        screen.fill(RED) 
        screen.blit(game_over, (30,250))
        pygame.display.update() 
        time.sleep(10) 
        pygame.quit() 
    # Move the player if an arrow key is pressed
    
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)
    counter -= 0.03

    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect):
        f = open('record.txt','w')
        f.write(f"{int(counter)}")
        f.close()
        end = font.render(f'Your score is: {int(counter)}',True, BLACK)
        screen.fill(RED) 
        screen.blit(end, (10,250))
        pygame.display.update() 
        time.sleep(10) 
        pygame.quit()
        sys.exit()

     # Draw the scene
    screen = pygame.display.set_mode((500, 600))  
    screen.fill((0, 0, 0))
    draw_grid()
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)

    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    
    # time and record on screen
    font2 = pygame.font.SysFont("voltec", 35)
    text = font2.render(f'TIME: {int(counter)} sec', True, RED)
    screen.blit(text, (30, 565))
    with open('record.txt','r') as f:
        rec = f.readlines()
    txt = font2.render(f'RECORD: {rec[0]}', True, RED)
    screen.blit(txt , (250, 565))

    pygame.display.flip()
    clock.tick(360)
 
pygame.quit()