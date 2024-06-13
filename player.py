import pygame
from drawer import *
move_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_a, pygame.K_s, pygame.K_w, pygame.K_d]
def move_player(maze_object, unit_size):
    maze = maze_object.maze
    keys = pygame.key.get_pressed()
    cord = ()
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 'p':
                cord = (y, x)
                break
        if cord: break 
    act_key = 0
    for key in move_keys:
        if keys[key]: 
            act_key = key
            break
    if act_key in [pygame.K_DOWN, pygame.K_s] and y < len(maze) - 1:
        next_cord = (y + 1, x)
    elif act_key in[pygame.K_UP, pygame.K_w] and y > 0:
        next_cord = (y - 1, x)
    elif act_key in [pygame.K_LEFT, pygame.K_a] and x > 0:
        next_cord = (y, x - 1)
    elif act_key in [pygame.K_RIGHT, pygame.K_d] and x < len(maze[0]) - 1:
        next_cord = (y, x + 1)
    else: next_cord = (y, x)
    if maze[next_cord[0]][next_cord[1]] != 1:
        maze[cord[0]][cord[1]] = 0
        maze[next_cord[0]][next_cord[1]] = 'p'
    else:
        next_cord = cord
    pygame.time.delay(200)
    return (cord[0] * unit_size, cord[1] * unit_size), (next_cord[0] * unit_size, next_cord[1] * unit_size)
