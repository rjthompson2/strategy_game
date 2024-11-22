class EventOptionChain():
    def __init__(self):
        self.button_option = {}
        self.option_button = {}
        self.option_event = {}
    
    def add_pair_options(self, option, button):
        self.button_option.update({button: option})
        self.option_button.update({option: button})
    

    def add_pair_event(self, event):
        for option in event.options:
            self.option_event.update({option: event})

    def remove(self, option):
        button = self.option_button[option]
        del self.button_option[button]
        del self.option_button[option]
        del self.option_event[option]