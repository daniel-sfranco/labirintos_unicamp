import pygame
from drawer import *
from player import *

pygame.init()
speed = [1 , 1]
game_part = 'init'
move_keys = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_a, pygame.K_s, pygame.K_w, pygame.K_d]
player, playerrect = create_player()
button_positions = []
mouse_x, mouse_y = 0, 0
pressed = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pressed = True
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    if game_part == 'init':
        button_positions = draw_init()
        buttons = ['new', 'saved', 'winners', 'info', 'quit']
        if pressed:
            for i in range(len(button_positions)):
                if mouse_x >= button_positions[i][0] and mouse_x <= button_positions[i][1] and mouse_y >= button_positions[i][2] and mouse_y <=  button_positions[i][3]:
                    game_part = buttons[i]
                    break
        if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
            game_part = 'new'
    elif game_part == 'new':
        for key in move_keys:
            if keys[key]:
                playerrect = move_player(key, playerrect)
        draw_player(player, playerrect)
    elif game_part == 'quit':
        pygame.quit()
        sys.exit()
