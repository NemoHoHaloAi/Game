import sys

import pygame
from pygame.color import THECOLORS as COLORS

from build import print_matrix,give_me_a_game,check

def draw_background():
    # white background
    screen.fill(COLORS['white'])

    # draw game board
    pygame.draw.rect(screen,COLORS['black'],(0,0,300,900),5)
    pygame.draw.rect(screen,COLORS['black'],(300,0,300,900),5)
    pygame.draw.rect(screen,COLORS['black'],(600,0,300,900),5)

    pygame.draw.rect(screen,COLORS['black'],(0,0,900,300),5)
    pygame.draw.rect(screen,COLORS['black'],(0,300,900,300),5)
    pygame.draw.rect(screen,COLORS['black'],(0,600,900,300),5)

def draw_choose():
    pygame.draw.rect(screen,COLORS['blue'],(cur_j*100+5,cur_i*100+5,100-10,100-10),0)

def check_win(matrix_all,matrix):
    if matrix_all == matrix:
        return True
    return False

def check_color(matrix,i,j):
    _matrix = [[col for col in row]for row in matrix]
    _matrix[i][j] = 0
    if check(_matrix,i,j,matrix[i][j]):
        return COLORS['green']
    return COLORS['red']

def draw_number():
    for i in range(len(MATRIX)):
        for j in range(len(MATRIX[0])):
            _color = check_color(MATRIX,i,j) if (i,j) in BLANK_IJ else COLORS['gray']
            txt = font80.render(str(MATRIX[i][j] if MATRIX[i][j] not in [0,'0'] else ''),True,_color)
            x,y = j*100+30,i*100+10
            screen.blit(txt,(x,y))

def draw_context():
    txt = font100.render('Blank:'+str(cur_blank_size)+'   Change:'+str(cur_change_size),True,COLORS['black'])
    x,y = 10,900
    screen.blit(txt,(x,y))

if __name__ == "__main__":
    # init pygame
    pygame.init()
    
    # contant
    SIZE = [900,1000]
    font80 = pygame.font.SysFont('Times', 80)
    font100 = pygame.font.SysFont('Times', 90)
    
    # create screen 500*500
    screen = pygame.display.set_mode(SIZE)
    
    # variable parameter
    cur_i, cur_j = 0,0
    cur_blank_size = int(sys.argv[1])
    cur_change_size = 0
    
    # matrix abount
    MATRIX_ANSWER,MATRIX,BLANK_IJ = give_me_a_game(blank_size=cur_blank_size)
    print(BLANK_IJ)
    print_matrix(MATRIX)
    
    # main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cur_j,cur_i = int(event.pos[0]/100),int(event.pos[1]/100)
            elif event.type == pygame.KEYUP:
                if chr(event.key) in ['1','2','3','4','5','6','7','8','9'] and (cur_i,cur_j) in BLANK_IJ:
                    MATRIX[cur_i][cur_j] = int(chr(event.key))
                    cur_blank_size = sum([1 if col==0 or col=='0' else 0 for row in MATRIX for col in row])
                    cur_change_size +=1
        # background
        draw_background()
        # choose item
        draw_choose()
        # numbers
        draw_number()
        # point
        draw_context()
        # flip
        pygame.display.flip()
    
        # check win or not
        if check_win(MATRIX_ANSWER,MATRIX):
            print('You win, smarty ass!!!')
            break
    
    pygame.quit()
