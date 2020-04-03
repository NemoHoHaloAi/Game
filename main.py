#!/usr/bin/env python
# coding=utf-8

import sys,random,math

import pygame
from pygame.color import THECOLORS as COLORS

# init pygame
pygame.init()

# create screen 500*500
SIZE = [900,900]
screen = pygame.display.set_mode(SIZE)

def draw_background(sc=screen):
    # white background
    screen.fill(COLORS['white'])

    # draw game board
    pygame.draw.rect(screen,COLORS['black'],(0,0,300,900),5)
    pygame.draw.rect(screen,COLORS['black'],(300,0,300,900),5)
    pygame.draw.rect(screen,COLORS['black'],(600,0,300,900),5)

    pygame.draw.rect(screen,COLORS['black'],(0,0,900,300),5)
    pygame.draw.rect(screen,COLORS['black'],(0,300,900,300),5)
    pygame.draw.rect(screen,COLORS['black'],(0,600,900,300),5)

cur_i, cur_j = 0,0
MATRIX = matrix = [([0]*9) for i in range(9)]
font80 = pygame.font.SysFont('Times', 80)
def draw_number(sc=screen):
    for i in range(len(MATRIX)):
        for j in range(len(MATRIX[0])):
            txt = font80.render(str(MATRIX[i][j]),True,COLORS['red'])
            screen.blit(txt,(i*100+30,j*100+10))

def check(matrix,i,j,number):
    if number in matrix[i]:
        return False
    if number in [row[j] for row in matrix]:
        return False
    group_i,group_j = int(i/3),int(j/3)
    if number in [matrix[i][j] for i in range(group_i*3,(group_i+1)*3) for j in range(group_j*3,(group_j+1)*3)]:
        return False
    return True

def create_sudoku(matrix=MATRIX,i=0,j=0):
    if i>8 or j>8:
        return matrix

    next_i,next_j = (i+1,0) if j==8 else (i,j+1)

    for number in range(1,10):
        if check(matrix,i,j,number):
            _matrix = [[col for col in row]for row in matrix]
            _matrix[i][j] = number
            return create_sudoku(_matrix,next_i,next_j)
    return matrix

MATRIX = create_sudoku()
print(MATRIX)

# background
draw_background(screen)

# main loop
running = True
while running:
    draw_background(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cur_i,cur_j = int(event.pos[0]/100),int(event.pos[1]/100)
        elif event.type == event.type == pygame.KEYUP:
            if chr(event.key) in ['1','2','3','4','5','6','7','8','9']:
                MATRIX[cur_i][cur_j] = chr(event.key)

    # choose item
    pygame.draw.rect(screen,COLORS['blue'],(cur_i*100+5,cur_j*100+5,100-10,100-10),0)

    # numbers
    draw_number(screen)

    # flip
    pygame.display.flip()

pygame.quit()
