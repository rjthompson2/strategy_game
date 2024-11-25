import pygame
from events.event_commands import *

events_dict = {
    "Starting Event": {
        "title": "A Brave New World",
        "description": "Our clan has roamed this area for many generations. We have struggled to survive, but some new arrivals have told us of their unique ways of life. Should we change our way of life or stick to the traditions of our ancestors?",
        "options": ["We will be Farmers", "We will be Herders", "We will continue as Hunter Gatherers"],
        "commands": [option_farmer, option_herder, option_hunter_gatherer]
    }
}


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

