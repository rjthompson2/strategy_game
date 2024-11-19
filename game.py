import pygame
from tile import TileMap
from math import *

def draw_regular_polygon(surface, color, vertex_count, radius, position, width=0):
    n, r = vertex_count, radius
    x, y = position
    pygame.draw.polygon(surface, color, [
        (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
        for i in range(n)
    ], width)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
moving = False
tile_map = TileMap()
tile_map.add_tile()
position = [500, 500]
LEFT = 1
RIGHT = 3
pygame.display.set_caption('Strategy Game')

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                tile_map.add_tile()

        # Making the screen move
        elif event.type == pygame.MOUSEBUTTONDOWN:
            moving = True
 
        # Set moving as False if you want 
        # to move the screen only with the 
        # mouse click
        # Set moving as True if you want 
        # to move the screen without the 
        # mouse click
        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False

        # Make your image move continuously
        elif event.type == pygame.MOUSEMOTION and moving:
            position = [position[0] + event.rel[0], position[1] + event.rel[1]]
        
        

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    draw_map = tile_map.generate_map()
    for draw_tile in draw_map:
        draw_regular_polygon(screen, draw_tile[0], draw_tile[1], draw_tile[2], [position[0]+draw_tile[3][0], position[1]+draw_tile[3][1]])

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()