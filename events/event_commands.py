from units import Units, Unit
units = Units()

# Event: "A Brave New World"
# Option: "We will be Farmers"
def option_farmer(tile_map):
    #create a farmer unit
    unit = Unit(tile_map.tiles[0])
    unit.set_type("farmer")
    units.add_unit(unit)
    return

# Event: "A Brave New World"
# Option: "We will be Herders"
def option_herder(tile_map):
    # add 6 more tiles
    for i in range(6):
        tile_map.add_tile()
    #create a herder unit
    unit = Unit(tile_map.tiles[0])
    unit.set_type("herder")
    units.add_unit(unit)
    return

# Event: "A Brave New World"
# Option: "We will continue as Hunter Gatherers"
def option_hunter_gatherer(tile_map):
    # add 18 more tiles
    for i in range(18):
        tile_map.add_tile()
    #create a hunter_gatherer unit
    unit = Unit(tile_map.tiles[0])
    unit.set_type("hunter_gatherer")
    units.add_unit(unit)
    return