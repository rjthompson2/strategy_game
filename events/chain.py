class EventOptionChain():
    def __init__(self):
        self.option_event = {}
        self.active_events = []
    
    def add_event(self, event):
        self.active_events.append(event)
        self.add_pair_event(event)

    def add_pair_event(self, event):
        for option in event.options:
            self.option_event.update({option: event})

    def remove_and_choose_option(self, option, tile_map):
        event = self.option_event[option]
        event.choice(option, tile_map)
        del self.option_event[option]
        self.active_events.remove(event)


    def remove_option(self, option):
        event = self.option_event[option]
        del self.option_event[option]
        self.active_events.remove(event)
    

    def remove_event(self, event):
        self.remove_option(event.options[0])