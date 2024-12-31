import random
import pygame
from math import *

biome_list = ["forrest", "desert", "plains", "mountains"]
biome_dictionary = {
    "forrest": "dark green",
    "desert": "yellow",
    "plains": "light green",
    "mountains": "grey"
}
biome_soil = {
    "forrest": {
        "soil": 8,
        "forage": 8
    },
    "desert": {
        "soil": 0,
        "forage": 3
    },
    "plains": {
        "soil": 10,
        "forage": 6
    },
    "mountains": {
        "soil": 3,
        "forage": 4
    }
}

class Tile():
    def __init__(self):
        self.biome = None
        self.adjacency = [0, 0, 0, 0, 0, 0]
        self.position = [0, 0]
        self.soil = None
        self.forage = None

    def generate_biome(self):
        if self.biome:
            return
        if self.adjacency == []:
            self.biome = random.choice(biome_list)
            self.soil = biome_soil[self.biome]["soil"]
            self.forage = biome_soil[self.biome]["forage"]
            return

        #TODO generate biomes better
        adjacent_biomes = biome_list
        for tile in self.adjacency:
            if tile != 0:
                adjacent_biomes.append(tile.biome)
        self.biome = random.choice(biome_list)
        self.soil = biome_soil[self.biome]["soil"]
        self.forage = biome_soil[self.biome]["forage"]

    def get_color(self) -> str:
        return biome_dictionary[self.biome]
    
    def update_position(self, position, old_position):
        if position == 0:
            self.position = [old_position[0], old_position[1]-180]
        elif position == 1:
            self.position = [old_position[0]+156, old_position[1]-90]
        elif position == 2:
            self.position = [old_position[0]+156, old_position[1]+90]
        elif position == 3:
            self.position = [old_position[0], old_position[1]+180]
        elif position == 4:
            self.position = [old_position[0]-156, old_position[1]+90]
        elif position == 5:
            self.position = [old_position[0]-156, old_position[1]-90]

    def draw_regular_polygon(self, surface, color, vertex_count, radius, position, width=0):
        n, r = vertex_count, radius
        x, y = position
        pygame.draw.polygon(surface, color, [
            (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
            for i in range(n)
        ], width)


class TileMap():
    def __init__(self):
        self.tiles = []

    def add_tile(self):
        tile = Tile()
        if self.tiles == []:
            tile.generate_biome()
            self.tiles.append(tile)
            return
        for old_tile in self.tiles:
            neighbors = old_tile.adjacency
            if 0 in neighbors:
                for i, value in enumerate(neighbors):
                    if value == 0:
                        old_tile.adjacency[i] = tile
                        tile.adjacency[(i+3)%6] = old_tile

                        if old_tile.adjacency[(i+1)%6] != 0:
                            adj_tile = old_tile.adjacency[(i+1)%6]
                            adj_tile.adjacency[(i-1)%6] = tile
                            tile.adjacency[(i+2)%6] = adj_tile
                        if old_tile.adjacency[(i-1)%6] != 0:
                            adj_tile = old_tile.adjacency[(i-1)%6]
                            adj_tile.adjacency[(i+1)%6] = tile
                            tile.adjacency[(i-2)%6] = adj_tile

                        tile.update_position(i, old_tile.position)
                        tile.generate_biome()
                        self.tiles.append(tile)
                        return

    def generate_map(self):
        _map = []
        for tile in self.tiles:
            _map.append([tile.get_color(), 6, 100, tile.position])
        return _map



def draw_regular_polygon(surface, color, vertex_count, radius, position, width=0):
    n, r = vertex_count, radius
    x, y = position
    pygame.draw.polygon(surface, color, [
        (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
        for i in range(n)
    ], width)