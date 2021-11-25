import pygame
import keyboard
from model import *
from view import *

Player1 = 0
Player2 = 0
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
pygame.init()


def init_operate_p1():
    addacc_x = 0
    addacc_y = 0
    if keyboard.is_pressed('w'):
        addacc_y += 0.5
    if keyboard.is_pressed('s'):
        addacc_y -= 0.5
    if keyboard.is_pressed('a'):
        addacc_x -= 0.5
    if keyboard.is_pressed('d'):
        addacc_x += 0.5
    return addacc_x, addacc_y


def init_operate_p2():
    addacc_x = 0
    addacc_y = 0
    if keyboard.is_pressed('up'):
        addacc_y += 0.5
    if keyboard.is_pressed('down'):
        addacc_y -= 0.5
    if keyboard.is_pressed('left'):
        addacc_x -= 0.5
    if keyboard.is_pressed('right'):
        addacc_x += 0.5
    return addacc_x, addacc_y


def game_over():
    pass


finished = False

FPS = 30
dt = 0
screen = pygame.display.set_mode((1024, 1024))

clock = pygame.time.Clock()
pygame.display.update()
field_drawer = Drawer(screen)

while not finished:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    # вызов обсчёта модели
    p1x, p1y = init_operate_p1()
    p2x, p2y = init_operate_p2()
    controls = [p1x, p1y, p2x, p2y]
    Player1, Player2, dt = tick(dt, controls)
    field_drawer.update(field)
    display_player(screen, RED, Player1)
    display_player(screen, BLUE, Player2)
    pygame.display.update()

pygame.quit()
