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
    
def get_unit_hashtable(unit_list):
    """
    Build unit hashtable
    Arguments:
        unit_list(List): list of all units used in game
    Returns:
        unit_hash(Dict): 
            Key(String): name of units
            Value(List): detail information of each units
    """
    unit_hash = {}

    for unit in unit_list:
        unit_name = unit['character_id']
        if unit_name not in unit_hash.keys():
             unit_hash[unit_name] = [unit]
        else:
             unit_hash[unit_name].append(unit)
    
    return unit_hash

def build_count_hashtable_from_list(lst):
    """
    Create hashtable from list
    Arguments:
        input(List): elements to build hashtable in list format
    Returns:
        (Dict): hashtable of items
            key: name of element
            val: count of element
    """
    table = {}
    for e in lst:
        if e not in table.keys():
            table[e] = 1
        else:
            table[e] += 1

    return table


def add_average_tier_on_unit_df(df):
    """
    Enrich the dataFrame with average tier of units column
    Argumnets:
        df(dataFrame): result dataframe from 'build_unit_use_count_tier_item_df' function
    Returns:
        df(dataFrame): df enriched with Average_Tier column
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
            
    df['Average_Tier'] = df.apply(lambda row: calculate_average_tier(row.Count, row.Tier), axis=1)
    
    return df


def add_average_num_item_on_unit_df(df):
    """
    Enrich the dataFrame with average number of item column
    Argumnets:
        df(dataFrame): result dataframe from 'build_unit_use_count_tier_item_df' function
    Returns:
        df(dataFrame): df enriched with Average_Num_Item column
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
            sum += int(val)

        return sum/cnt
            
    df['Average_#_Item'] = df.apply(lambda row: calculate_average_num_item(row.Count, row.Item), axis=1)
    return df


def add_unit_avg_placement_on_df(df):
    """
    Enrich the dataFrame with unit average placement
    Average_Placement = Sum(unit placement) / Count
    Argumnets:
        df(dataFrame): result dataframe from 'build_unit_use_count_tier_item_df' function
    Returns:
        df(dataFrame): df enriched with Average_Placement column
    """

    total_unit_count = sum(df['Count'])
    df['Count(%)'] = df.apply(lambda row: (row.Count/total_unit_count)*100, axis=1)


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


def build_unit_df(db, region='na1'):
    '''
    Build dataframe for unit useage analysis
    Arguments:
        db: Databse connection
        region(String)
    Returns:
        unit_use_count_tier_item_df(dataFrame): |name(String) | use_count(Int) | tiers(List) | items(List)|
    
    sample single unit data :
    { 
        'character_id': 'TFT3_Fiora',
        'items': [59],
        'name': '',
        'rarity': 0,
        'tier': 1
    }
    '''

    regx = "^" + region.upper()
    match_data = list(db.collection.find( {'_id': {'$regex':regx} }))
    units_in_matches = get_units_in_multi_match(match_data)
    units_in_matches_hash = get_unit_hashtable(units_in_matches)
    
    unit_df_data = []
    for champ_name, list_of_units in units_in_matches_hash.items():
        champ_tiers_list = []
        champ_items_list = []
        champ_traits_list = []
        sum_champ_placement = 0
        for unit in list_of_units:
            # Champion tier
            champ_tiers_list.append(unit['tier'])
            # Placements with the champ
            sum_champ_placement += unit['placement']
            # Items used with the champ
            if 99 in unit['items']:
                champ_items_list += [99] # 99: Thief's Gloves: generates 2 random item
            else:
                champ_items_list += unit['items']
            # Traits used with the champ
            champ_traits_list += convert_traits(unit['traits'])
            
        champ_tiers = Counter(champ_tiers_list)
        champ_traits = Counter(champ_traits_list)
        champ_items = Counter(champ_items_list)
        average_placement = sum_champ_placement/len(list_of_units)

        unit_df_data.append([champ_name, len(list_of_units), champ_tiers, champ_traits, champ_items, average_placement])
    
    
    unit_df = pd.DataFrame(unit_df_data, columns = ['Champion', 'Count', 'Tier', 'Traits', 'Item', 'Average_Placement']) 
    unit_df = add_average_tier_on_unit_df(unit_df)
    unit_df = add_average_num_item_on_unit_df(unit_df)

    return unit_df
