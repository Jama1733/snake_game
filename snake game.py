import pygame

# pygame setup
pygame.init()
screen_width, screen_height = 1280,720
FPS = 60
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# set up grid and background display values
grid_line_width = 3
grid_box_size = 10
grid_unit = grid_line_width + grid_box_size

grid_line_color = 'blue'
background_color = 'black'

# set up values for snake segments
height = grid_box_size
width = grid_box_size
x, y = grid_line_width, grid_line_width
speed = grid_unit
direction = 'r'

# counter for snake speed. wait is how many fames to wait to move
# wait/FPS is grid units per second
counter = 0
wait = 5


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for keypress
        if event.type == pygame.KEYDOWN:
            match event.key:
                # WASD checking and direction updating
                case 119: direction = 'u'
                case 97: direction = 'l'
                case 115: direction = 'd'
                case 100: direction = 'r'


    # fill the screen with a color to wipe away anything from last frame
    screen.fill(background_color)

    
    # draw grid for snake
    for x_coordinate in range(0,screen_width,grid_unit):
        r = pygame.Rect(x_coordinate, 0, grid_line_width, screen_height)
        pygame.draw.rect(screen,grid_line_color, r)
    for y_coordinate in range(0,screen_height,grid_unit):
        r = pygame.Rect(0, y_coordinate, screen_width, grid_line_width)
        pygame.draw.rect(screen,grid_line_color, r)
    
        
    # change direction every wait frames
    if counter % wait == 0:
        if direction =='r': x+=speed
        if direction == 'l': x-=speed
        if direction == 'u': y-=speed
        if direction == 'd': y+=speed
    counter += 1

    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen,'red',rect)



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    clock.tick(FPS)

pygame.quit()