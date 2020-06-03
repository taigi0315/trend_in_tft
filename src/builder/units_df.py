import pandas as pd
from collections import Counter


def get_units_in_single_match(single_match_data):
    """
    Extract all unit data from single match data
    Arguments: 
        single_match_data(Dict): response from Riot API match details
    Returns:
        units(List): All units used in match
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
            unit['traits'] = p['traits']

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


def add_average_tier_on_unit_df(unit_df):
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


def add_average_num_item_on_unit_df(unit_df):
    """
    Enrich the dataFrame with average number of item column
    Argumnets:
        unit_df(dataFrame): result dataframe from 'build_unit_use_count_tier_item_df' function
    Returns:
        unit_df(dataFrame): unit_df enriched with Average_Num_Item column
    """
    def calculate_average_num_item(cnt, item_hash):
        """
        Calculate average of tier
        Arguments:
            item_dict(Dict)
        Returns:
            average_num_item(Float)
        """
        sum = 0
        for val in item_hash.values():
            sum += int(val['count'])

        return sum/cnt
            
    unit_df['Average_#_Item'] = unit_df.apply(lambda row: calculate_average_num_item(row.Count, row.Item), axis=1)
    return unit_df


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
    
    units_df['Image'] = units_df.apply(lambda row: f"../../../assets/set3/champions/{str(row.Champion_Name).lower()}.png", axis=1)
    return units_df


def convert_champion_id_to_name(units_df):
    """
    Enrich the units_df with champion name
    """
    units_df['Champion_Name'] = units_df.apply(lambda row: str(row.Champion_Id[5:]), axis=1)
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
        # Items used with the champ
        if 99 in unit['items']:
            if 99 not in item_hash.keys():
                item_hash[99] = {
                    'count': 1,
                    'sum_placement': unit['placement']
                }
            else:
                item_hash[99]['count'] += 1
                item_hash[99]['sum_placement'] += unit['placement']
        else: 
            # Unit can holds up to 3 items
            for item in unit['items']:
                if item not in item_hash.keys():
                    item_hash[item] = {
                    'count': 1,
                    'sum_placement': unit['placement']
                }
                else:
                    item_hash[item]['count'] += 1
                    item_hash[item]['sum_placement'] += unit['placement']
            
        # Convert Sum(placement) to Avg(placement)
        for item_data in item_hash.values():
            item_data['average_placement'] = item_data['sum_placement']/item_data['count']
    
    return item_hash


def build_units_df(match_data):
    '''
    Build a dataframe for unit useage analysis
    Arguments:
        match_data(List): list of match data(Dict)
    Returns:
        unit_df(dataFrame): |name(String)|Count(Int)|tiers(List)|items(List)|Traits(Dict)|Average_Placement(Float)|Average_Tier(Float)|Average_#_Item(Float)|Count(%)(Float)|
    
    sample single unit data :
    '''

    units_list = get_units_in_multi_match(match_data)
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
        average_placement = sum(placement_list) / len(list_of_unit)

        units_df_data.append([champ_name, len(list_of_unit), champ_tiers, champ_traits, item_hash, champ_placements, average_placement])
    
    
    units_df = pd.DataFrame(units_df_data, columns = ['Champion_Id', 'Count', 'Tier', 'Traits', 'Item', 'Placement_List', 'Average_Placement']) 
    units_df = add_average_tier_on_unit_df(units_df)
    units_df = add_average_num_item_on_unit_df(units_df)
    units_df = add_unit_count_percent_on_df(units_df)
    units_df = convert_champion_id_to_name(units_df)
    units_df = add_champion_image_on_df(units_df)

    return units_df
