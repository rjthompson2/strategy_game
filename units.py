import pygame

pygame.font.init()
display_font = pygame.font.SysFont('timesnewroman', 20)

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
                self.food += (self.amount//2)*5
            else:
                self.food += (self.amount//2)*self.current_tile.forage
        else:
            self.food += (self.amount//2)*self.current_tile.soil
    
    def change_color(self, color):
        self.color = color

    def draw_unit(self, screen, position):
        pygame.draw.circle(screen, self.color, [position[0]+self.current_tile.position[0], position[1]+self.current_tile.position[1]], 20)
    
    def get_info(self):
        return f"Health: {self.health}\nFood: {self.food}\nType: {self.type}\nAmount: {self.amount}"
    
    def display_info(self, screen, position):
        display_text = display_font.render(self.get_info(), False, (255, 255, 255))
        screen.blit(display_text, (position[0]+self.current_tile.position[0]+10, position[1]+self.current_tile.position[1]))


class Units():
    unit_list = []

    def add_unit(self, unit):
        self.unit_list.append(unit)
    
    def update(self):
        for i, unit in enumerate(self.unit_list):
            unit.get_food()
            if unit.food <= 0:
                unit.health -= 10
            if unit.health < 0:
                self.unit_list.remove(i)
            if unit.food > unit.amount**2:
                if unit.health < 100:
                    unit.health += 10
                else:
                    unit.amount += 1
                unit.food = 0
            elif unit.food < unit.amount:
                unit.amount = unit.amount*(unit.food/unit.amount)//1