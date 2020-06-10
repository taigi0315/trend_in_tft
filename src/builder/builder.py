import json
import os
from collections import Counter

import numpy as np
import pandas as pd

from .helper import (CHAMPION_COSTS, CHAMPION_IDS, CHAMPION_NAMES, ITEM_DATA,
                     ITEM_NAMES, TRAIT_NAMES, find_item_name)
from .items_df import (add_item_count_percent_on_df, add_item_image_on_df,
                       update_item_hashtable)
from .traits_df import build_traits_df
from .units_df import (add_average_num_item_on_units_df,
                       add_average_tier_on_units_df, add_champion_image_on_df,
                       add_unit_count_percent_on_df,
                       build_champion_count_placement_df,
                       build_champion_count_tier_df,
                       build_champion_item_placement_df, build_unit_hashtable,
                       build_unit_item_hashtable, convert_champion_id_to_name,
                       convert_traits, get_champion_cost,
                       get_units_in_multi_match)


def calculate_average_tier(tier_1, tier_2, tier_3, count):
    """
    Calculate average tier for each row
    Return .00 precision value
    """
    if count == 0:
        return 0

    sum_of_tier = 0
    if tier_1 != 0:
        sum_of_tier += len(tier_1)
    if tier_2 != 0:
        sum_of_tier += 2*len(tier_2)
    if tier_3 != 0:
        sum_of_tier += 2*len(tier_3)
    return round(float(sum_of_tier / count), 2)


def calculate_average_number_item(champion_df):
    """
    Returns:
        column with average number of item in champion
    """
    item_df = champion_df.loc[ :, ITEM_NAMES]
    item_df = convert_list_df_to_count(item_df)

    return item_df.sum(axis=1)/champion_df['count']


def convert_list_df_to_count(df):
    """
    Convert cell with list of placement(list) to count(int)
    """
    converted_df = df.copy()
    cols = converted_df.columns
    index = converted_df.index.values
    for c in cols:
        for i in index:
            if df.loc[i, c] != 0:
                converted_df.loc[i, c] = len(df.loc[i, c])

    return converted_df

class TFTDataBuilder:
    """
    Builder class creates and stores DataFrame
    """
    def __init__(self, file_name_prefix, match_data, save=True):
        self.file_name_prefix = file_name_prefix
        self.save = save
        self.match_data = match_data

    def build_items_dataframe(self, save=False):
        """
        Build a dataframe for item usage analysis
        Arguments:
            match_data(DataFrame): list of match data(Dict)
        Returns:
            item_df(dataFrame): |Id(String) | Name(String) | Count(Int) | Average_Placement(Float) | Image(String)|
        """
        
        item_hashtable = {}
        for match in self.match_data:
            players = match['match']['info']['participants']
            for player in players:
                player_placement = player['placement']
                for unit in player['units']:
                        item_hashtable = update_item_hashtable(item_hashtable, unit['items'], player_placement)    
        

        items_df = pd.DataFrame(item_hashtable.values(), columns=['Id', 'Count', 'Sum_Placement', 'Placement_List'])
        items_df['Placements'] = items_df.apply(lambda row: dict(Counter(row.Placement_List)), axis=1)
        items_df['Name'] = items_df.apply(lambda row: find_item_name(ITEM_ID_NAME_LIST, row.Id), axis=1)
        items_df['Average_Placement'] = items_df.apply(lambda row: (row.Sum_Placement / row.Count), axis=1)
        items_df = add_item_image_on_df(items_df)
        items_df = add_item_count_percent_on_df(items_df)
        
        self.items_df = items_df
        
        if save:
            self.items_df.to_csv(f'experiments/dataframe/items/items_df_{self.region}_{self.start_date}_{self.end_date}.csv')

#---------------------------------------------------------------------------------------Version 2
        
    def build_champion_dataframe(self):
        """
        Champion Dataframe will be used to analyze relationship between 
        "How the champion is used" and "Placement of the player"
        """
        df_columns = ['champion_name', 'champion_cost', 'image', 'count', 'all_placement']
        # Add tiers to columns
        df_columns += ['tier_1', 'tier_2', 'tier_3']
        # Add items to columns
        df_columns += ITEM_NAMES
        #  Add traits to columns
        df_columns += TRAIT_NAMES
        # Create empty dataframe
        champion_df = pd.DataFrame(index=CHAMPION_IDS, columns=df_columns)
        champion_df = champion_df.fillna(0) # with 0s rather than NaNs
        
        
        # %This trick is required to store list data in dataframe%
        object_dtype_cols = ['all_placement', 'tier_1', 'tier_2', 'tier_3', ITEM_NAMES, TRAIT_NAMES]
        for col in object_dtype_cols:
            champion_df[col] = champion_df[col].astype(object)

        # Update champion name column
        champion_df['champion_name'] = CHAMPION_NAMES
        # Update champion cost column
        champion_df['champion_cost'] = CHAMPION_COSTS
        # Update champion image column
        champion_df['image'] = champion_df.apply(lambda row: f"../../../assets/TFT_set_data/set3/champions/{str(row['champion_name']).lower()}.png", axis=1)

        # Get all unit data from all player in all matches
        units_in_matches = get_units_in_multi_match(self.match_data)
        for unit in units_in_matches:
            # unit data
            placement = unit['placement']
            items = [find_item_name(item) for item in unit['items']]

            # Update champion-count
            champion_df.at[unit['character_id'], 'count'] += 1
            # Update champin-placement
            if champion_df.at[unit['character_id'], 'all_placement'] == 0:
                champion_df.at[unit['character_id'], 'all_placement'] = [placement]
            else:
                # champion_df.at[unit['character_id'], 'all_placement'] =[champion_df.at[unit['character_id'], 'all_placement'], unit['placement']]
                champion_df.at[unit['character_id'], 'all_placement'].append(placement)
            # Update champion-tier
            tier_column = 'tier_' + str(unit['tier'])
            if champion_df.at[unit['character_id'], tier_column] == 0:
                champion_df.at[unit['character_id'], tier_column] = [placement]
            else:
                champion_df.at[unit['character_id'], tier_column].append(placement)
            # Update champion-trait data
            for trait in unit['traits']:
                if champion_df.at[unit['character_id'], trait] == 0:
                    champion_df.at[unit['character_id'], trait] = [placement]
                else:
                    champion_df.at[unit['character_id'], trait].append(placement)
            # Update champion-item data
            for item in items:
                if champion_df.at[unit['character_id'], item] == 0:
                    champion_df.at[unit['character_id'], item] = [placement]
                else:
                    champion_df.at[unit['character_id'], item].append(placement)
        # Calculate champion-count_percent
        champion_df['count_percent'] = champion_df.apply(lambda row: round(float(row['count'] / len(units_in_matches) * 100), 2), axis=1)
        # Calculate champion-average_placement      
        champion_df['average_placement'] = champion_df.apply(lambda row: 0 if row['all_placement'] == 0 else round(float(sum(row['all_placement']) / len(row['all_placement'])), 2), axis=1)
        # Calculate champion-average_tier
        champion_df['average_tier'] = champion_df.apply(lambda row: calculate_average_tier(row['tier_1'], row['tier_2'], row['tier_3'], row['count']), axis=1)
        calculate_average_number_item(champion_df)
        champion_df['average_number_item'] = calculate_average_number_item(champion_df)

        self.champion_df = champion_df
        self.champion_count_placement_df = build_champion_count_placement_df(champion_df)
        self.champion_count_tier_df = build_champion_count_tier_df(champion_df)
        
        build_champion_item_placement_df(champion_df, save=self.save, file_name_prefix=self.file_name_prefix)
        
        if self.save:
            champion_df.to_csv(f"assets/data/{self.file_name_prefix}/champion_df.csv")
            self.champion_count_placement_df.to_csv(f"assets/data/{self.file_name_prefix}/champion_count_placement_df.csv")
            self.champion_count_tier_df.to_csv(f"assets/data/{self.file_name_prefix}/champion_count_tier_df.csv")
