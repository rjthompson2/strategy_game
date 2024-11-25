class EventOptionChain():
    def __init__(self):
        self.button_option = {}
        self.option_button = {}
        self.option_event = {}
        self.active_events = []
    
    def add_event(self, event):
        self.active_events.append(event)

    def add_pair_options(self, option, button):
        self.button_option.update({button: option})
        self.option_button.update({option: button})
    

    def add_pair_event(self, event):
        for option in event.options:
            self.option_event.update({option: event})

    def remove_and_choose_option(self, option, tile_map):
        button = self.option_button[option]
        event = self.option_event[option]
        event.choice(option, tile_map)
        del self.button_option[button]
        del self.option_button[option]
        del self.option_event[option]
        self.active_events.remove(event)


    def remove_option(self, option):
        button = self.option_button[option]
        event = self.option_event[option]
        del self.button_option[button]
        del self.option_button[option]
        del self.option_event[option]
        self.active_events.remove(event)
    

    def remove_event(self, event):
        self.remove_option(event.options[0])