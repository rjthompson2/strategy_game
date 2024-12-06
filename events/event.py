import pygame
from events.event_commands import *
from utils import *

events_dict = {
    "Starting Event": {
        "title": "A Brave New World",
        "description": "Our clan has roamed this area for many generations. We have struggled to survive, but some new arrivals have told us of their unique ways of life. Should we change our way of life or stick to the traditions of our ancestors?",
        "options": ["We will be Farmers", "We will be Herders", "We will continue as Hunter Gatherers"],
        "commands": [option_farmer, option_herder, option_hunter_gatherer]
    }
}


#Font
pygame.font.init()
title_font = pygame.font.SysFont('timesnewroman', 30)
description_font = pygame.font.SysFont('timesnewroman', 15)
option_font = pygame.font.SysFont('arial', 15)


class Event():
    def __init__(self, name):
        self.name = name
        if name in events_dict.keys():
            self.title = events_dict[name]["title"]
            self.description = events_dict[name]["description"]
            self.options = events_dict[name]["options"]
            self.position = [550, 90]
        else:
            self.title = ""
            self.description = ""
            self.options = []
            self.position = [550, 90]

    def choice(self, option, tile_map):
        current_event_dict = events_dict[self.name]
        i = current_event_dict["options"].index(option)
        current_event_dict["commands"][i](tile_map)


    def draw_event(self, surface):
        width = 300
        height = 500
        
        #check borders
        if self.position[0] < 0:
            self.position[0] = 0
        elif self.position[0] > MAX_WIDTH-width:
            self.position[0] = MAX_WIDTH-width
        x = self.position[0]

        if self.position[1] < 0:
            self.position[1] = 0
        elif self.position[1] > MAX_HEIGHT-height:
            self.position[1] = MAX_HEIGHT-height
        y = self.position[1]

        #create event window
        pygame.draw.rect(surface=surface, color="gray", rect=pygame.Rect((x, y, width, height)))
        #create exit button
        pygame.draw.rect(surface=surface, color="dark gray", rect=pygame.Rect((x+5, y+5, 10, 10)))
        
        # create a text surface object, on which text is drawn on it.
        title_text = title_font.render(self.title, False, (0, 0, 0))

        # text wrapping for descriptions
        descriptions = self.description.split(" ")
        description_text_list = []
        description = ""
        i = 0
        while i < len(descriptions):
            if len(description + descriptions[i]) < 41:
                description += " " + descriptions[i]
                i += 1
            else:
                description_text_list.append(description_font.render(description, False, (0, 0, 0)))
                description = ""
        if description != "":
            description_text_list.append(description_font.render(description, False, (0, 0, 0)))


        surface.blit(title_text, (x+10, y+20))
        i = 50
        for description_text in description_text_list:
            surface.blit(description_text, (x+10, y+i))
            i += 15
        i += 15
        
        for option in self.options:
            #create options buttons
            option_button = pygame.draw.rect(surface=surface, color=(90, 90, 90), rect=pygame.Rect((x+10, y+i, width-20, 50)))
            font_width, font_height = option_font.size(option)
            option_text = option_font.render(option, False, (200, 200, 200))
            surface.blit(option_text, (x+(width)//2-font_width//2, y+i+50//2-font_height//2))
            i += 55
