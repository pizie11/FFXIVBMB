from math import ceil

import csv
import pkgutil

short_long = {
    "MLN": "Middle La Noscea",
    "LLN": "Lower La Noscea",
    "ELN": "Eastern La Noscea",
    "WLN": "Western La Noscea",
    "ULN": "Upper La Noscea",
    "OLN": "Outer La Noscea",

    "CS": "Central Shroud",
    "ES": "East Shroud",
    "SS": "South Shroud",
    "NS": "North Shroud",

    "CT": "Central Thanalan",
    "WT": "Western Thanalan",
    "ET": "Eastern Thanalan",
    "ST": "Southern Thanalan",
    "NT": "Northern Thanalan",

    "CCH": "Coerthas Central Highlands",
    "CWH": "Coerthas Western Highlands",

    "MD": "Mor Dhona",

    "TSC": "The Sea of Clouds",
    "AL": "Azys Lla",

    "TDF": "The Dravanian Forelands",
    "TCM": "The Churning Mists",
    "TDH": "The Dravanian Hinterlands",

    "TF": "The Fringes",
    "TP": "The Peaks",
    "TL": "The Lochs",

    "TRS": "The Ruby Sea",
    "Y": "Yanxia",
    "TAS": "The Azim Steppe",

    "L": "Lakeland",
    "K": "Kholusia",
    "IM": "Il Mheg",
    "AA": "Amh Araeng",
    "TRG": "The Rak'tika Greatwood",
    "TT": "The Tempest"
}

mag_spells = "("
phys_spells = "("

def generate_spell_list():
    spell_list = []

    global mag_spells
    global phys_spells

    spellreader = csv.reader(pkgutil.get_data(__name__, "spells.csv").decode().splitlines(), delimiter=',', quotechar='|')
    count = 1
    for row in spellreader:
        if row[0] not in ["", "Name", "ARR", "HW", "STB", "SHB"]:
            #print("#" + str(count) + " " + row[0])
            spell_list.append(
                {
                    "name": "#" + str(count) + " " + row[0],
                    "category": [row[1]],
                    "count": 1,
                    row[5]: True
                }
            )

            if row[1] == "Damage" and row[2] == "Magic":
                mag_spells += "|#" + str(count) + " " + row[0] + "| or "
            if row[1] == "Damage" and row[2] == "Physical":
                phys_spells += "|#" + str(count) + " " + row[0] + "| or "

            count += 1

    mag_spells = mag_spells[:-4] +")"
    phys_spells = phys_spells[:-4] +")"

    return spell_list

spell_items = generate_spell_list()
#print(mag_spells)
#print(phys_spells)

def generate_duty_list():
    duty_list = []

    dutyreader = csv.reader(pkgutil.get_data(__name__, "duties.csv").decode().splitlines(), delimiter=',', quotechar='|')

    for row in dutyreader:
        if row[0] not in ["", "Name", "ARR", "HW", "STB", "SHB"]:
            #print(', '.join(row))
            #print(str(ceil(int(row[2])/10)) + " "+ str(ceil(int(row[3])/10)))
            requires_str = "|10 Equip Levels:" + str(ceil(int(row[2])/10)) + "| and |" + row[4] + " Access:1|"
            requires_str += (" and |" + row[7] + "|") if  (row[7] != "") else ""
            #print(requires_str)
            #print(row[0]+": " + row[5] + "-" + row[6])
            duty_list.append(
                {
                    "name": row[0],
                    "region": "Duty",
                    "category": [row[1], row[4]],
                    "requires": requires_str,
                    #"level" : row[3]
                    "party" : row[5],
                    "diff" : row[6],
                }
            )

    return duty_list


duty_locations = generate_duty_list()

# called after the game.json file has been loaded
def after_load_game_file(game_table: dict) -> dict:
    return game_table

# called after the items.json file has been loaded, before any item loading or processing has occurred
# if you need access to the items after processing to add ids, etc., you should use the hooks in World.py
def after_load_item_file(item_table: list) -> list:
    item_table.extend(spell_items)
    return item_table

# NOTE: Progressive items are not currently supported in Manual. Once they are,
#       this hook will provide the ability to meaningfully change those.
def after_load_progressive_item_file(progressive_item_table: list) -> list:
    return progressive_item_table

# called after the locations.json file has been loaded, before any location loading or processing has occurred
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def after_load_location_file(location_table: list) -> list:
        # add Masked Carnivale locations
    mc_list = []
    for i in range(1,32):
        mc_list.append({
            "name": "Masked Carnivale #" + str(i),
            "region": "Masked Carnivale",
            "category": ["Masked Carnivale"],
            "requires": []
        })

    # Special Requires
    mc_list[6]['requires'] = "|#31 Sticky Tongue| or |#25 Snort| and |Spell Slot:2|" #MC #7
    mc_list[7]['requires'] = "|#24 Flying Sardine| or |#28 Bad Breath| and |Spell Slot:2|" #MC 8
    mc_list[11]['requires'] = "(|#49 Veil of the Whorl| or |#16 Ice Spikes|) and (|#23 Faze| or |#19 Bomb Toss|) and |Spell Slot:3|" #MC #12
    mc_list[13]['requires'] = "|#7 Loom| or |#29 Diamondback|  and |Spell Slot:2|" #MC #14
    mc_list[14]['requires'] = "|#18 Acorn Bomb| and |Spell Slot:2|" #MC 15
    mc_list[15]['requires'] = "|#7 Loom| or |#29 Diamondback| and |Spell Slot:2|" #MC #16
    mc_list[18]['requires'] = phys_spells + " and |#37 Ink Jet| and |Spell Slot:3|" #MC #19
    mc_list[19]['requires'] = "|#29 Diamondback| and |Spell Slot:2|" #MC #20
    mc_list[20]['requires'] = "|#7 Loom| or |#29 Diamondback| and |Spell Slot:2|" #MC #21
    mc_list[21]['requires'] = "|#7 Loom| or |#29 Diamondback| and |Spell Slot:2|" #MC #22
    mc_list[22]['requires'] = "|#29 Diamondback| and |Spell Slot:2|" #MC #23
    mc_list[23]['requires'] = mag_spells +" and " + phys_spells +"  and |#29 Diamondback| and |Spell Slot:3|" #MC 24
    mc_list[24]['requires'] = "|#7 Loom| and " + mag_spells + " and " + phys_spells + " and |Spell Slot:3|" #MC 25

    mc_list[25]['requires'] = "|10 Equip Levels:6| and |#57 Eerie Soundwave| and |#73 Exuviation| and |Spell Slot:3|" #MC 26
    mc_list[26]['requires'] = "|10 Equip Levels:6| and |#1 Water Cannon| and (|#31 Sticky Tongue| or |#25 Snort| or |#51 Protean Wave|) and |Spell Slot:3|" #MC 27
    mc_list[27]['requires'] = "|10 Equip Levels:6| and |#38 Fire Angon| and |Spell Slot:2|" #MC 28
    mc_list[28]['requires'] = "|10 Equip Levels:6| and |#24 Flying Sardine| and |#53 Electrogenesis| and |#29 Diamondback| and |Spell Slot:4|" #MC 29
    mc_list[29]['requires'] = "|10 Equip Levels:6| and |#73 Exuviation| and |#55 Abyssal Transfixion| and |Spell Slot:3|" #MC 30

    mc_list[30]['requires'] = "|10 Equip Levels:7| and |#24 Flying Sardine| and |#57 Eerie Soundwave| and |#73 Exuviation| and |#29 Diamondback| and |Spell Slot:6|" #MC 31
    #Final Challenge
    mc_list.append({
        "name": "Masked Carnivale #32",
        "region": "Masked Carnivale",
        "category": ["Masked Carnivale"],
        "requires": "|10 Equip Levels:8| and |#73 Exuviation| and |#29 Diamondback| and |#30 Mighty Guard| and |#33 The Ram's Voice| and |#92 Ultravibration| and |#24 Flying Sardine| and |#7 Loom| and " + phys_spells + " and |Spell Slot:8|",
        "victory": True
    })

    location_table.extend(mc_list)

    #add FATE locations
    fate_list = []
    fate_zones = {
        "MLN": [3,3],
        "LLN": [3,3],
        "ELN": [30,30],
        "WLN": [10,10,],
        "ULN": [20,20],
        "OLN": [30,30],

        "CS": [4,4],
        "ES": [11,11],
        "SS": [21,21],
        "NS": [3,3],

        "CT": [5,5],
        "WT": [5,5],
        "ET": [15,15],
        "ST": [25,26],
        "NT": [49,49],

        "CCH": [35,35],
        "CWH": [50, 130],

        "MD": [44,44],

        "TSC": [50, 130],
        "AL": [59, 145],

        "TDF": [52, 130],
        "TCM": [54, 130],
        "TDH": [58, 145],

        "TF": [60,0],
        "TP": [60,0],
        "TL": [69,0],

        "TRS": [62],
        "Y": [64],
        "TAS": [65],

        "L": [70],
        "K": [70],
        "IM": [72],
        "AA": [76],
        "TRG": [74],
        "TT": [79]
    }

    for key in list(fate_zones.keys()):
        level = fate_zones[key][0]
        #ilvl = fate_zones[key][1]
        fate_list.append(create_FATE_location(1,key,level))
        fate_list.append(create_FATE_location(2,key,level))
        fate_list.append(create_FATE_location(3,key,level))
        #fate_list.append(create_FATE_location(4,key,level))
        #fate_list.append(create_FATE_location(5,key,level))

    location_table.extend(fate_list)

    location_table.extend(duty_locations)

    return location_table

# called after the locations.json file has been loaded, before any location loading or processing has occurred
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def after_load_region_file(region_table: dict) -> dict:
    return region_table


def create_FATE_location(number, key, lvl):
    return {
            "name": short_long[key] + ": FATE #" + str(number),
            "region": short_long[key],
            "category": ["FATEs", short_long[key]],
            "requires": "|10 Equip Levels:" + str(ceil(lvl/10)) + "|"
        }

# called after the categories.json file has been loaded
def after_load_category_file(category_table: dict) -> dict:
    return category_table


# called after the categories.json file has been loaded
def after_load_option_file(option_table: dict) -> dict:
    # option_table["core"] is the dictionary of modification of existing options
    # option_table["user"] is the dictionary of custom options
    return option_table

# called after the meta.json file has been loaded and just before the properties of the apworld are defined. You can use this hook to change what is displayed on the webhost
# for more info check https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#webworld-class
def after_load_meta_file(meta_table: dict) -> dict:
    return meta_table

# called when an external tool (eg Universal Tracker) ask for slot data to be read
# use this if you want to restore more data
# return True if you want to trigger a regeneration if you changed anything
def hook_interpret_slot_data(world, player: int, slot_data: dict[str, any]) -> dict | bool:
    return False
