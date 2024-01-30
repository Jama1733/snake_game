import pygame
from random import randrange as rand

# pygame setup
pygame.init()
screen_width, screen_height = 1280,720
FPS = 60
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# set up grid and background display values
grid_line_width = 4
grid_box_size = 18
grid_unit = grid_line_width + grid_box_size

# color values
grid_line_color = 'blue'
background_color = 'black'
snake_color = 'red'
rat_color = 'gray'

# set up values for snake segments
x_pos, y_pos = grid_line_width, grid_line_width
direction = 'r'
speed = grid_unit

# set up snake
head = pygame.Rect(x_pos, y_pos, grid_box_size, grid_box_size)
snake = [head]

# set up first rat
x = rand(0, screen_width, grid_unit) + grid_line_width
y = rand(0, screen_height, grid_unit) + grid_line_width
rat_size = grid_box_size
# rat buffer to prevent rat from spawning near the edges
rat_buffer = grid_unit *2
rat = pygame.Rect(x, y, rat_size, rat_size)
rat_exists = True

# counter for snake speed. wait is how many fames to wait to move
# wait/FPS is grid units per second
counter = 0
wait = 6


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
                case 119:
                    if direction != 'd': direction = 'u'
                case 97:
                    if direction != 'r': direction = 'l'
                case 115:
                    if direction != 'u': direction = 'd'
                case 100:
                    if direction != 'l': direction = 'r'


    # fill the screen with a color to wipe away anything from last frame
    screen.fill(background_color)

    
    # draw grid for snake
    for x_coordinate in range(0,screen_width,grid_unit):
        r = pygame.Rect(x_coordinate, 0, grid_line_width, screen_height)
        pygame.draw.rect(screen,grid_line_color, r)
    for y_coordinate in range(0,screen_height,grid_unit):
        r = pygame.Rect(0, y_coordinate, screen_width, grid_line_width)
        pygame.draw.rect(screen,grid_line_color, r)
    

    # generate and draw rat if it doesn't exist
    # if it does just draw it
    if not rat_exists:
        x = rand(rat_buffer, screen_width - rat_buffer, grid_unit) + grid_line_width
        y = rand(rat_buffer, screen_height - rat_buffer, grid_unit) + grid_line_width 
        rat = pygame.Rect(x, y, rat_size, rat_size)
        pygame.draw.rect(screen, rat_color, rat)
        rat_exists = True
    if rat_exists:
        pygame.draw.rect(screen, rat_color, rat)
        

    # change direction and adjust snake location every wait frames
    if counter % wait == 0:
        if direction =='r': x_pos += speed
        if direction == 'l': x_pos -= speed
        if direction == 'u': y_pos -= speed
        if direction == 'd': y_pos += speed
        # look at 'previous' segment's position and move there where previous is new position for the head for the first loop
        previous_x = x_pos
        previous_y = y_pos
        for segment in snake:
            # store current segment's spot
            temp_x = segment.x
            temp_y = segment.y
            # adjust segment to new value
            segment.x = previous_x
            segment.y = previous_y
            # send old value to the next segment
            previous_x = temp_x
            previous_y = temp_y
    # draw the snake every frame
    for segment in snake:
        pygame.draw.rect(screen, snake_color, segment)
    counter += 1


    # if the snake is on a rat then add a new segment
    if x_pos == rat.x and y_pos == rat.y and counter % wait == 0:
        x_diff = y_diff = 0
        tail_x = snake[-1].x
        tail_y = snake[-1].y
        # if the snake is just the head then the differences are set based on direction
        if len(snake) == 1:
            match direction:
                case 'u': y_diff = -grid_unit
                case 'l': x_diff = -grid_unit
                case 'd': y_diff = grid_unit
                case 'r': x_diff = grid_unit
        # if not then direction is found by looking at the difference between the tail and next one
        else:
            # tail in the last segment and next is the second to last segment
            next_x = snake[-2].x
            next_y = snake[-2].y
            # so if the next segment is to the right of or below the tail then the difference will be positive
            x_diff = next_x - tail_x
            y_diff = next_y - tail_y
        # if there's a difference in x then the tail will be placed horizontal to the tail and that difference will be subtracted(should be the same as grid_unit)
        if x_diff != 0:
            caboose = pygame.Rect(tail_x - x_diff, tail_y, grid_box_size, grid_box_size)
        if y_diff != 0:
            caboose = pygame.Rect(tail_x, tail_y - y_diff, grid_box_size, grid_box_size)
        # add new tail to end of snake
        snake.append(caboose)
        # set condition to make new rat
        rat_exists = False


    # if the snake touches the edge then restart
    if x_pos < 0 or y_pos < 0 or x_pos > screen_width or y_pos > screen_height:
        snake = [snake[0]]
        x_pos, y_pos = grid_line_width, grid_line_width
        direction = 'r'
        rat_exists = False
    
    # if the snake touches itself then restart
    # it can't do that if it's smaller than 5 segments
    if len(snake)> 4:
        # go backwards through segments and check if they're in the same spot as the head
        for segment in snake[-1:-(len(snake)-1):-1]:
            seg_x = segment.x
            seg_y = segment.y
            if seg_x == x_pos and seg_y == y_pos:
                snake = [snake[0]]
                x_pos, y_pos = grid_line_width, grid_line_width
                direction = 'r'
                rat_exists = False
                break


    # flip() the display to put your work on screen
    pygame.display.flip()


    # limits FPS
    clock.tick(FPS)

pygame.quit()

