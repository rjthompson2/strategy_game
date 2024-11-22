import pygame
import pygame_gui
from tile import TileMap
from event import Event
from math import *

MAX_WIDTH = 1280
MAX_HEIGHT = 720

def draw_regular_polygon(surface, color, vertex_count, radius, position, width=0):
    n, r = vertex_count, radius
    x, y = position
    pygame.draw.polygon(surface, color, [
        (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
        for i in range(n)
    ], width)

def draw_event(surface, active_events):
    width = 300
    height = 500

    for event in active_events:
        if event.position[0] < 0:
            event.position[0] = 0
        elif event.position[0] > MAX_WIDTH-width:
            event.position[0] = MAX_WIDTH-width
        x = event.position[0]

        if event.position[1] < 0:
            event.position[1] = 0
        elif event.position[1] > MAX_HEIGHT-height:
            event.position[1] = MAX_HEIGHT-height
        y = event.position[1]

        pygame.draw.rect(surface=surface, color="gray", rect=pygame.Rect((x, y, width, height)))
    return

pygame.init()
screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
clock = pygame.time.Clock()
running = True
moving = False
tile_map = TileMap()
position = [650, 400]
LEFT = 1
RIGHT = 3
zoom = 0
pygame.display.set_caption('Strategy Game')
selected_event = None

#GUI
manager = pygame_gui.UIManager((800, 600))
gui = True
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 80, 100, 50)),
    text='New Game',
    manager=manager,
    anchors={'centerx': 'centerx',
            'centery': 'centery'})

#Events
active_events = []

while running:
    time_delta = clock.tick(60)/1000.0
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #UI Button
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
              if event.ui_element == start_button:  
                tile_map.add_tile()
                gui = False
                active_events.append(Event("Starting Event"))

        #DEV add a new tile on down key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                tile_map.add_tile()

        # Making the screen move
        elif event.type == pygame.MOUSEBUTTONDOWN:
            moving = True
            x, y = pygame.mouse.get_pos() # Get click position
            for current_event in active_events:
                if x >= current_event.position[0]-100 and x <= current_event.position[0]+100 and y >= current_event.position[1]-50 and y <= current_event.position[1]+50: # Check if click is within rectangle
                    selected_event = current_event
            
 
        # Set moving as False if you want 
        # to move the screen only with the 
        # mouse click
        # Set moving as True if you want 
        # to move the screen without the 
        # mouse click
        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False
            selected_event = None
        

        # Make the events move
        # elif event.type == pygame.MOUSEMOTION and moving and event.button == 1:
        #     position = [position[0] + event.rel[0], position[1] + event.rel[1]]

        elif event.type == pygame.MOUSEMOTION and moving:
            if selected_event:
                selected_event.position = [selected_event.position[0] + event.rel[0], selected_event.position[1] + event.rel[1]]
            else:
                position = [position[0] + event.rel[0], position[1] + event.rel[1]]
        
        # Zoom in and out
        # if event.button == 3: 
        #     zoom += 1
        # elif event.button == 4: 
        #     zoom -= 1
        #     print(zoom)

        # Make the background tiles move
            
            
        manager.process_events(event)
        
    
    manager.update(time_delta)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER GAME HERE
    draw_map = tile_map.generate_map()
    for draw_tile in draw_map:
        draw_regular_polygon(screen, draw_tile[0], draw_tile[1], draw_tile[2], [position[0]+draw_tile[3][0], position[1]+draw_tile[3][1]])

    #GUI
    if gui:
        manager.draw_ui(screen)
    if active_events != []:
        draw_event(screen, active_events)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()