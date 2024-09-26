# Example file showing a circle moving on screen
import pygame
import random
import math

# pygame setup
pygame.mixer.pre_init(44100, -16, 2, 64) #reducing the buffer size apparently reduces sounds delay
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
starting = True
running = False
ending = False
game = True
dt = 0
winner = ""

# KEYS
# player 1
player1_up_key = pygame.K_z
player1_down_key = pygame.K_s
player1_left_key = pygame.K_q
player1_right_key = pygame.K_d
player1_dash_key = pygame.K_f
player1_bump_key = pygame.K_g

# player 2
player2_up_key = pygame.K_o
player2_down_key = pygame.K_l
player2_left_key = pygame.K_k
player2_right_key = pygame.K_m
player2_dash_key = pygame.K_UP
player2_bump_key = pygame.K_RIGHT

# others
start_key = pygame.K_SPACE

trail_size = 10
player_speed = 500

player1_bumping = False
player1_bump_start = 0
player2_bumping = False
player2_bump_start = 0

bump_cooldown = 1 #seconds
bump_timing = 0.5 #seconds

pads_width = 25
pads_height = 100

dash_force = 200
dash_cooldown = 30
player1_dash_used = False
player2_dash_used = False
player1_dash_cooldown = dash_cooldown
player2_dash_cooldown = dash_cooldown

zpressed = False
spressed = False
qpressed = False
dpressed = False

uppressed = False  
downpressed = False
leftpressed = False
rightpressed = False

right_score, left_score = 0, 0

space_enabled = False

player1_position = pygame.Vector2(25,screen.get_height() / 2 - 50)
player2_position = pygame.Vector2(screen.get_width() - 50,screen.get_height() / 2 - 50)

centered_player1_position = pygame.Vector2(player1_position.x + 25, player1_position.y + 50)
centered_player2_position = pygame.Vector2(player2_position.x, player2_position.y + 50)

ball_color = [0,0,0]

ball_color_lowspeed = [229, 255, 0]
ball_color_highspeed = [0, 252, 147]

player1_color = [34, 59, 199]
player2_color = [250, 2, 2]

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

    # draw player 1
    time_since_bump = pygame.time.get_ticks() - player1_bump_start
    color_ratio = min(time_since_bump / 1000, 1)
    current_color = [
        player1_color[i] + color_ratio * (255 - player1_color[i])
        for i in range(3)
    ]
    pygame.draw.rect(screen, current_color, (player1_position.x, player1_position.y, 25, 100))

    # draw player 1 dash cooldown indicator
    dash_color_ratio = player1_dash_cooldown / dash_cooldown
    dash_current_color = [
        player1_color[i] + dash_color_ratio * (255 - player1_color[i])
        for i in range(3)
    ]
    pygame.draw.rect(screen, dash_current_color, (player1_position.x + 5, player1_position.y + 10, 15, 80))


    # draw player 2
    time_since_bump = pygame.time.get_ticks() - player2_bump_start
    color_ratio = min(time_since_bump / 1000, 1)
    current_color = [
        player2_color[i] + color_ratio * (255 - player2_color[i])
        for i in range(3)
    ]
    pygame.draw.rect(screen, current_color, (player2_position.x, player2_position.y, 25, 100))

    # draw player 2 dash cooldown indicator
    dash_color_ratio = player2_dash_cooldown / dash_cooldown
    dash_current_color = [
        player2_color[i] + dash_color_ratio * (255 - player2_color[i])
        for i in range(3)
    ]
    pygame.draw.rect(screen, dash_current_color, (player2_position.x + 5, player2_position.y + 10, 15, 80))

    # draw ball
    pygame.draw.circle(screen, (ball_color[0], ball_color[1], ball_color[2]), (ball_position.x, ball_position.y), 15)
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
bump_fx = pygame.mixer.Sound("./sounds/blast_4.mp3")
goal_fx = pygame.mixer.Sound("./sounds/blast_3.mp3")
dash_fx = pygame.mixer.Sound("./sounds/dash_goofy.mp3")

channel = pygame.mixer.Channel(1)

# ball_direction = pygame.Vector2(1, 0)

ball_positions = [ball_position]
player1_positions = [centered_player1_position]
player2_positions = [centered_player2_position]

while game:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    while starting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starting = False
                game = False

        keys = pygame.key.get_pressed() 
        
        screen.fill("black")

        title_font = pygame.font.Font(None, 135)
        title_surface = title_font.render("ADVANCED PONG", False, "white")
        screen.blit(title_surface, (screen.get_width() / 2 - 400, 10))

        start_font = pygame.font.Font(None, 100)
        start_btn = start_font.render("Start", False, "white")
        screen.blit(start_btn, (screen.get_width() / 2 - start_btn.get_width() / 2, screen.get_height() / 2 - start_btn.get_height() / 2))
        
        if not(keys[start_key]):
            space_enabled = True

        if keys[start_key] and space_enabled:
            starting = False
            running = True
        
        pygame.display.flip()

        dt = clock.tick(60) / 1000

    while running:
        space_enabled = False
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        UpdateScoreText()

        # Interpolate ball color based on ball speed
        speed_ratio = (ball_speed - 500) / 500
        ball_color = [
            ball_color_lowspeed[i] + speed_ratio * (ball_color_highspeed[i] - ball_color_lowspeed[i])
            for i in range(3)
        ]

        # draw circle and trail
        size = 1
        for element in reversed(ball_positions):
            pygame.draw.circle(screen, (ball_color[0], ball_color[1], ball_color[2]), (element[0], element[1]), 15-size)
            size += 1

        # draw player 1 trail
        size = 1
        for element in reversed(player1_positions):
            pygame.draw.rect(screen, (player1_color[0], player1_color[1], player1_color[2]), (element[0] + (size/2), element[1], 25-size, 100))
            size += 1

        # draw player 2 trail
        size = 1
        for element in reversed(player2_positions):
            pygame.draw.rect(screen, (player2_color[0], player2_color[1], player2_color[2]), (element[0] + (size/2), element[1], 25-size, 100))
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
        if (ball_position.x - centered_player1_position.x <= 15 and ball_position.x - centered_player1_position.x >= -40) and (ball_position.y - centered_player1_position.y <= 50 and ball_position.y - centered_player1_position.y >= -50):
            # play the collision sound 
            if player1_bumping:
                bump_fx.play()
                player1_bumping = False
                ball_speed = 1000
            else:
                if not channel.get_busy():
                    channel = touch_fx.play()
            if ball_direction.x < 0:
                ball_direction.x = -ball_direction.x
            ball_direction.y += (ball_position.y - centered_player1_position.y) / 50
            
            if ball_direction.x > 0:
                ball_direction.x = math.ceil(ball_direction.x)
            else:
                ball_direction.x = math.floor(ball_direction.x)
            ball_direction = ball_direction.normalize()

        # bounce the ball on player 2
        if (ball_position.x - centered_player2_position.x >= -15 and ball_position.x - centered_player2_position.x <= 40) and (ball_position.y - centered_player2_position.y <= 50 and ball_position.y - centered_player2_position.y >= -50):
            # play the collision sound 
            if player2_bumping:
                bump_fx.play()
                player2_bumping = False
                ball_speed = 1000
            else:
                if not channel.get_busy():
                    channel = touch_fx.play()
            if ball_direction.x > 0:
                ball_direction.x = -ball_direction.x
            ball_direction.y += (ball_position.y - centered_player2_position.y) / 50
            
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
            if right_score >= 8:
                left_score = 0
                right_score = 0
                running = False
                ending = True
                winner = "red"
            else:
                Goal()
        if ball_position.x >= screen.get_width():
            goal_fx.play()
            ball_position, ball_direction, player1_position, player2_position, ball_speed = Init()
            left_score += 1
            if left_score >= 8:
                left_score = 0
                right_score = 0
                running = False
                ending = True
                winner = "blue"
            else:
                Goal()

        keys = pygame.key.get_pressed()

        # player 1 controls
        if keys[player1_up_key]:
            if player1_position.y > 0:
                if ((abs(player1_position.x - player2_position.x) < pads_width) and (-pads_height <= ((player1_position.y - player_speed * dt) - player2_position.y) <= pads_height)):
                    player1_position.y = player2_position.y + pads_height
                else:
                    player1_position.y -= player_speed * dt

            if keys[player1_dash_key] and player1_dash_used == False:
                zpressed = True

        if keys[player1_down_key]:
            if player1_position.y < screen.get_height() - pads_height:
                if ((abs(player1_position.x - player2_position.x) < pads_width) and (-pads_height <= ((player1_position.y + player_speed * dt) - player2_position.y) <= pads_height)):
                    player1_position.y = player2_position.y - pads_height
                else:
                    player1_position.y += player_speed * dt
            
            if keys[player1_dash_key] and player1_dash_used == False:
                spressed = True

        if keys[player1_left_key]:
            if player1_position.x > (pads_width/2) + 25:
                if ((abs(player1_position.y - player2_position.y) < pads_height) and (-pads_width <= ((player1_position.x - player_speed * dt) - player2_position.x) <= pads_width)):
                    player1_position.x = player2_position.x + pads_width
                else:
                    player1_position.x -= player_speed * dt

            if keys[player1_dash_key] and player1_dash_used == False:
                qpressed = True

        if keys[player1_right_key]:
            if player1_position.x < screen.get_width() - (pads_width/2) - 25:
                if ((abs(player1_position.y - player2_position.y) < 100) and (-25 <= ((player1_position.x + player_speed * dt) - player2_position.x) <= 25)):
                    player1_position.x = player2_position.x - 25
                else:
                    player1_position.x += player_speed * dt

            if keys[player1_dash_key] and player1_dash_used == False:
                dash_fx.play()
                dpressed = True

        if keys[player1_bump_key] and not player1_bumping and (pygame.time.get_ticks() - player1_bump_start) > bump_cooldown * 1000:
            player1_bumping = True
            player1_bump_start = pygame.time.get_ticks()

        # player 2 controls
        if keys[player2_up_key]:
            if player2_position.y > 0:
                if ((abs(player2_position.x - player1_position.x) < pads_width) and (-pads_height <= ((player2_position.y - player_speed * dt) - player1_position.y) <= pads_height)):
                    player2_position.y = player1_position.y + pads_height
                else:
                    player2_position.y -= player_speed * dt
        
            if keys[player2_dash_key] and player2_dash_used == False:
                uppressed = True
            
        if keys[player2_down_key]:
            if player2_position.y < screen.get_height() - pads_height:
                if ((abs(player2_position.x - player1_position.x) < pads_width) and (-pads_height <= ((player2_position.y + player_speed * dt) - player1_position.y) <= pads_height)):
                    player2_position.y = player1_position.y - pads_height
                else:
                    player2_position.y += player_speed * dt

            if keys[player2_dash_key] and player2_dash_used == False:
                downpressed = True

        if keys[player2_left_key]:
            if player2_position.x > (pads_width/2) + 25:
                if ((abs(player2_position.y - player1_position.y) < pads_height) and (-pads_width <= ((player2_position.x - player_speed * dt) - player1_position.x) <= pads_width)):
                    player2_position.x = player1_position.x + pads_width
                else:
                    player2_position.x -= player_speed * dt

            if keys[player2_dash_key] and player2_dash_used == False:
                leftpressed = True
        
        if keys[player2_right_key]:
            if player2_position.x < screen.get_width() - (pads_width/2) - 25:
                if ((abs(player2_position.y - player1_position.y) < pads_height) and (-25 <= ((player2_position.x + player_speed * dt) - player1_position.x) <= 25)):
                    player2_position.x = player1_position.x - 25
                else:
                    player2_position.x += player_speed * dt

            if keys[player2_dash_key] and player2_dash_used == False:
                rightpressed = True

        if keys[player2_bump_key] and not player2_bumping and (pygame.time.get_ticks() - player2_bump_start) > bump_cooldown * 1000:
            player2_bumping = True
            player2_bump_start = pygame.time.get_ticks()

        # bump control
        if player1_bumping:
            if pygame.time.get_ticks() - player1_bump_start >= bump_timing * 1000:
                player1_bumping = False

        if player2_bumping:
            if pygame.time.get_ticks() - player2_bump_start >= bump_timing * 1000:
                player2_bumping = False


        # dash control
        if (zpressed or spressed or qpressed or dpressed) and player1_dash_cooldown == dash_cooldown:
            dash_fx.play()
            player1_dash_used = True
            player1_dash_cooldown = 0

            if zpressed:
                player1_position.y -= dash_force
            if spressed:
                player1_position.y += dash_force
            if qpressed:
                player1_position.x -= dash_force
            if dpressed:
                player1_position.x += dash_force

            previous_x, previous_y = player1_positions[-1][0], player1_positions[-1][1]

            for i in range(5):
                player1_positions.pop(0)
                player1_positions.append([previous_x + (player1_position.x - previous_x) * (i+1)/6, previous_y + (player1_position.y - previous_y) * (i+1)/6])

            zpressed = False
            spressed = False
            qpressed = False
            dpressed = False

        if keys[player1_dash_key] == False:
            player1_dash_used = False

        if (uppressed or downpressed or leftpressed or rightpressed) and player2_dash_cooldown == dash_cooldown:
            dash_fx.play()
            player2_dash_used = True
            player2_dash_cooldown = 0

            if uppressed:
                player2_position.y -= dash_force
            if downpressed:
                player2_position.y += dash_force
            if leftpressed:
                player2_position.x -= dash_force
            if rightpressed:
                player2_position.x += dash_force

            previous_x, previous_y = player2_positions[-1][0], player2_positions[-1][1]

            for i in range(5):
                player2_positions.pop(0)
                player2_positions.append([previous_x + (player2_position.x - previous_x) * (i+1)/6, previous_y + (player2_position.y - previous_y) * (i+1)/6])

            uppressed = False
            downpressed = False
            leftpressed = False
            rightpressed = False

        if keys[player2_dash_key] == False:
            player2_dash_used = False

        if player1_dash_cooldown < dash_cooldown:
            player1_dash_cooldown += 1
        
        if player2_dash_cooldown < dash_cooldown:
            player2_dash_cooldown += 1

        
        if not(player1_position.y > 0):
            player1_position.y = 0
        if not(player1_position.y < screen.get_height() - pads_height):
            player1_position.y = screen.get_height() - pads_height
        if not(player1_position.x > (pads_width/2) + 25):
            player1_position.x = (pads_width/2) + 25
        if not(player1_position.x < screen.get_width() - (pads_width/2) - 25):
            player1_position.x = screen.get_width() - (pads_width/2) - 25

        if not(player2_position.y > 0):
            player2_position.y = 0
        if not(player2_position.y < screen.get_height() - pads_height):
            player2_position.y = screen.get_height() - pads_height
        if not(player2_position.x > (pads_width/2) + 25):
            player2_position.x = (pads_width/2) + 25
        if not(player2_position.x < screen.get_width() - (pads_width/2) - 25):
            player2_position.x = screen.get_width() - (pads_width/2) - 25

        
        if ball_speed > 500:
            ball_speed -= 3


        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    while ending:
        space_enabled = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ending = False
                game = False

        keys = pygame.key.get_pressed()

        screen.fill("black")

        end_font = pygame.font.Font(None, 100)
        end_surface = end_font.render(winner + " player wins", False, "white")
        screen.blit(end_surface, (screen.get_width() / 2 - end_surface.get_width() / 2, 30))

        text = pygame.font.Font(None, 50)
        text_surface = text.render("Back to Menu", False, "white")
        screen.blit(text_surface, (screen.get_width() / 2 - text_surface.get_width() / 2, screen.get_height() / 2 - text_surface.get_height() / 2))

        if keys[start_key]:
            ending = False
            starting = True
            space_enabled = False

        pygame.display.flip()

        dt = clock.tick(60) / 1000

pygame.quit()