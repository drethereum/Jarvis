import pygame
import sys

pygame.init()

screen_width, screen_height = 1440, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Holofy Music Player")

# Load images
background_img = pygame.image.load('holomat/resources/spotify/banner.png')
play_button_img = pygame.image.load('holomat/resources/spotify/play.png')
pause_button_img = pygame.image.load('holomat/resources/spotify/pause.png')
prev_button_img = pygame.image.load('holomat/resources/spotify/previous.png')
skip_button_img = pygame.image.load('holomat/resources/spotify/skip.png')

# Scale images
background = pygame.transform.smoothscale(background_img, (screen_width, screen_height))

button_scale = 0.5
play_button_width, play_button_height = play_button_img.get_size()
play_button = pygame.transform.smoothscale(play_button_img, (int(play_button_width * button_scale), int(play_button_height * button_scale)))
pause_button_width, pause_button_height = pause_button_img.get_size()
pause_button = pygame.transform.smoothscale(pause_button_img, (int(pause_button_width * button_scale), int(pause_button_height * button_scale)))
prev_button_width, prev_button_height = prev_button_img.get_size()
prev_button = pygame.transform.smoothscale(prev_button_img, (int(prev_button_width * button_scale), int(prev_button_height * button_scale)))
skip_button_width, skip_button_height = skip_button_img.get_size()
skip_button = pygame.transform.smoothscale(skip_button_img, (int(skip_button_width * button_scale), int(skip_button_height * button_scale)))

# Position images
background_rect = background.get_rect(center=screen.get_rect().center)

play_button_rect = play_button.get_rect()
pause_button_rect = pause_button.get_rect()
prev_button_rect = prev_button.get_rect()
skip_button_rect = skip_button.get_rect()

total_button_width = (play_button_rect.width + pause_button_rect.width +
               prev_button_rect.width + skip_button_rect.width) + 30  # total spacing between buttons

button_pos_x = (screen_width - total_button_width) // 2
button_pos_y = (screen_height - 400) # number of pixels from the bottom of the screen

button_spacing = 10
prev_button_rect.topleft = (button_pos_x, button_pos_y)
play_button_rect.topleft = (prev_button_rect.topright[0] + button_spacing, button_pos_y)
pause_button_rect.topleft = (play_button_rect.topright[0] + button_spacing, button_pos_y)
skip_button_rect.topleft = (pause_button_rect.topright[0] + button_spacing, button_pos_y)

play_button_pos = play_button_rect.topleft
pause_button_pos = pause_button_rect.topleft
prev_button_pos = prev_button_rect.topleft
skip_button_pos = skip_button_rect.topleft


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("Holofy Application Closed")
            pygame.quit()
            sys.exit()

    screen.blit(background,background_rect)
    screen.blit(play_button,play_button_pos)
    screen.blit(pause_button,pause_button_pos)
    screen.blit(prev_button,prev_button_pos)
    screen.blit(skip_button,skip_button_pos)

    pygame.display.flip()