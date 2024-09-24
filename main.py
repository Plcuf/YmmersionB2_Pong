# Example file showing a circle moving on screen
import pygame
import random
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player1_position = pygame.Vector2(25,screen.get_height() / 2 - 50)
player2_position = pygame.Vector2(screen.get_width() - 50,screen.get_height() / 2 - 50)

centered_player1_position = pygame.Vector2(player1_position.x + 25, player1_position.y + 50)
centered_player2_position = pygame.Vector2(player2_position.x, player2_position.y + 50)

ball_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
#ball_direction = pygame.Vector2(random.randint(-100, 100), random.randint(-100, 100))
#ball_direction = ball_direction.normalize()
ball_direction = pygame.Vector2(1, 0)
ball_speed = 8

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # draw the shapes :D
    pygame.draw.rect(screen, "white", (player1_position.x, player1_position.y, 25, 100))
    pygame.draw.rect(screen, "white", (player2_position.x, player2_position.y, 25, 100))
    pygame.draw.circle(screen, "white", (ball_position.x, ball_position.y), 15)

    # center the player positions
    centered_player1_position = pygame.Vector2(player1_position.x + 12.5, player1_position.y + 50)
    centered_player2_position = pygame.Vector2(player2_position.x + 12.5, player2_position.y + 50)

    #update ball position
    ball_position += ball_direction * ball_speed

    # bounce the ball on top and bottom side
    if (ball_position.y - 15) <= 0 or (ball_position.y + 15) >= screen.get_height():
        ball_direction.y = -ball_direction.y

    # bounce the ball on player 1
    if ball_position.x - player1_position.x <= 10 and ball_position.y - player1_position.y <= 50:
        ball_direction.x = -ball_direction.x

    # bounce the ball on player 2
    if ball_position.x - player2_position.x >= 0 and ball_position.y - player2_position.y <= 50:
        ball_direction.x = -ball_direction.x

    keys = pygame.key.get_pressed()

    if keys[pygame.K_z]:
        if player1_position.y > 0:
            player1_position.y -= 300 * dt

    if keys[pygame.K_s]:
        if player1_position.y < screen.get_height() - 100:
            player1_position.y += 300 * dt

    if keys[pygame.K_UP]:
        if player2_position.y > 0:
            player2_position.y -= 300 * dt
    
    if keys[pygame.K_DOWN]:
        if player2_position.y < screen.get_height() - 100:
            player2_position.y += 300 * dt


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    


pygame.quit()