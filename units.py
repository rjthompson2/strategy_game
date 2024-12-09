import pygame

class Unit():
    def __init__(self, tile):
        self.current_tile = tile
        self.health = 100
        self.food = 0
        self.type = None
        self.amount = 10
        self.color = (150, 100, 100)
    
    def set_type(self, new_type):
        self.type = new_type

    def get_food(self):
        if self.type != "farmer":
            if self.type == "herder":
                self.food += amount*5
            else:
                self.food += amount*self.current_tile.forage
        else:
            self.food += amount*self.current_tile.soil
    
    def change_color(self, color):
        self.color = color

    def draw_unit(self, surface):
        pygame.draw.circle(surface, self.color, [position[0]+self.current_tile.position[0], position[1]+self.current_tile.position[1]], 20)

class Units():
    unit_list = []

    def add_unit(self, unit):
        self.unit_list.append(unit)