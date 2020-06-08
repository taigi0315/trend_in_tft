import json
import os
from collections import Counter

import numpy as np
import pandas as pd

from .helper import split_match_data_win_lose, find_item_name
from .items_df import update_item_hashtable, add_item_image_on_df, add_item_count_percent_on_df
from .traits_df import build_traits_df
from .units_df import (add_average_num_item_on_units_df,
                       add_average_tier_on_units_df, add_champion_image_on_df,
                       add_unit_count_percent_on_df, build_unit_hashtable,
                       build_unit_item_hashtable, convert_champion_id_to_name,
                       convert_traits, get_champion_cost,
                       get_units_in_multi_match)

with open('assets/set3/items.json') as f:
    ITEM_DATA = json.load(f)
    ITEM_NAMES = [item['name'] for item in ITEM_DATA]
    
with open('assets/set3/champions.json') as f:
    CHAMPION_DATA = json.load(f)
    CHAMPION_IDS = [champ['championId'] for champ in CHAMPION_DATA]
    CHAMPION_NAMES = [champ['name'] for champ in CHAMPION_DATA]
    CHAMPION_COSTS = [champ['cost'] for champ in CHAMPION_DATA]

with open('assets/set3/traits.json') as f:
    TRAIT_DATA = json.load(f)
    # Build traits names ex) Blaster_1, Blaster_2
    TRAIT_NAMES = []
    for trait in TRAIT_DATA:
        for i in range(len(trait['sets'])):
            trait_level = trait['key'] + '_' + str(i+1)
            TRAIT_NAMES.append(trait_level)

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

class TFTDataBuilder:
    """
    Builder class creates and stores DataFrame
    """
    def __init__(self, start_date, end_date, region='na1', match_data=None):
        self.region=region
        self.match_data = match_data
        self.start_date = start_date
        self.end_date = end_date
    

    def build_units_dataframe(self, save=False):
        '''
        Build a dataframe for unit useage analysis
        Arguments:
            match_data(List): list of match data(Dict)
        Returns:
            unit_df(dataFrame): |Name(String)|Id(String)|Count(Int)|tiers(List)|items(List)|Traits(Dict)|Average_Placement(Float)|Average_Tier(Float)|Average_#_Item(Float)|Count(%)(Float)|
        
        sample single unit data :
        '''

        units_list = get_units_in_multi_match(self.match_data)
        units_hash = build_unit_hashtable(units_list)
        
        units_df_data = []
        for champ_name, list_of_unit in units_hash.items():
            tiers_list = []
            traits_list = []
            placement_list = []
            
            for unit in list_of_unit:
                # Champion tier
                tiers_list.append(unit['tier'])
                # Placements with the champ
                placement_list.append(unit['placement'])
                # Traits used with the champ
                traits_list += convert_traits(unit['traits'])

            item_hash = build_unit_item_hashtable(list_of_unit)

            champ_tiers = dict(Counter(tiers_list))
            champ_traits = dict(Counter(traits_list))
            champ_placements = dict(Counter(placement_list))
            
            # Fill up missing cases ex) no specific placement with the unit
            for p in range(1, 9):
                if p not in champ_placements.keys():
                    champ_placements[p] = 0
            # Fill up missing cases ex) no specific tier with the unit
            for p in range(1, 4):
                if p not in champ_tiers.keys():
                    champ_tiers[p] = 0
                
            average_placement = sum(placement_list) / len(list_of_unit)
            champ_items = item_hash
            units_df_data.append([champ_name, len(list_of_unit), champ_tiers, champ_traits, champ_items, champ_placements, average_placement])
        
        
        units_df = pd.DataFrame(units_df_data, columns = ['Id', 'Count', 'Tier', 'Traits', 'Item', 'Placement', 'Average_Placement']) 
        units_df = add_average_tier_on_units_df(units_df)
        units_df = add_average_num_item_on_units_df(units_df)
        units_df = add_unit_count_percent_on_df(units_df)
        units_df = convert_champion_id_to_name(units_df)
        units_df = add_champion_image_on_df(units_df)
        units_df['Cost'] = units_df.apply(lambda row: get_champion_cost(row.Id), axis=1)

        self.units_df = units_df
        
        if save:
            self.units_df.to_csv(f'experiments/dataframe/units/units_df_{self.region}_{self.start_date}_{self.end_date}.csv')

        

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
        
        
    
    def build_units_item_placement_dataframe(self, save=False):       
        unit_list = get_units_in_multi_match(self.match_data)
        set_name = 'set3'

        set_champion_file_path = f'assets/{set_name}/champions.json'
        with open(set_champion_file_path) as f:
            set_champions_info = json.load(f)

        set_item_file_path = f'assets/{set_name}/items.json'
        with open(set_item_file_path) as f:
            set_items_info = json.load(f)

        # Get all champion id to use as index
        champion_id_list = []
        for champ in set_champions_info:
            champion_id_list.append(champ['championId'])
        # Get all item id to use as index
        item_id_list = []
        item_name_list = []
        for item in set_items_info:
            item_id_list.append(item['id'])
            item_name_list.append(item['name'])
        
        units_item_placement_df = {}
        # Iterate through unit in all units in all matches
        for unit in unit_list:
            champ_id = unit['character_id']
            placement = unit['placement']
            
            # Create empty dict if champion is not in yet
            if champ_id not in units_item_placement_df.keys():
                # Create empty dataframe with size of placement * #item
                empty_df = pd.DataFrame(index=list(range(1, 9)), columns=item_id_list)
                empty_df = empty_df.fillna(0) # with 0s rather than NaNs
                # Add item name row
                empty_df.loc['Item_Name'] = item_name_list
                units_item_placement_df[champ_id] = empty_df
            
            # Fill up the empty dataframe
            for i in unit['items']:
                units_item_placement_df[champ_id].loc[placement][i] += 1
            
            # Add Average Placement row
            units_item_placement_df[champ_id].loc['Average_Placement'] = units_item_placement_df[champ_id].sum(axis=0)

            
        

        self.units_item_placement_df = units_item_placement_df
        
        if save:    
            for champ_id, table in units_item_placement_df.items():
                if not os.path.exists('experiments/dataframe/units/units_item_placement_dataframe'):
                    os.makedirs('experiments/dataframe/units/units_item_placement_dataframe')
                
                df = pd.DataFrame(table, index=[list(range(1, 9)), 'Item_Name', 'Average_Placement'], columns=item_id_list)
                df.to_csv(f'experiments/dataframe/units/units_item_placement_dataframe/{champ_id}_item_placement.csv')

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
        champion_df['image'] = champion_df.apply(lambda row: f"../../../assets/set3/champions/{str(row['champion_name']).lower()}.png", axis=1)

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
        
        champion_df.to_csv('TEST_champion_df.csv')
             

