# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. set_rules - Creates rules for accessing regions and locations
##    3. generate_basic - Creates the item pool and runs any place_item options
##    4. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Called before regions and locations are created. Not clear why you'd want this, but it's here.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    party_size = get_option_value(multiworld, player, "party_size") or 0
    duty_diff = get_option_value(multiworld, player, "duty_diff") or 0
    expac_goal = get_option_value(multiworld, player, "expac_goal") or 0
    main_duties = get_option_value(multiworld, player, "main_duties") or 0

    # Include Basic Instinct in requirements for duties if going solo
    if party_size == 0:
        region_table["Duty"]["requires"] += " and |#91 Basic Instinct|" 
    
    locations_to_remove = []
    # Remove locations based on options
    for location in world.location_table:

        # Based on party size
        if "party" in location:
            # Remove Alliance
            if party_size < 3 and location["party"] == "Alliance":
                locations_to_remove.append(location)
                continue
            # Remove Full Party
            if party_size < 2 and location["party"] == "Full Party":
                locations_to_remove.append(location)
                continue
            # Remove Light Party
            if party_size < 1 and location["party"] == "Light Party":
                locations_to_remove.append(location)
                continue
        # Based on difficulty
        if "diff" in location:
            # Remove Savage
            if party_size < 2 and location["diff"] == "Savage":
                locations_to_remove.append(location)
                continue
            # Remove Hard
            if party_size < 1 and location["diff"] == "Hard":
                locations_to_remove.append(location)
                continue
        # remove main scenario
        if location["name"] == "Castrum Meridianum" or location["name"] == "The Praetorium" or location["name"] == "The Porta Decumana":
            locations_to_remove.append(location)
            continue


    #print(world.location_name_to_location)

    for location in locations_to_remove:
        location_table.remove(location)
        world.location_name_to_location.pop(location["name"])
        temp =  world.location_name_to_id.pop(location["name"])
        del world.location_id_to_name[temp]


# Called after regions and locations are created, in case you want to see or modify that information.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass
    # party_size = get_option_value(multiworld, player, "party_size") or 0

    # # Update duty region requirements based on party size
    # if party_size != 0:
    #     for region in multiworld.regions:
    #         if region.name != "Solo Duty" and region.player == player:
    #             region["requires"] = "|#77 Aetherial Mimicry| and |#58 Pom Cure| and |Spell Slot:2|"


    
    

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def before_generate_basic(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is called before the victory location has the victory event placed and locked
def before_pre_fill(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is called after the victory location has the victory event placed and locked
def after_pre_fill(world: World, multiworld: MultiWorld, player: int):
    pass

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    slot_data["party_size"] = get_option_value(multiworld, player, "party_size") or 0
    slot_data["duty_diff"] = get_option_value(multiworld, player, "duty_diff") or 0
    slot_data["expac_goal"] = get_option_value(multiworld, player, "expac_goal") or 0
    slot_data["main_duties"] = get_option_value(multiworld, player, "main_duties") or 0

    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data