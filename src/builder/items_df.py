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

    items_df['Image'] = items_df.apply(lambda row: f"../../../assets/TFT_set_data/set3/items/{str(row.Id).zfill(2)}.png", axis=1)
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
