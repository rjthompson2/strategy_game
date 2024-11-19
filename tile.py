import random
biome_list = ["forrest", "desert", "plains"]
biome_dictionary = {
    "forrest": "dark green",
    "desert": "yellow",
    "plains": "light green"
}

class Tile():
    biome = None
    adjacency = []

    def generate_biome(self):
        if self.biome:
            return
        if self.adjacency == []:
            self.biome = random.choice(biome_list)
            return


    def get_color(self) -> str:
        return biome_dictionary[self.biome]

class TileMap():
    tiles = []
    def add_tile(self):
        tile = Tile()
        if self.tiles != []:
            for old_tile in self.tiles:
                if len(old_tile.adjacency) < 6:
                    old_tile.adjacency.append(tile)
                    tile.adjacency = old_tile
        tile.generate_biome()
        self.tiles.append(tile)

    def generate_map(self):
        _map = []
        radius = 103-3*len(self.tiles)
        for tile in self.tiles:
            _map.append([tile.get_color(), 6, radius, [500, 500]])
        return _map