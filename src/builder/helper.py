import copy
import json

with open('assets/TFT_set_data/set3/items.json') as f:
    ITEM_DATA = json.load(f)
    ITEM_NAMES = [item['name'] for item in ITEM_DATA]
    ITEM_IDS = [item['id'] for item in ITEM_DATA]
    
with open('assets/TFT_set_data/set3/champions.json') as f:
    CHAMPION_DATA = json.load(f)
    CHAMPION_IDS = [champ['championId'] for champ in CHAMPION_DATA]
    CHAMPION_NAMES = [champ['name'].replace(" ", "").replace("'", "") for champ in CHAMPION_DATA]
    CHAMPION_COSTS = [champ['cost'] for champ in CHAMPION_DATA]

with open('assets/TFT_set_data/set3/traits.json') as f:
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

def calculate_average_placement(row):
    """
    Calculate average placement
    Example Input:
        |1|2|3|4|5|6|7|8|
    row_1|0|0|2|0|2|2|0|1|
    Example Output:
        5.14...
    """

    sum = 1*row['1']+2*row['2']+3*row['3']+4*row['4']+5*row['5']+6*row['6']+7*row['7']+8*row['8']
    count = row['1']+row['2']+row['3']+row['4']+row['5']+row['6']+row['7']+row['8']
    if sum == 0:
        return 0
    return round(float(sum/count), 2)