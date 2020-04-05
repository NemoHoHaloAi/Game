import sys

import pygame
from pygame.color import THECOLORS as COLORS

def draw_background():
    # white background
    screen.fill(COLORS['lightblue'])
    pygame.draw.rect(screen,COLORS['black'],(-100,902,3000,200),5)

def draw_tunnel():
    for x in tunnel_list:
        pygame.draw.rect(screen,COLORS['darkgreen'],(x,0,100,350),0)
        pygame.draw.rect(screen,COLORS['darkgreen'],(x+100,550,100,350),0)

def draw_bird():
    screen.blit(birdImg,[bird_x,bird_y])

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
    # bird
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
    if (left_up2[0]<=right_up1[0]<=right_up2[0]): # x,肯定是右侧线接触，因此判断bird的right即可
        if up and (left_up2[1]<=right_up1[1]<=left_down2[1]):
            return True
        elif (not up) and (left_up2[1]<=right_down1[1]<=left_down2[1]):
            return True
    return False


def check_dead():
    bird_rect = (bird_x,bird_y,70,70)
    if bird_rect[1]+bird_rect[3]>900:
        return True
    for x in tunnel_list:
        up_rect = (x,0,100,350)
        down_rect = (x+100,550,100,350)
        if rect_cover(bird_rect,up_rect) or rect_cover(bird_rect,down_rect,up=False):
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

    # brid
    birdPath = 'bird.png'
    birdImg = pygame.image.load(birdPath)

    # tunnel
    tunnel_list = [100,600,1100,1600,2100]
    
    # create screen 500*500
    screen = pygame.display.set_mode(SIZE)
    
    # variable parameter
    bird_x,bird_y = 700,450
    bird_v = 0
    count_time = 0

    # level
    speed = 5
    frame = 0.02
    
    # main loop
    running = True
    pause = False
    jump = False
    dead = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pause = not pause
            elif event.type == pygame.KEYUP:
                if chr(event.key) == ' ':
                    jump = True

        # update data
        if not pause and not dead:
            count_time += frame
            tunnel_list = [x-speed if x-speed>-200 else 2100 for x in tunnel_list ]

            if not jump:
                bird_v += G*frame
            else:
                bird_v = JUMP_V
                jump = False
            bird_y += frame*bird_v

        # background
        draw_background()
        # tunnel
        draw_tunnel()
        # choose item
        draw_bird()
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
        pygame.time.delay(int(frame*1000))

        # check win or not
        if check_dead():
            #print('You dead, dumb ass!!!')
            #break
            dead = True
    
    pygame.quit()
