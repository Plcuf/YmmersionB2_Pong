# Example file showing a circle moving on screen
import pygame
import random
import math

# pygame setup
pygame.mixer.pre_init(44100, -16, 2, 64) #reducing the buffer size apparently reduces sounds delay
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

trail_size = 10
player_speed = 500

player1_bumping = False
player1_bump_start = 0
player2_bumping = False
player2_bump_start = 0

pads_width = 25
pads_height = 100

right_score, left_score = 0, 0

player1_position = pygame.Vector2(25,screen.get_height() / 2 - 50)
player2_position = pygame.Vector2(screen.get_width() - 50,screen.get_height() / 2 - 50)

centered_player1_position = pygame.Vector2(player1_position.x + 25, player1_position.y + 50)
centered_player2_position = pygame.Vector2(player2_position.x, player2_position.y + 50)

player1_size = 1
player2_size = 1


def Init():
    player1_position = pygame.Vector2(25,screen.get_height() / 2 - 50)
    player2_position = pygame.Vector2(screen.get_width() - 50,screen.get_height() / 2 - 50)
    ball_position = pygame.Vector2(640, 360)
    ball_direction = pygame.Vector2(random.randint(-100, 100), random.randint(-100, 100))
    if ball_direction.x in range(0, 20):
        ball_direction.x = 30
    elif ball_direction.x in range(-20, 0):
        ball_direction.x = -30
    ball_direction = ball_direction.normalize()
    return ball_position, ball_direction, player1_position, player2_position, 500

ball_position, ball_direction, player1_position, player2_position, ball_speed = Init()

def UpdateScoreText():
    right_score_text = pygame.font.Font(None, 150)
    right_score_surface = right_score_text.render(str(right_score), False, "white")
    left_score_text = pygame.font.Font(None, 150)
    left_score_surface = left_score_text.render(str(left_score), False, "white")
    screen.blit(right_score_surface, (1210, 10))
    screen.blit(left_score_surface, (10, 10))

def Draw():
    UpdateScoreText()
    pygame.draw.rect(screen, "white", (player1_position.x, player1_position.y, 25, 100))
    pygame.draw.rect(screen, "white", (player2_position.x, player2_position.y, 25, 100))
    pygame.draw.circle(screen, "purple", (ball_position.x, ball_position.y), 15)
    pygame.draw.circle(screen, "white", (ball_position.x, ball_position.y), 10)

async def Goal():
    timer_text = pygame.font.Font(None, 500)
    Draw()
    for i in range(3):
        timer_surface = timer_text.render(str(i), False, "white")
        await screen.blit(timer_surface, (screen.get_width() / 2 - 250, screen.get_height() / 2 - 250))
        pygame.display.flip()
        pygame.time.wait(1000)


touch_fx = pygame.mixer.Sound("./sounds/touched.mp3")
touch_fx.set_volume(0.7)
goal_fx = pygame.mixer.Sound("./sounds/blast_3.mp3")


# ball_direction = pygame.Vector2(1, 0)

ball_positions = [ball_position]
player1_positions = [centered_player1_position]
player2_positions = [centered_player2_position]

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
    Draw()

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
    ball_position += ball_direction * (ball_speed * dt)

    # bounce the ball on top and bottom side
    if (ball_position.y - 15) <= 0 and ball_direction.y < 0:
        ball_direction.y = -ball_direction.y
    if (ball_position.y + 15) >= screen.get_height() and ball_direction.y > 0:
        ball_direction.y = -ball_direction.y

    # bounce the ball on player 1
    if (ball_position.x - centered_player1_position.x <= 15 * player1_size and ball_position.x - centered_player1_position.x >= -40 * player1_size) and (ball_position.y - centered_player1_position.y <= 50 * player1_size and ball_position.y - centered_player1_position.y >= -50 * player1_size):
        # play the collision sound 
        touch_fx.play()
        if player1_bumping:
            player1_bumping = False
            player1_size = 1
            ball_speed = 1000
        else:
            ball_speed = 500
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
    if (ball_position.x - centered_player2_position.x >= -15 * player2_size and ball_position.x - centered_player2_position.x <= 40 * player2_size) and (ball_position.y - centered_player2_position.y <= 50 * player2_size and ball_position.y - centered_player2_position.y >= -50 * player2_size):
        # play the collision sound 
        touch_fx.play()
        if player2_bumping:
            player2_bumping = False
            player2_size = 1
            ball_speed = 1000
        else:
            ball_speed = 500
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
        goal_fx.play()
        ball_position, ball_direction, player1_position, player2_position, ball_speed = Init()
        right_score += 1
        Goal()
    if ball_position.x >= screen.get_width():
        goal_fx.play()
        ball_position, ball_direction, player1_position, player2_position, ball_speed = Init()
        left_score += 1
        Goal()

    keys = pygame.key.get_pressed()

    # player 1 controls
    if keys[pygame.K_z]:
        if player1_position.y > (pads_height/2):
            if ((abs(player1_position.x - player2_position.x) < pads_width) and (-pads_height <= ((player1_position.y - player_speed * dt) - player2_position.y) <= pads_height)):
                player1_position.y = player2_position.y + pads_height
                player1_position.y += 50
            else:
                player1_position.y -= player_speed * dt
            

    if keys[pygame.K_s]:
        if player1_position.y < screen.get_height() - (pads_height/2):
            if ((abs(player1_position.x - player2_position.x) < pads_width) and (-pads_height <= ((player1_position.y + player_speed * dt) - player2_position.y) <= pads_height)):
                player1_position.y = player2_position.y - pads_height
                player1_position.y -= 50
            else:
                player1_position.y += player_speed * dt

    if keys[pygame.K_q]:
        if player1_position.x > (pads_width/2) + 25:
            if ((abs(player1_position.y - player2_position.y) < pads_height) and (-pads_width <= ((player1_position.x - player_speed * dt) - player2_position.x) <= pads_width)):
                player1_position.x = player2_position.x + pads_width
                player1_position.x += 50
            else:
                player1_position.x -= player_speed * dt

    if keys[pygame.K_d]:
        if player1_position.x < screen.get_width() - (pads_width/2) - 250:
            if ((abs(player1_position.y - player2_position.y) < 100) and (-25 <= ((player1_position.x + player_speed * dt) - player2_position.x) <= 25)):
                player1_position.x = player2_position.x - pads_width
                player1_position.x -= 50
            else:
                player1_position.x += player_speed * dt
    
    if keys[pygame.K_e] and not player1_bumping and (pygame.time.get_ticks() - player1_bump_start) > 1000:
        player1_bumping = True
        player1_bump_start = pygame.time.get_ticks()


    # player 2 controls
    if keys[pygame.K_UP]:
        if player2_position.y > (pads_height/2):
            if ((abs(player2_position.x - player1_position.x) < pads_width) and (-pads_height <= ((player2_position.y - player_speed * dt) - player1_position.y) <= pads_height)):
                player2_position.y = player1_position.y + pads_height
                player2_position.y += 50
            else:
                player2_position.y -= player_speed * dt
        
    if keys[pygame.K_DOWN]:
        if player2_position.y < screen.get_height() - (pads_height/2):
            if ((abs(player2_position.x - player1_position.x) < pads_width) and (-pads_height <= ((player2_position.y + player_speed * dt) - player1_position.y) <= pads_height)):
                player2_position.y = player1_position.y - pads_height
                player2_position.y -= 50
            else:
                player2_position.y += player_speed * dt

    if keys[pygame.K_LEFT]:
        if player2_position.x > (pads_width/2) + 250:
            if ((abs(player2_position.y - player1_position.y) < pads_height) and (-pads_width <= ((player2_position.x - player_speed * dt) - player1_position.x) <= pads_width)):
                player2_position.x = player1_position.x + pads_width
                player2_position.x += 50
            else:
                player2_position.x -= player_speed * dt
    
    if keys[pygame.K_RIGHT]:
        if player2_position.x < screen.get_width() - (pads_width/2) - 25:
            if ((abs(player2_position.y - player1_position.y) < pads_height) and (-25 <= ((player2_position.x + player_speed * dt) - player1_position.x) <= 25)):
                player2_position.x = player1_position.x - pads_width
                player2_position.x -= 50
            else:
                player2_position.x += player_speed * dt

    if keys[pygame.K_KP0] and not player2_bumping and (pygame.time.get_ticks() - player2_bump_start) > 1000:
        player2_bumping = True
        player2_bump_start = pygame.time.get_ticks()

    # bump control
    if player1_bumping:
        player1_size = 1.2
        if pygame.time.get_ticks() - player1_bump_start >= 500:
            player1_bumping = False
            player1_size = 1

    if player2_bumping:
        player2_size = 1.2
        if pygame.time.get_ticks() - player2_bump_start >= 500:
            player2_bumping = False
            player2_size = 1

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()