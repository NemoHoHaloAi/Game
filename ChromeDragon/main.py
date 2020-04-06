import sys,random

import pygame
from pygame.color import THECOLORS as COLORS

def draw_background():
    # white background
    screen.fill(COLORS['lightblue'])
    pygame.draw.rect(screen,COLORS['black'],(-100,902,3000,200),5)
    pygame.draw.rect(screen,COLORS['darkgray'],(-100,802,3000,100),0)

def draw_dragon():
    pygame.draw.rect(screen,COLORS['darkred'],(dragon_x,dragon_y,dragon_width,dragon_height),0)

def draw_cactus():
    for x in cactus_list:
        pygame.draw.rect(screen,COLORS['darkgreen'],(x[0],730,40*x[1],100),0)

def draw_raven():
    for x in raven_list:
        pygame.draw.rect(screen,COLORS['black'],(x[0],800-x[1]*50,100,20),0)

def draw_context():
    txt = font50.render('Count time: '+str(int(count_time))+' S',True,COLORS['black'])
    x,y = 10,920
    screen.blit(txt,(x,y))

def draw_pause():
    s = pygame.Surface(SIZE, pygame.SRCALPHA)
    s.fill((255,255,255,220))
    screen.blit(s, (0,0))
    txt = font120.render('PAUSE',True,COLORS['darkgray'])
    x,y = 550,400
    screen.blit(txt,(x,y))

def draw_dead():
    s = pygame.Surface(SIZE, pygame.SRCALPHA)
    s.fill((255,255,255,240))
    screen.blit(s, (0,0))
    txt = font120.render('YOU DEAD',True,COLORS['black'])
    x,y = 450,400
    screen.blit(txt,(x,y))

def rect_cover(rect1,rect2,up=True):
    # dragon
    left_up1 = (rect1[0],rect1[1])
    left_down1 = (rect1[0],left_up1[1]+rect1[3])
    right_up1 = (left_up1[0]+rect1[2],rect1[1])
    right_down1 = (left_up1[0]+rect1[2],left_up1[1]+rect1[3])
    # tunnel
    left_up2 = (rect2[0],rect2[1])
    left_down2 = (rect2[0],left_up2[1]+rect2[3])
    right_up2 = (left_up2[0]+rect2[2],rect2[1])
    right_down2 = (left_up2[0]+rect2[2],left_up2[1]+rect2[3])
    # check
    if (left_up2[0]<=right_up1[0]<=right_up2[0]): # x,肯定是右侧线接触，因此判断dragon的right即可
        if up and (left_up2[1]<=right_up1[1]<=left_down2[1]):
            return True
        elif (not up) and (left_up2[1]<=right_down1[1]<=left_down2[1]):
            return True
    return False


def check_dead():
    dragon_rect = (dragon_x,dragon_y,dragon_width,dragon_height)
    if dragon_rect[1]+dragon_rect[3]>900:
        return True
    for x in cactus_list:
        down_rect = (x[0],730,x[1]*40,100)
        if rect_cover(dragon_rect,down_rect,up=False):
            return True
    for x in raven_list:
        down_rect = (x[0],800-x[1]*50,100,20)
        if rect_cover(dragon_rect,down_rect,up=False):
            return True
    return False

if __name__ == "__main__":
    # init pygame
    pygame.init()
    
    # contant
    SIZE = [1500,1000]
    font50 = pygame.font.SysFont('Times', 50)
    font120 = pygame.font.SysFont('Times', 120)
    G = 9.8*30 # g
    JUMP_V = -300
    FLOOR_Y = 800

    # create screen 500*500
    screen = pygame.display.set_mode(SIZE)
    
    # variable parameter
    cactus_list = [[300,1],[500,2],[900,2],[1200,1],[1500,1],[2000,2]]
    cactus_list = [[500,2],[1000,1],[1500,1],[2000,2]]
    raven_list = [[700,1],[1700,2]]
    dragon_x,dragon_y,dragon_width,dragon_height = 200,760,30,50
    dragon_v = 0
    count_time = 0
    jump_times = 2

    # level
    speed = 5
    frame = 0.02
    level = 1
    
    # main loop
    running = True
    pause = False
    jump = False
    lookdown = False
    dead = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pause = not pause
            elif event.type == pygame.KEYUP:
                if chr(event.key) == 'w':
                    if jump_times > 0:
                        jump_times -= 1
                        jump = True
                elif chr(event.key) == 's':
                    lookdown = True

        # update data
        if not pause and not dead:
            level = count_time/10+1
            count_time += frame/level
            cactus_list = [[x[0]-speed,x[1]] if x[0]-speed>-200 else [2200,random.choice([1,2])] for x in cactus_list ]
            raven_list = [[x[0]-speed,x[1]] if x[0]-speed>-200 else [2200,random.choice([1,2])] for x in raven_list ]

            if not jump:
                dragon_v += G*frame
            else:
                dragon_v = JUMP_V
                jump = False
            dragon_y = dragon_y+frame*dragon_v if dragon_y+frame*dragon_v < (FLOOR_Y-dragon_height) else (FLOOR_Y-dragon_height)
            if dragon_y >= (FLOOR_Y-dragon_height):
                jump_times = 2

        # background
        draw_background()
        # anamy
        draw_cactus()
        draw_raven()
        # choose item
        draw_dragon()
        # point
        draw_context()
        # pause
        if not dead and pause:
            draw_pause()
        # dead
        if dead:
            draw_dead()
        # flip
        pygame.display.flip()

        # pause 20ms
        pygame.time.delay(int(frame/level*1000))

        # check win or not
        if check_dead():
            #print('You dead, dumb ass!!!')
            #break
            dead = True
    
    pygame.quit()
