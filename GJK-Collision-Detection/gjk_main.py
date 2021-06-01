import os
import pygame
from gjk import intersect

def main():
    #initialize colours
    BACKGROUND = (175, 175, 225)
    POLYGON = (225, 225, 225)
    RED = (200, 75, 75)
    GREEN = (75, 200, 75)

    #initialize the fixed polygon
    polygon1 = [[300, 500], [500, 300], [240, 240]]

    #initialize pygame display
    DISPLAY_WIDTH = 1000
    DISPLAY_HEIGHT = 600
    DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("GJK Collision Detection")


    #run the visualizer 
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        
        #fill display
        pygame.time.delay(10)
        pygame.display.flip()
        DISPLAY.fill(BACKGROUND)

        #draw the fixed polygon
        pygame.draw.polygon(DISPLAY, POLYGON, polygon1)

        #get the position of polygon2
        position = pygame.mouse.get_pos()
        polygon2 = [[50+position[0], 50+position[1]], \
            [50+position[0], -15+position[1]], \
                [position[0], -50+position[1]], \
                    [-60+position[0], position[1]]]

        #run the GJK algorithm
        collision = intersect(polygon1, polygon2)

        #draw polygon2
        pygame.draw.polygon(DISPLAY, RED if collision else GREEN, polygon2)


    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
