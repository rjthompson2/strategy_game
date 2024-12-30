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
    unit.set_type("hunter gatherer")
    units.add_unit(unit)
    return

# Event: "Flu Season"
# Option: "Nothing. This will pass"
def flu_nothing(tile_map):
    for unit in units.unit_list:
        unit.amount -= (unit.amount*0.1)//1
    return

# Event: "Flu Season"
# Option: "This is a sign. We must renounce our way of life"
def flu_change(tile_map):
    for unit in units.unit_list:
        unit.set_type("hunter gatherer")
    return

# Event: "Year of Plenty"
# Option: "We shall have a feast"
def plenty_feast(tile_map):
    for unit in units.unit_list:
        unit.amount += 3
    return

# Event: "Year of Plenty"
# Option: "We shall add it to our stockpile"
def plenty_stock(tile_map):
    for unit in units.unit_list:
        unit.food += unit.food*2
    return

# Event: "Year of Plenty"
# Option: "Let us show thanks with a sacrifice"
def plenty_sacrifice(tile_map):
    #TBD
    return