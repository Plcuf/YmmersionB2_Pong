# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player1_position = pygame.Vector2(25,screen.get_height() / 2 - 50)
player2_position = pygame.Vector2(screen.get_width() - 50,screen.get_height() / 2 - 50)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")


    pygame.draw.rect(screen, "white", (player1_position.x, player1_position.y, 25, 100))
    pygame.draw.rect(screen, "white", (player2_position.x, player2_position.y, 25, 100))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_z]:
        print(player1_position.y)
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