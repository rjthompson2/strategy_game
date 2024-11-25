import pygame
import pygame_gui
from tiles.tile import TileMap
from events.event import Event
from chain import EventOptionChain
from units import Units
from math import *

MAX_WIDTH = 1280
MAX_HEIGHT = 720
LEFT = 1
RIGHT = 3


pygame.init()
pygame.display.set_caption('Strategy Game')
screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((MAX_WIDTH, MAX_HEIGHT))

running = True
moving = False
tile_map = TileMap()
units = Units()
position = [650, 400]
zoom = 0
selected_event = None
chain = EventOptionChain()

#Font
pygame.font.init()
title_font = pygame.font.SysFont('timesnewroman', 30)
my_font = pygame.font.SysFont('timesnewroman', 15)

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
        #check borders
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

        #create event window
        pygame.draw.rect(surface=surface, color="gray", rect=pygame.Rect((x, y, width, height)))
        #create exit button
        pygame.draw.rect(surface=surface, color="dark gray", rect=pygame.Rect((x+5, y+5, 10, 10)))
        
        # create a text surface object, on which text is drawn on it.
        title_text = title_font.render(event.title, False, (0, 0, 0))

        # text wrapping for descriptions
        descriptions = event.description.split(" ")
        description_text_list = []
        description = ""
        i = 0
        while i < len(descriptions):
            if len(description + descriptions[i]) < 41:
                description += " " + descriptions[i]
                i += 1
            else:
                description_text_list.append(my_font.render(description, False, (0, 0, 0)))
                description = ""
        if description != "":
            description_text_list.append(my_font.render(description, False, (0, 0, 0)))


        surface.blit(title_text, (x+10, y+20))
        i = 50
        for description_text in description_text_list:
            surface.blit(description_text, (x+10, y+i))
            i += 15
        i += 15
        
        for option in event.options:
            option_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x+10, y+i, width-20, 50)),
                text=option,
                manager=manager)
            i += 55
            chain.add_pair_options(option, option_button)
        chain.add_pair_event(event)
    return

def draw_unit(surface, unit):
    pygame.draw.circle(surface, (80, 80, 80), [position[0]+unit.current_tile.position[0], position[1]+unit.current_tile.position[1]], 20)

#GUI
gui = True
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0, 100, 50)),
    text='New Game',
    manager=manager,
    anchors={'centerx': 'centerx',
            'centery': 'centery'})

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
                manager.clear_and_reset()
                chain.add_event(Event("Starting Event"))
            elif event.ui_element in chain.button_option.keys():
                #TODO remove the event from the screen
                #clear all options in that event from the list
                #activate the option
                option = chain.button_option[event.ui_element]
                chain.remove_and_choose_option(option, tile_map)
                manager.clear_and_reset()

        #DEV add a new tile on down key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                tile_map.add_tile()

        # Making the screen move
        elif event.type == pygame.MOUSEBUTTONDOWN:
            moving = True
            x, y = pygame.mouse.get_pos() # Get click position
            for current_event in chain.active_events:
                if x >= current_event.position[0] and x <= current_event.position[0]+300 and y >= current_event.position[1] and y <= current_event.position[1]+20: # Check if click is within rectangle
                    selected_event = current_event
                    if x >= current_event.position[0]+5 and x <= current_event.position[0]+15 and y >= current_event.position[1]+5 and y <= current_event.position[1]+15:
                        chain.remove_event(selected_event)
                        selected_event = None
                        manager.clear_and_reset()
                        
            
 
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
                manager.clear_and_reset()
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
    # screen.fill("white")
    screen.fill("black")

    # RENDER GAME HERE
    draw_map = tile_map.generate_map()
    for draw_tile in draw_map:
        draw_regular_polygon(screen, draw_tile[0], draw_tile[1], draw_tile[2], [position[0]+draw_tile[3][0], position[1]+draw_tile[3][1]])

    if chain.active_events != []:
        draw_event(screen, chain.active_events)
    
    for unit in units.unit_list:
        draw_unit(screen, unit)
        
    manager.draw_ui(screen)

    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()