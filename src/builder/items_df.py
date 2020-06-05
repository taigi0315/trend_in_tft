import pandas as pd
import json
from collections import Counter

def add_item_count_percent_on_df(items_df):
    """
    Enrich the dataFrame with item use count in percentage
    Argumnets:
        items_df(dataFrame)
    Returns:
        item_df(dataFrame): item_df enriched with 'Count(%)' column
    """
    total_item_cnt = sum(items_df['Count'])
    items_df['Count(%)'] = items_df.apply(lambda row: (row.Count/total_item_cnt) * 100, axis=1)

    return items_df


def add_item_image_on_df(items_df):
    """
    Add image file path to df
    """

    items_df['Image'] = items_df.apply(lambda row: f"../../../assets/set3/items/{str(row.Id).zfill(2)}.png", axis=1)
    return items_df


def update_item_hashtable(item_hash, items_in_unit, player_placement):
    for item in items_in_unit:
        item_id = str(item)
        if item_id == '99':
            if item_id not in item_hash:
                item_hash[item_id] = {
                    'Id': item_id,
                    'Count': 1,
                    'Sum_Placement': player_placement,
                    'Placement_List': [player_placement]
                }
            else:
                item_hash[item_id]['Count'] += 1
                item_hash[item_id]['Sum_Placement'] += player_placement
                item_hash[item_id]['Placement_List'].append(player_placement)
        else:
            for item in items_in_unit:
                if item_id not in item_hash:
                    item_hash[item_id] = {
                        'Id': item_id,
                        'Count': 1,
                        'Sum_Placement': player_placement,
                        'Placement_List': [player_placement]
                    }
                else:
                    item_hash[item_id]['Count'] += 1
                    item_hash[item_id]['Sum_Placement'] += player_placement
                    item_hash[item_id]['Placement_List'].append(player_placement)
    
    return item_hash
    

def find_item_name(item_id_name_list, item_id):
     for item in item_id_name_list:
            if str(item['id']) == str(item_id):
                return item['name']
    

def build_items_df(match_data):
    """
    Build a dataframe for item usage analysis
    Arguments:
        match_data(DataFrame): list of match data(Dict)
    Returns:
        item_df(dataFrame): |Id(String) | Name(String) | Count(Int) | Average_Placement(Float) | Image(String)|
    """

    item_hashtable = {}
    for match in match_data:
        players = match['match']['info']['participants']
        for player in players:
            player_placement = player['placement']
            for unit in player['units']:
                    item_hashtable = update_item_hashtable(item_hashtable, unit['items'], player_placement)    
    
    with open('assets/set3/items.json') as f:
        item_id_name_list = json.load(f)
    
    
    items_df = pd.DataFrame(item_hashtable.values(), columns=['Id', 'Count', 'Sum_Placement', 'Placement_List'])
    items_df['Placements'] = items_df.apply(lambda row: dict(Counter(row.Placement_List)), axis=1)
    items_df['Name'] = items_df.apply(lambda row: find_item_name(item_id_name_list, row.Id), axis=1)
    items_df['Average_Placement'] = items_df.apply(lambda row: (row.Sum_Placement / row.Count), axis=1)
    items_df = add_item_image_on_df(items_df)
    items_df = add_item_count_percent_on_df(items_df)
    
    return items_df

                