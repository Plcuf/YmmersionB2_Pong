# Example file showing a circle moving on screen
import pygame
import random
import time
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

trail_size = 10
player_speed = 300

right_score, left_score = 0, 0

player1_position = pygame.Vector2(25,screen.get_height() / 2 - 50)
player2_position = pygame.Vector2(screen.get_width() - 50,screen.get_height() / 2 - 50)

centered_player1_position = pygame.Vector2(player1_position.x + 25, player1_position.y + 50)
centered_player2_position = pygame.Vector2(player2_position.x, player2_position.y + 50)

def BallInit():
    pos = pygame.Vector2(640, 360)
    dir = pygame.Vector2(random.randint(-100, 100), random.randint(-100, 100))
    if dir.x in range(0, 20):
        dir.x = 30
    elif dir.x in range(-20, 0):
        dir.x = -30
    dir = dir.normalize()
    return pos, dir

def UpdateScoreText():
    right_score_text = pygame.font.Font(None, 150)
    right_score_surface = right_score_text.render(str(right_score), False, "white")
    left_score_text = pygame.font.Font(None, 150)
    left_score_surface = left_score_text.render(str(left_score), False, "white")
    screen.blit(right_score_surface, (1210, 10))
    screen.blit(left_score_surface, (10, 10))

ball_position, ball_direction = BallInit()
# ball_direction = pygame.Vector2(1, 0)
ball_speed = 7

ball_positions = [ball_position]
player1_positions = [centered_player1_position]
player2_positions = [centered_player2_position]

scored = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    UpdateScoreText()

    # draw circle and trail
    size = 1
    for element in reversed(ball_positions):
        pygame.draw.circle(screen, ((135+(size*5)), 49, 181), (element[0], element[1]), 15-size)
        size += 1

    # draw player 1 trail
    size = 1
    for element in reversed(player1_positions):
        pygame.draw.rect(screen, (34, 59-(size*5), 199), (element[0] + (size/2), element[1], 25-size, 100))
        size += 1

    # draw player 2 trail
    size = 1
    for element in reversed(player2_positions):
        pygame.draw.rect(screen, (250, 2, 2+(size*5)), (element[0] + (size/2), element[1], 25-size, 100))
        size += 1

    # draw the pads
    pygame.draw.rect(screen, "white", (player1_position.x, player1_position.y, 25, 100))
    pygame.draw.rect(screen, "white", (player2_position.x, player2_position.y, 25, 100))
    pygame.draw.circle(screen, "white", (ball_position.x, ball_position.y), 15)

    if scored:
        time.sleep(1)
        player1_position = pygame.Vector2(25,screen.get_height() / 2 - 50)
        player2_position = pygame.Vector2(screen.get_width() - 50,screen.get_height() / 2 - 50)
        scored = False

    # math the ball trail
    if len(ball_positions) > trail_size:
        ball_positions.pop(0)
        ball_positions.append([ball_position.x, ball_position.y])
    else:
        ball_positions.append([ball_position.x, ball_position.y])

    # math the player 1 trail
    if len(player1_positions) > trail_size:
        player1_positions.pop(0)
        player1_positions.append([player1_position.x, player1_position.y])
    else:
        player1_positions.append([player1_position.x, player1_position.y])
    
    # math the player 2 trail
    if len(player2_positions) > trail_size:
        player2_positions.pop(0)
        player2_positions.append([player2_position.x, player2_position.y])
    else:
        player2_positions.append([player2_position.x, player2_position.y])

    # center the player positions
    centered_player1_position = pygame.Vector2(player1_position.x + 25, player1_position.y + 50)
    centered_player2_position = pygame.Vector2(player2_position.x, player2_position.y + 50)

    #update ball position
    ball_position += ball_direction * ball_speed

    # bounce the ball on top and bottom side
    if (ball_position.y - 15) <= 0 and ball_direction.y < 0:
        ball_direction.y = -ball_direction.y
    if (ball_position.y + 15) >= screen.get_height() and ball_direction.y > 0:
        ball_direction.y = -ball_direction.y

    # bounce the ball on player 1
    if ball_position.x - centered_player1_position.x <= 15 and (ball_position.y - centered_player1_position.y <= 50 and ball_position.y - centered_player1_position.y >= -50):
        if ball_direction.x < 0:
            ball_direction.x = -ball_direction.x
        ball_direction.y += (ball_position.y - centered_player1_position.y) / 50
        if ball_direction.y > 2:
            ball_direction.y = 2
        if ball_direction.y < -2:
            ball_direction.y = -2
        
        if ball_direction.x > 0:
            ball_direction.x = math.ceil(ball_direction.x)
        else:
            ball_direction.x = math.floor(ball_direction.x)
        ball_direction = ball_direction.normalize()


    # bounce the ball on player 2
    if ball_position.x - centered_player2_position.x >= -15 and (ball_position.y - centered_player2_position.y <= 50 and ball_position.y - centered_player2_position.y >= -50):
        if ball_direction.x > 0:
            ball_direction.x = -ball_direction.x
        ball_direction.y += (ball_position.y - centered_player2_position.y) / 50
        if ball_direction.y > 2:
            ball_direction.y = 2
        if ball_direction.y < -2:
            ball_direction.y = -2
        
        if ball_direction.x > 0:
            ball_direction.x = math.ceil(ball_direction.x)
        else:
            ball_direction.x = math.floor(ball_direction.x)
        ball_direction = ball_direction.normalize()

    # check if point marked and updates score
    if ball_position.x <= 0:
        right_score += 1
        scored = True
    if ball_position.x >= screen.get_width():
        left_score += 1
        scored = True

    if scored:
        ball_position, ball_direction = BallInit()

    keys = pygame.key.get_pressed()

    # player 1 controls
    if keys[pygame.K_z]:
        if player1_position.y > 0:
            player1_position.y -= player_speed * dt

    if keys[pygame.K_s]:
        if player1_position.y < screen.get_height() - 100:
            player1_position.y += player_speed * dt

    if keys[pygame.K_q]:
        if player1_position.x > 25:
            player1_position.x -= player_speed * dt

    if keys[pygame.K_d]:
        if player1_position.x < screen.get_width() - 50:
            player1_position.x += player_speed * dt

    # player 2 controls
    if keys[pygame.K_UP]:
        if player2_position.y > 0:
            player2_position.y -= player_speed * dt
    
    if keys[pygame.K_DOWN]:
        if player2_position.y < screen.get_height() - 100:
            player2_position.y += player_speed * dt

    if keys[pygame.K_LEFT]:
        if player2_position.x > 25:
            player2_position.x -= player_speed * dt
    
    if keys[pygame.K_RIGHT]:
        if player2_position.x < screen.get_width() - 50:
            player2_position.x += player_speed * dt


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()