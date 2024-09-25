# Imports needed tools
import pygame
import random
import time

# Initialize pygame settings
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

###############################
########## FUNCTIONS ##########
###############################

# Initialize ball position
def BallInit():
    pos = pygame.Vector2(640, 360)
    dir = pygame.Vector2(random.randint(-100, 100), random.randint(-100, 100))
    if dir.x in range(0, 20):
        dir.x = 30
    elif dir.x in range(-20, 0):
        dir.x = -30
    dir = dir.normalize()
    return pos, dir

# Update score text
def UpdateScoreText():
    right_score_text = pygame.font.Font(None, 150)
    right_score_surface = right_score_text.render(str(right_score), False, "white")
    left_score_text = pygame.font.Font(None, 150)
    left_score_surface = left_score_text.render(str(left_score), False, "white")
    screen.blit(right_score_surface, (1210, 10))
    screen.blit(left_score_surface, (10, 10))

# Draw trails
def BallTrail():
    for i in range(len(ball_positions)-1):
        color_decrement = i*5
        color = (135+(color_decrement), 49, 181)
        pygame.draw.circle(screen, color, (ball_positions[-(i+1)][0], ball_positions[i][1]), 15-i)

def DrawPlayer1Trail():
    for i in range(len(player1_positions)):
        color_decrement = i*5
        color = (34, 59-(color_decrement), 199)
        pygame.draw.rect(screen, color, (player1_positions[-(i+1)][0] + (i/2), player1_positions[i][1], pads_width-i, pads_height-i))

def DrawPlayer2Trail():
    for i in range(len(player2_positions)):
        color_increment = i*5
        color = (250, 2, 2+(color_increment))
        pygame.draw.rect(screen, color, (player2_positions[-(i+1)][0] + (i/2), player2_positions[i][1], pads_width-i, pads_height-i))

# Math for trails
def TrailMath(trail_tab, position):
    if len(trail_tab) < length_of_trail:
        trail_tab.append(position)
    else:
        trail_tab.pop(0)
        trail_tab.append(position)

###############################
########## VARIABLES ##########
###############################

# Screen size
screen_height = screen.get_height()
screen_width = screen.get_width()

# Pads size
pads_width = 25
pads_height = 100
players_speed = 500

# Score variables
scored = False
right_score, left_score = 0, 0

# Ball variables
ball_position, ball_direction = BallInit()
ball_speed = 500
ball_size = 15

# Player position (centered)
player1_position = pygame.Vector2(25 + pads_width/2, screen_height / 2)
player2_position = pygame.Vector2(screen_width - (25 + pads_width/2), screen_height / 2)

# Trails initializations
length_of_trail = 10
ball_positions = [ball_position]
player1_positions = [player1_position]
player2_positions = [player2_position]

###############################
########## GAME LOOP ##########
###############################

while running:

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Initialize the screen
    screen.fill("black")
    UpdateScoreText()

    # Score event
    if scored:
        time.sleep(1)
        player1_position = pygame.Vector2(25,screen.get_height() / 2 - 50)
        player2_position = pygame.Vector2(screen.get_width() - 50,screen.get_height() / 2 - 50)
        scored = False

    # Update ball position
    ball_position += ball_direction * (ball_speed * dt)

    # Ball bounces on top and bottom walls
    if (ball_position.y - 15) <= 0 and ball_direction.y < 0:
        ball_direction.y = -ball_direction.y
    if (ball_position.y + 15) >= screen_height and ball_direction.y > 0:
        ball_direction.y = -ball_direction.y

    # Ball bounce on player 1
    if abs(ball_position.x - player1_position.x) < (ball_size + pads_width/2) and abs(ball_position.y - player1_position.y) < (ball_size + pads_height/2):
        ball_direction.x = -ball_direction.x
    if abs(ball_position.x - player1_position.x) < pads_width and abs(ball_position.y - player1_position.y) < (ball_size + pads_height/2):
        ball_direction.y = -ball_direction.y
        ball_direction.x = -ball_direction.x

    # Ball bounces on player 2
    if abs(ball_position.x - player2_position.x) < (ball_size + pads_width/2) and abs(ball_position.y - player2_position.y) < (ball_size + pads_height/2):
        ball_direction.x = -ball_direction.x
    if abs(ball_position.x - player2_position.x) < pads_width and abs(ball_position.y - player2_position.y) < (ball_size + pads_height/2):
        ball_direction.y = -ball_direction.y
        ball_direction.x = -ball_direction.x

    # Update score
    if ball_position.x <= 0:
        right_score += 1
        scored = True
    if ball_position.x >= screen.get_width():
        left_score += 1
        scored = True
    if scored:
        ball_position, ball_direction = BallInit()

    # Input controls
    keys = pygame.key.get_pressed()

    # player 1 controls
    if keys[pygame.K_z]:
        if player1_position.y > (pads_height/2):
            if ((abs(player1_position.x - player2_position.x) < pads_width) and (-pads_height <= ((player1_position.y - players_speed * dt) - player2_position.y) <= pads_height)):
                player1_position.y = player2_position.y + pads_height
            else:
                player1_position.y -= players_speed * dt
            

    if keys[pygame.K_s]:
        if player1_position.y < screen.get_height() - (pads_height/2):
            if ((abs(player1_position.x - player2_position.x) < pads_width) and (-pads_height <= ((player1_position.y + players_speed * dt) - player2_position.y) <= pads_height)):
                player1_position.y = player2_position.y - pads_height
            else:
                player1_position.y += players_speed * dt

    if keys[pygame.K_q]:
        if player1_position.x > (pads_width/2) + 25:
            if ((abs(player1_position.y - player2_position.y) < pads_height) and (-pads_width <= ((player1_position.x - players_speed * dt) - player2_position.x) <= pads_width)):
                player1_position.x = player2_position.x + pads_width
            else:
                player1_position.x -= players_speed * dt

    if keys[pygame.K_d]:
        if player1_position.x < screen.get_width() - (pads_width/2) - 250:
            if ((abs(player1_position.y - player2_position.y) < 100) and (-25 <= ((player1_position.x + players_speed * dt) - player2_position.x) <= 25)):
                player1_position.x = player2_position.x - 25
            else:
                player1_position.x += players_speed * dt

    # player 2 controls
    if keys[pygame.K_UP]:
        if player2_position.y > (pads_height/2):
            if ((abs(player2_position.x - player1_position.x) < pads_width) and (-pads_height <= ((player2_position.y - players_speed * dt) - player1_position.y) <= pads_height)):
                player2_position.y = player1_position.y + pads_height
            else:
                player2_position.y -= players_speed * dt
        
    if keys[pygame.K_DOWN]:
        if player2_position.y < screen.get_height() - (pads_height/2):
            if ((abs(player2_position.x - player1_position.x) < pads_width) and (-pads_height <= ((player2_position.y + players_speed * dt) - player1_position.y) <= pads_height)):
                player2_position.y = player1_position.y - pads_height
            else:
                player2_position.y += players_speed * dt

    if keys[pygame.K_LEFT]:
        if player2_position.x > (pads_width/2) + 250:
            if ((abs(player2_position.y - player1_position.y) < pads_height) and (-pads_width <= ((player2_position.x - players_speed * dt) - player1_position.x) <= pads_width)):
                player2_position.x = player1_position.x + pads_width
            else:
                player2_position.x -= players_speed * dt
    
    if keys[pygame.K_RIGHT]:
        if player2_position.x < screen.get_width() - (pads_width/2) - 25:
            if ((abs(player2_position.y - player1_position.y) < pads_height) and (-25 <= ((player2_position.x + players_speed * dt) - player1_position.x) <= 25)):
                player2_position.x = player1_position.x - 25
            else:
                player2_position.x += players_speed * dt

    # Math for trails
    TrailMath(ball_positions, ball_position)
    TrailMath(player1_positions, player1_position)
    TrailMath(player2_positions, player2_position)

    # Draw the trails
    BallTrail()
    DrawPlayer1Trail()
    DrawPlayer2Trail()
    
    # Draw the pads
    pygame.draw.rect(screen, "white", (player1_position.x - (pads_width/2), player1_position.y - (pads_height/2), pads_width, pads_height))
    pygame.draw.rect(screen, "white", (player2_position.x - (pads_width/2), player2_position.y - (pads_height/2), pads_width, pads_height))
    
    # Draw the ball
    pygame.draw.circle(screen, "purple", (ball_position.x, ball_position.y), 15)
    pygame.draw.circle(screen, "white", (ball_position.x, ball_position.y), 10)

    
    
    # Update the screen
    pygame.display.flip()

    # Update the clock
    dt = clock.tick(60) / 1000

pygame.quit()