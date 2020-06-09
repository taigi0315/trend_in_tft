import copy
import json

with open('assets/set3/items.json') as f:
    ITEM_DATA = json.load(f)
    ITEM_NAMES = [item['name'] for item in ITEM_DATA]
    
with open('assets/set3/champions.json') as f:
    CHAMPION_DATA = json.load(f)
    CHAMPION_IDS = [champ['championId'] for champ in CHAMPION_DATA]
    CHAMPION_NAMES = [champ['name'].replace(" ", "").replace("'", "") for champ in CHAMPION_DATA]
    CHAMPION_COSTS = [champ['cost'] for champ in CHAMPION_DATA]

with open('assets/set3/traits.json') as f:
    TRAIT_DATA = json.load(f)
    # Build traits names ex) Blaster_1, Blaster_2
    TRAIT_NAMES = []
    for trait in TRAIT_DATA:
        for i in range(len(trait['sets'])):
            trait_level = trait['key'] + '_' + str(i+1)
            TRAIT_NAMES.append(trait_level)

def find_item_name(item_id):
     for item in ITEM_DATA:
            if str(item['id']) == str(item_id):
                return item['name']