import json
import os
from collections import Counter

import numpy as np
import pandas as pd

from .helper import split_match_data_win_lose
from .items_df import update_item_hashtable, add_item_image_on_df, add_item_count_percent_on_df, find_item_name
from .traits_df import build_traits_df
from .units_df import (add_average_num_item_on_units_df,
                       add_average_tier_on_units_df, add_champion_image_on_df,
                       add_unit_count_percent_on_df, build_unit_hashtable,
                       build_unit_item_hashtable, convert_champion_id_to_name,
                       convert_traits, get_champion_cost,
                       get_units_in_multi_match)


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
        
        with open('assets/set3/items.json') as f:
            item_id_name_list = json.load(f)
        
        
        items_df = pd.DataFrame(item_hashtable.values(), columns=['Id', 'Count', 'Sum_Placement', 'Placement_List'])
        items_df['Placements'] = items_df.apply(lambda row: dict(Counter(row.Placement_List)), axis=1)
        items_df['Name'] = items_df.apply(lambda row: find_item_name(item_id_name_list, row.Id), axis=1)
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
        for item in set_items_info:
            item_id_list.append(item['id'])

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
                units_item_placement_df[champ_id] = empty_df
            
            # Fill up the empty dataframe
            for i in unit['items']:
                units_item_placement_df[champ_id].loc[placement][i] += 1
        
        self.units_item_placement_df = units_item_placement_df
        
        if save:    
            for champ_id, table in units_item_placement_df.items():
                if not os.path.exists('experiments/dataframe/units/units_item_placement_dataframe'):
                    os.makedirs('experiments/dataframe/units/units_item_placement_dataframe')
                
                df = pd.DataFrame(table, index=list(range(1, 9)), columns=item_id_list)
                df.to_csv(f'experiments/dataframe/units/units_item_placement_dataframe/{champ_id}_item_placement.csv')

    
    # def build_winner_loser_dataframe(self, save=False):
    #     self.winner_match_data, self.loser_match_data = split_match_data_win_lose(self.match_data)
    #     # Build unit_df for winner & loser
    #     self.winner_units_df = build_units_df(self.winner_match_data)
    #     self.loser_units_df = build_units_df(self.loser_match_data)
        
    #     if save:
    #         self.winner_units_df.to_csv(f'experiments/dataframe/win_and_lose/units/winner_units_df_{self.region}_{self.start_date}_{self.end_date}.csv')
    #         self.loser_units_df.to_csv(f'experiments/dataframe/win_and_lose/units/loser_units_df_{self.region}_{self.start_date}_{self.end_date}.csv')

    #     # Build item_df for winner & loser
    #     self.winner_items_df = build_items_df(self.winner_match_data)
    #     self.loser_items_df = build_items_df(self.loser_match_data)

    #     if save:
    #         self.winner_items_df.to_csv(f'experiments/dataframe/win_and_lose/items/winner_items_df_{self.region}_{self.start_date}_{self.end_date}.csv')
    #         self.loser_items_df.to_csv(f'experiments/dataframe/win_and_lose/items/loser_items_df_{self.region}_{self.start_date}_{self.end_date}.csv')

    #     # Build trait_df for winner & loser
    #     self.winner_traits_df = build_traits_df(self.winner_match_data)
    #     self.loser_traits_df = build_traits_df(self.loser_match_data)

    #     if save:
    #         self.winner_traits_df.to_csv(f'experiments/dataframe/win_and_lose/traits/winner_traits_df_{self.region}_{self.start_date}_{self.end_date}.csv')
    #         self.loser_traits_df.to_csv(f'experiments/dataframe/win_and_lose/traits/loser_traits_df_{self.region}_{self.start_date}_{self.end_date}.csv')
