import pygame
import pygame_gui
from tiles.tile import TileMap, draw_regular_polygon
from events.event import Event, event_chance
from chain import EventOptionChain
from units import Units
from utils import *


pygame.init()
pygame.display.set_caption('Strategy Game')
screen = pygame.display.set_mode((MAX_WIDTH, MAX_HEIGHT))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((MAX_WIDTH, MAX_HEIGHT))
#Font
pygame.font.init()
turn_font = pygame.font.SysFont('arial', 30)

running = True
moving = False
selected_event = None
selected_unit = None
civilization = False

position = [650, 400]

turn = 1
# zoom = 0

chain = EventOptionChain()
tile_map = TileMap()
units = Units()

#GUI
gui = True
end_turn_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((MAX_WIDTH-105, MAX_HEIGHT-55, 100, 50)),
    text='End Turn',
    manager=manager,
    visible=0)
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0, 100, 50)),
    text='New Game',
    manager=manager,
    visible=1,
    anchors={'centerx': 'centerx',
            'centery': 'centery'})

while running:
    time_delta = clock.tick(60)/1000.0
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #UI Buttons
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                tile_map.add_tile()
                chain.add_event(Event("Starting Event"))
                start_button.visible=0
                gui = False
            elif event.ui_element == end_turn_button:
                #TODO implement what happens at the end of the turn
                turn += 1
                # fulfill all old events
                if chain.active_events != []:
                    for active_event in chain.active_events:
                        chain.remove_and_choose_option(active_event.options[0], tile_map)
                # chance to add an event
                new_event = event_chance(units.unit_list[0].type, turn)
                if new_event:
                    chain.add_event(new_event)
                # units update
                units.update()
            elif event.ui_element in chain.button_option.keys():
                #clear all options in that event from the list
                #activate the option
                option = chain.button_option[event.ui_element]
                chain.remove_and_choose_option(option, tile_map)

        # Making the screen move
        elif event.type == pygame.MOUSEBUTTONDOWN:
            moving = True
            x, y = pygame.mouse.get_pos() # Get click position
            lock = False
            for current_event in chain.active_events:
                # Top bar selected
                if x >= current_event.position[0] and x <= current_event.position[0]+300 and y >= current_event.position[1] and y <= current_event.position[1]+20: # Check if click is within rectangle
                    selected_event = current_event
                    # Close event
                    if x >= current_event.position[0]+5 and x <= current_event.position[0]+15 and y >= current_event.position[1]+5 and y <= current_event.position[1]+15:
                        chain.remove_event(selected_event)
                        selected_event = None
                    lock = True
                # Event option selected
                else:
                    for i, option in enumerate(current_event.options_positions):
                        if x >= option[0] and x <= option[2] and y >= option[1] and y <= option[3]:
                            # figure out which option was selected
                            chain.remove_and_choose_option(current_event.options[i], tile_map)
                            break
                    lock = True
            # Locks to prevent clicking multiple different objects
            if not lock:
                original = (150, 100, 100)
                new = (90, 60, 60)
                if selected_unit and selected_unit.current_moves > 0:
                    neighbor = selected_unit.within_neightbors([x-position[0], y-position[1]])
                    if neighbor:
                        selected_unit.current_tile = neighbor
                        selected_unit.change_color(original)
                        selected_unit.current_moves -= 1
                        selected_unit = None
                for unit in units.unit_list:
                    if x >= position[0]+unit.current_tile.position[0]-10 and x <= position[0]+unit.current_tile.position[0]+10 and y >= position[1]+unit.current_tile.position[1]-10 and y <= position[1]+unit.current_tile.position[1]+10:
                        # Select a unit
                        if unit.color == original and selected_unit is None:
                            unit.change_color(new)
                            selected_unit = unit
                        # Deselect aunit
                        elif selected_unit:
                            selected_unit = None
                            unit.change_color(original)
                        lock = True
                    # Event to create a civilization at 100 population
                    if unit.amount >= 100 and not civilization:
                        chain.add_event(Event("Civilization"))
                        civilization = True
               
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
        elif event.type == pygame.MOUSEMOTION and moving:
            # Make events move
            if selected_event:
                selected_event.position = [selected_event.position[0] + event.rel[0], selected_event.position[1] + event.rel[1]]

            # Make the background tiles move
            else:
                position = [position[0] + event.rel[0], position[1] + event.rel[1]]
        
        # Zoom in and out
        # if event.button == 3: 
        #     zoom += 1
        # elif event.button == 4: 
        #     zoom -= 1
        #     print(zoom)

        manager.process_events(event)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER GAME HERE
    draw_map = tile_map.generate_map()
    for draw_tile in draw_map:
        draw_regular_polygon(screen, draw_tile[0], draw_tile[1], draw_tile[2], [position[0]+draw_tile[3][0], position[1]+draw_tile[3][1]])

    for unit in units.unit_list:
        unit.draw_unit(screen, position)
        if selected_unit:
            selected_unit.display_info(screen, position)
    
    if chain.active_events != []:
        for active_event in chain.active_events:
            active_event.draw_event(screen)
    
    
    if not gui:
        screen.blit(turn_font.render(str(turn), False, (255, 255, 255)), (5, 5))
        end_turn_button.visible=1
        
    manager.update(time_delta)
    manager.draw_ui(screen)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()