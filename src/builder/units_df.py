import os
import pandas as pd
import numpy as np
from collections import Counter
import json

from .helper import ITEM_NAMES

CHAMPIONS = None
with open('assets/set3/champions.json') as f:
        CHAMPIONS  = json.load(f)

def get_units_in_single_match(single_match_data):
    """
    Extract all unit data from single match data, and
    enrich each unit data with players placement and traits
    Arguments: 
        single_match_data(Dict): response from Riot API match details
    Returns:
        units(List): All units used in the match
    """
    
    players = single_match_data['match']['info']['participants']
    units = []
    for p in players:
        player_units = p['units']        
        
        # Enrich each unit data with placement
        # This will be used to calculate average placement for the unit
        for unit in player_units:
            unit['placement'] = p['placement']
        
        # Enrich each unit data with traits
        # This will be used to calculate most used trait for the unit
        for unit in player_units:
            unit['traits'] = []
            for trait in p['traits']:
                if trait['tier_current'] > 0:
                    trait_level = trait['name'] + '_' + str(trait['tier_current'])
                    unit['traits'].append(trait_level)

        units += player_units

    return units


def get_units_in_multi_match(multi_match_data):
    """
    Get unit data from list of multiple matches
    Arguments:
        multi_match_data(List):
    Returns:
        units(List)
    """
    units = []
    for match in multi_match_data:
        units = units + get_units_in_single_match(match)
    
    return units


def build_unit_hashtable(unit_list):
    """
    Build unit hashtable
    Arguments:
        unit_list(List): list of all units used in game
    Returns:
        unit_hash(Dict): 
            Key(String): name of unit
            Value(List): data of each units
    """
    unit_hash = {}

    for unit in unit_list:
        unit_name = unit['character_id']
        if unit_name not in unit_hash.keys():
             unit_hash[unit_name] = [unit]
        else:
             unit_hash[unit_name].append(unit)
    
    return unit_hash


def add_average_tier_on_units_df(unit_df):
    """
    Enrich the dataFrame with average tier of units column
    Argumnets:
        unit_df(dataFrame): result dataframe from 'build_unit_use_count_tier_item_df' function
    Returns:
        unit_df(dataFrame): unit_df enriched with Average_Tier column
    """

    def calculate_average_tier(cnt, tier_hash):
        """
        Calculate average of tier
        Arguments:
            tier_dict(Dict)
        Returns:
            average_tier(Float)
        """
        sum = 0
        for key, val in tier_hash.items():
            sum += (int(key) * int(val))

        return sum/cnt
            
    unit_df['Average_Tier'] = unit_df.apply(lambda row: calculate_average_tier(row.Count, row.Tier), axis=1)
    
    return unit_df


def add_average_num_item_on_units_df(units_df):
    """
    Enrich the dataFrame with average number of item column
    Argumnets:
        unit_df(dataFrame): result dataframe from 'build_unit_use_count_tier_item_df' function
    Returns:
        unit_df(dataFrame): unit_df enriched with Average_Num_Item column
    """
    def calculate_average_num_item(cnt, used_item_hash):
        """
        Calculate average of tier
        Arguments:
            used_item_hash(Dict)
        Returns:
            average_num_item(Float)
        """
        sum = 0
        for item_id, item_data in used_item_hash.items():
            sum += int(item_data['Count'])

        return sum/cnt
            
    units_df['Average_#_Item'] = units_df.apply(lambda row: calculate_average_num_item(row.Count, row.Item), axis=1)
    return units_df


def add_unit_count_percent_on_df(unit_df):
    """
    Enrich the dataFrame with unit use count in percentage
    Argumnets:
        unit_df(dataFrame)
    Returns:
        unit_df(dataFrame): unit_df enriched with 'Count(%)' column
    """

    total_unit_count = sum(unit_df['Count'])
    unit_df['Count(%)'] = unit_df.apply(lambda row: (row.Count/total_unit_count)*100, axis=1)
    
    return unit_df


def convert_traits(player_traits):
    """
    Convert player traits dict to list of traits with its tier
    Arguments:
        player_traits(List): traits filed from match data
    Returns:
        traits_list(List): list of name of traits with its tier combined
    """
    traits_list = []
    for t in player_traits:
        if t['tier_current'] > 0:
            traits_with_tier = f"{t['name']}_{t['tier_current']}"
            traits_list.append(traits_with_tier)
    
    return traits_list


def add_champion_image_on_df(units_df):
    """
    Add image file path to df
    """
    
    units_df['Image'] = units_df.apply(lambda row: f"../../../assets/set3/champions/{str(row.Name).lower()}.png", axis=1)
    return units_df


def get_champion_cost(champion_id):
    for champ in CHAMPIONS:
            if str(champ['championId']) == str(champion_id):
                return champ['cost']


def convert_champion_id_to_name(units_df):
    """
    Enrich the units_df with champion name
    """
    units_df['Name'] = units_df.apply(lambda row: str(row.Id[5:]), axis=1)
    return units_df


def build_unit_item_hashtable(list_of_unit):
    """
    Build item hash table
    Arguments:
        list_of_unit(list): list of unit data in dict
    REturns:
        item_hash(Dict): item in hashtable
            key(String): id of item,
            value(Dict): {
                count
                sum_placement
            }
    """
    item_hash = {}
    for unit in list_of_unit:
        # 99 is a thief guntlet that create 2 item randomly
        if 99 in unit['items']:
            if 99 not in item_hash.keys():
                item_hash[99] = {
                    'Id': 99,
                    'Count': 1,
                    'Sum_Placement': unit['placement'],
                    'Placement_List': [unit['placement']]
                }
            else:
                item_hash[99]['Count'] += 1
                item_hash[99]['Sum_Placement'] += unit['placement']
                item_hash[99]['Placement_List'].append(unit['placement'])
        else: 
            # Unit can holds up to 3 items
            for item in unit['items']:
                if item not in item_hash.keys():
                    item_hash[item] = {
                        'Id': item,
                        'Count': 1,
                        'Sum_Placement': unit['placement'],
                        'Placement_List': [unit['placement']]
                    }
                else:
                    item_hash[item]['Count'] += 1
                    item_hash[item]['Sum_Placement'] += unit['placement']
                    item_hash[item]['Placement_List'].append(unit['placement'])
            
    # Convert Sum(placement) to Avg(placement)
    for item_data in item_hash.values():
        item_data['Average_Placement'] = item_data['Sum_Placement']/item_data['Count']
    
    return item_hash


#--------------------------------version 2-----------------------------------------------

def build_champion_count_placement_df(champion_df):
    """
    Build dataframe for champion_count_placement plot
    """
    # Copy general_info columns from champion_df
    col_names = ['champion_name', 'champion_cost', 'image', 'count', 'count_percent', 'average_placement', 'average_tier']
    champion_count_placement_df = champion_df.loc[:, col_names].copy()
    # build zeros-df with index of champion_id and column of 'placement'
    placement_col_names = ['1', '2', '3', '4', '5', '6', '7', '8']
    empty_placement_df = pd.DataFrame(index=champion_df.index, columns=placement_col_names)
    empty_placement_df = empty_placement_df.fillna(0)
    # join those two
    champion_count_placement_df =  pd.concat([champion_count_placement_df, empty_placement_df], axis=1)
    # iterate through dataframe to update each placement
    for idx, champ_row in champion_df.iterrows():
        # Skip the case champion is not used
        if champ_row['all_placement'] == 0:
            pass
        else:
            for place in champ_row['all_placement']:
                champion_count_placement_df.loc[idx, str(place)] += 1
                
    return champion_count_placement_df    

    
def build_champion_count_tier_df(champion_df):
    """
    Build dataframe for champion_count_tier plot
    """
    # Copy general_info columns from champion_df
    col_names = ['champion_name', 'champion_cost', 'image', 'count', 'count_percent', 'average_placement', 'average_tier']
    champion_count_tier_df = champion_df.loc[:, col_names].copy()
    # build zeros-df with index of champion_id and column of 'tier_level'
    tier_col_names = ['tier_1', 'tier_2', 'tier_3']
    empty_tier_df = pd.DataFrame(index=champion_df.index, columns=tier_col_names)
    empty_tier_df = empty_tier_df.fillna(0)
    # join those two
    champion_count_tier_df =  pd.concat([champion_count_tier_df, empty_tier_df], axis=1)

    # iterate through dataframe to update each tier
    for idx, champ_row in champion_df.iterrows():
        # Skip the case champion is not used
        for t in tier_col_names:
            if champ_row[t] == 0:
                pass
            else:
                champion_count_tier_df.loc[idx, t] = len(champion_df.loc[idx, t])
                
    return champion_count_tier_df    


def build_champion_item_placement_df(champion_df):
    champion_item_placement_df = {}
    index = champion_df.index.values
    placement_list = ['1', '2', '3', '4', '5', '6', '7', '8']
    # Iterate through each champion (row of champion_df)
    for idx in index:
        # Create empty dataframe for each champion  row:placement col:items
        one_champ_item_placement_df = pd.DataFrame(index=placement_list, columns=ITEM_NAMES)
        one_champ_item_placement_df = one_champ_item_placement_df.fillna(0) # with 0s rather than NaNs
        
        champ_item_row = champion_df.loc[idx, ITEM_NAMES]
        for item_name in ITEM_NAMES:
            item_placement = champ_item_row[item_name]
            # Skip if item is not used
            if item_placement != 0:
                for p in item_placement:
                    one_champ_item_placement_df.loc[str(p), item_name] += 1
        # Build dictionary key=champion_id, value=champion_item_placement_df
        champion_item_placement_df[idx] = one_champ_item_placement_df

    
    return champion_item_placement_df