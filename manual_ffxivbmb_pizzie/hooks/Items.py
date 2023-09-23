import csv
import os
import pkgutil


def generate_spell_list():
    spell_list = []

    spellreader = csv.reader(pkgutil.get_data(__name__, "spells.csv").decode().splitlines(), delimiter=',', quotechar='|')
    count = 1
    for row in spellreader:
        if row[0] != "" and row[0] != "Name" and row[0] != "ARR" and row[0] != "HW" and row[0] != "STB" and row[0] != "SHB":
            print("#" + str(count) + " " + row[0])
            spell_list.append(
                {
                    "name": "#" + str(count) + " " + row[0],
                    "category": [row[1]],
                    "count": 1,
                    row[5]: True
                }
            )
            count += 1
    return spell_list

spell_items = generate_spell_list()

# called after the items.json has been imported, but before ids, etc. have been assigned
# if you need access to the items after processing to add ids, etc., you should use the hooks in World.py
def before_item_table_processed(item_table: list) -> list:
    
    item_table.extend(spell_items)

    return item_table

# NOTE: Progressive items are not currently supported in Manual. Once they are, 
#       this hook will provide the ability to meaningfully change those.
def before_progressive_item_table_processed(progressive_item_table: list) -> list:
    return progressive_item_table
