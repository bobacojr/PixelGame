import pygame
from sys import exit

#start pygame
pygame.init()
#create the screen
screen = pygame.display.set_mode((1200, 800))
#set the title
pygame.display.set_caption('Andrea the Cat')
#make variable for fps
clock = pygame.time.Clock()

#surface with color
color_surface = pygame.Surface((400, 500))
#add color to surface
color_surface.fill('Blue')

while True:
    #quits the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #place the colored surface ( (0,0) starts at top left)
    screen.blit(color_surface, (200, 100))

    #updates the screen
    pygame.display.update()
    #sets the fps
    clock.tick(60)
