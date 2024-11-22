import pygame
events_dict = {
    "Starting Event": {
        "title": "A Brave New World",
        "description": "Our clan has roamed this area for many generations. We struggled to survive, but some new arrivals have told us of their unique ways of life. Should we change our way of life or stick to the traditions of our ancestors?",
        "options": ["We will be Farmers", "We will be Herders", "We will stick to the old traditions of our Hunter_Gatherer ancestors"]
    }
}


class Event():
    def __init__(self, name):
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

