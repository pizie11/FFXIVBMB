from statistics import median
from math import floor, ceil

import csv
import os
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
    "MD": "Mor Dhona",
}

mag_spells = "(|#1 Water Cannon| or |#2 Flame Thrower| or |#3 Aqua Breath| or |#6 High Voltage| or |#10 Glower| or |#11 Plaincracker| or |#19 Bomb Toss| or |#33 The Ram's Voice| or |#34 The Dragon's Voice| or |#37 Ink Jet| or |#41 Mind Blast|)"
phys_spells = "(|#4 Flying Frenzy| or |#5 Drill Cannons| or |#15 Sharpened Knife| or |#26 4-tonze Weight| or |#38 Fire Angon|)"

def generate_duty_list():
    duty_list = []

    dutyreader = csv.reader(pkgutil.get_data(__name__, "duties.csv").decode().splitlines(), delimiter=',', quotechar='|')
    
    for row in dutyreader:
        if row[0] != "" and row[0] != "Name":
            #print(', '.join(row))
            requires_str = "|10 Equip Levels:" + str(ceil(int(row[2])/10)) + "| and |" + row[4] + " Access:1|"
            requires_str += (" and |" + row[7] + "|") if  (row[7] != "") else ""
            #print(row[0]+": " + row[5] + "-" + row[6])
            duty_list.append(
                {
                    "name": row[0],
                    "region": "Solo Duty",
                    "category": [row[1]], #, row[4]],
                    "requires": requires_str,
                    "party" : row[5],
                    "diff" : row[6],
                }
            )
    return duty_list
    

duty_locations = generate_duty_list()

# called after the locations.json has been imported, but before ids, etc. have been assigned
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def before_location_table_processed(location_table: list) -> list:
    
    # add Masked Carnivale locations
    mc_list = []
    for i in range(1,25):
        mc_list.append({ 
            "name": "Masked Carnivale #" + str(i),
            "region": "Masked Carnivale",
            "category": ["Masked Carnivale"],
            "requires": []
        })

    # Special Requires
    mc_list[6]['requires'] = "|#31 Sticky Tongue| or |#25 Snort| and |Spell Slot:2|" #MC #7
    mc_list[7]['requires'] = "|#24 Flying Sardine| or |#28 Bad Breath| and |Spell Slot:2|" #MC 8
    mc_list[11]['requires'] = "(|#49 Viel of the Whorl| or |#16 Ice Spikes|) and (|#23 Faze| or |#19 Bomb Toss|) and |Spell Slot:3|" #MC #12
    mc_list[13]['requires'] = "|#7 Loom| or |#29 Diamondback|  and |Spell Slot:2|" #MC #14
    mc_list[14]['requires'] = "|#18 Acorn Bomb| and |Spell Slot:2|" #MC 15
    mc_list[15]['requires'] = "|#7 Loom| or |#29 Diamondback| and |Spell Slot:2|" #MC #16
    mc_list[18]['requires'] = phys_spells + "and |#37 Inkjet| and |Spell Slot:3|" #MC #19
    mc_list[19]['requires'] = "|#29 Diamondback| and |Spell Slot:2|" #MC #20
    mc_list[20]['requires'] = "|#7 Loom| or |#29 Diamondback| and |Spell Slot:2|" #MC #21
    mc_list[21]['requires'] = "|#7 Loom| or |#29 Diamondback| and |Spell Slot:2|" #MC #22
    mc_list[22]['requires'] = "|#29 Diamondback| and |Spell Slot:2|" #MC #23
    mc_list[23]['requires'] = mag_spells +" and " + phys_spells +"  and |#29 Diamondback| and |Spell Slot:3|"
    
    #Final Challenge
    mc_list.append({
        "name": "Masked Carnivale #25",
        "region": "Masked Carnivale",
        "category": ["Masked Carnivale"],
        "requires": "|#7 Loom| and " + mag_spells + " and " + phys_spells + " and |Spell Slot:3|",
        "victory": True
    })

    location_table.extend(mc_list)

    #add FATE locations
    fate_list = []
    fate_zones = {
        "MLN": [3,4,5,5,6,7,7,8,9,10,12,13,14,14,14], 
        "LLN": [3,4,5,6,7,8,9,9,10,10,11,12,13],
        "ELN": [30,30,31,32,32,32,32,32,32,32,32,32,33,33,33,33,33,33,33,33,34],
        "WLN": [10,10,12,12,13,15,15,16,16,17,17,18,18,40,40,44,44,44,45,45,46,48,49],
        "ULN": [20,20,20,20,21,23,30,30,31,31,33,33,34], 
        "OLN": [30,34,34,34,34,34,34,41,41,41,44,47,47,47,49],

        "CS": [4,5,5,7,8,8,9,9,10,10,11,11,12,13,14,30,30,31,31,31,33,34,43,50],
        "ES": [11,11,16,17,19,19,20,20,21,23,40,40,42,42,42,43,44,46,47,47,49,49,49,49],
        "SS": [21,22,22,22,23,24,28,29,29,29,30,31,32,32,32,32,32,33,34,46],
        "NS": [3,3,5,7,8,25,27,27,28,28,37,37,47,48],
        
        "CT": [5,5,5,6,7,7,7,9,9,11,12,14,14],
        "WT": [5,5,6,8,8,8,9,9,10,10,10,13,13,20,21,22,22,23],
        "ET": [15,17,17,17,17,17,18,18,19,26,26,26,26,26,26,27,29,40,42,42,42],
        "ST": [25,26,27,28,28,29,31,31,32,32,32,45,45,46,46,46,46,46,46,48,48,48,48,49,49,49,49],
        "NT": [49,49,49,49],

        "CCH": [35,35,35,36,36,36,36,37,37,38,38,38,38,38,38,38,39,39,39,39,39,40,40,40,40,40,45,45,45,46,47,47,48,49,49,49,50,50],
        "MD": [44,44,44,45,45,45,45,46,46,46,46,46,46,48],
    }

    for key in list(fate_zones.keys()):
        level = fate_zones[key][0]
        fate_list.append(create_FATE_location(1,key,level))
        fate_list.append(create_FATE_location(2,key,level))
        fate_list.append(create_FATE_location(3,key,level))
        #fate_list.append(create_FATE_location(4,key,level))
        #fate_list.append(create_FATE_location(5,key,level))
        # Old code for level-range FATE locations
        # arr = fate_zones[key]
        # lowest = arr[0]
        # midlow = int(calc_quantile(arr, 0.20))
        # mid = int(calc_quantile(arr, 0.40))
        # midtad = int(calc_quantile(arr, 0.60))
        # midhigh = int(calc_quantile(arr, 0.80))
        # # midlow = int(calc_quantile(arr, 0.25))
        # # mid = int(calc_quantile(arr, 0.50))
        # # midhigh = int(calc_quantile(arr, 0.75))
        # highest = arr[-1]
        # #Add low 
        # fate_list.append(create_FATE_location_range(1, key, lowest, midlow))
        # #Add mid-low 
        # fate_list.append(create_FATE_location_range(2, key, midlow, mid))
        # #Add mid
        # # fate_list.append(create_FATE_location(3, key, mid, midhigh))
        # fate_list.append(create_FATE_location_range(3, key, mid, midtad))
        # #Add midtad
        # fate_list.append(create_FATE_location_range(4, key, midtad, midhigh))
        # #add midhigh
        # fate_list.append(create_FATE_location_range(5, key, midhigh, highest))

    location_table.extend(fate_list)

    location_table.extend(duty_locations)

    return location_table

def create_FATE_location_range(number, key, low_lvl, high_lvl):
    return { 
            "name": key + "#" + str(number) + " Level " + str(low_lvl) + 
            "-" + str(high_lvl),
            "region": short_long[key],
            "category": ["FATEs"],
            "requires": "|10 Equip Levels:" + str(ceil(high_lvl/10)) + "|"
        }

def create_FATE_location(number, key, lvl):
    return { 
            "name": short_long[key] + ": FATE #" + str(number),
            "region": short_long[key],
            "category": ["FATEs"], #, short_long[key]],
            "requires": "|10 Equip Levels:" + str(ceil(lvl/10)) + "|"
        }

def calc_quantile(lst, q):
    s_lst = sorted(lst)

    idx = (len(s_lst) - 1)*q
    int_idx = int(idx)
    remainder = idx % 1
    if remainder > 0:
        lower_val = s_lst[int_idx]
        upper_val = s_lst[int_idx + 1]

        return lower_val * (1 - remainder) + upper_val * remainder
    else:
        return s_lst[int_idx]