from pong import PongGame
import pygame

game = PongGame(1000, 600)
run = True

while run:

    clock = pygame.time.Clock()
    clock.tick(60)

    game.update() # update method call methods like draw and move ball

    keys = pygame.key.get_pressed()

    # Move Player 1
    if keys[pygame.K_d] == True:
        game.move_player_2(1)
    elif keys[pygame.K_a] == True:
        game.move_player_2(-1)
    
    # Move Player 2
    if keys[pygame.K_LEFT] == True:
        game.move_player_1(-1)
    elif keys[pygame.K_RIGHT] == True:
        game.move_player_1(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    

pygame.quit() # Quit Game after While loop