import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

background = 'purple'
height = 15
width = 15
x, y = 0,0
speed = 3
right=left=up=down=grow=shrink = False
direction = 'r'

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
        #Check for keypress
        if event.type == pygame.KEYDOWN:
            print(event.key)
            match event.key:
                #WASD checking and direction updating
                case 119: direction = 'u'
                case 97: direction = 'l'
                case 115: direction = 'd'
                case 100: direction = 'r'


    # fill the screen with a color to wipe away anything from last frame
    screen.fill(background)

    # RENDER YOUR GAME HERE
    if direction =='r': x+=speed
    if direction == 'l': x-=speed
    if direction == 'u': y-=speed
    if direction == 'd': y+=speed

    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen,'red',rect)



    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    clock.tick(60)

pygame.quit()