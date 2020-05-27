import pandas as pd

def get_units_in_single_match(single_match_data):
    """
    Extract all unit data from single match data
    Arguments: 
        single_match_data(Dict): response from Riot API match details
    Returns:
        units(List): All units used in match
    """
    players = single_match_data['info']['participants']
    units = []
    for p in players:
        units += p['units']

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

def get_units_from_player_list(player_list):
    """
    Extract all unit data from list of player data
    Arguments:
        player_list(List): list of player data(dict)
    Returns:
        unit_list(List): list of unit data
    """
    units = []
    for player in player_list:
        units += player['units']
    
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
        unit_name = unit['character_id'][5:]
        if unit_name not in unit_hash.keys():
             unit_hash[unit_name] = [unit]
        else:
             unit_hash[unit_name].append(unit)
    
    return unit_hash

def build_hashtable_from_list(lst):
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


def build_unit_use_count_tier_item_df(unit_hashtable):
    '''
    Build dataframe for unit useage analysis
    Arguments:
        unit_hashtable(Dict): result from unit_dict_in_multi_match function.
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
    unit_use_count_tier_item = []
    for champ_name, list_of_units in unit_hashtable.items():
        champ_tier_list = []
        champ_item_list = []
        for unit in list_of_units:
            champ_tier_list.append(unit['tier'])
            items = unit['items']
            if 99 in items:
                champ_item_list += [99] # 99: Thief's Gloves: generates 2 random item
            else:
                champ_item_list += unit['items']
        
        champ_tier_table = build_hashtable_from_list(champ_tier_list)
        champ_item_table = build_hashtable_from_list(champ_item_list)
        unit_use_count_tier_item.append([champ_name, len(list_of_units), champ_tier_table, champ_item_table])
    
    
    unit_use_count_tier_item_df = pd.DataFrame(unit_use_count_tier_item, columns = ['Champion', 'Count', 'Tier', 'Item']) 
    return unit_use_count_tier_item_df

    # unit_use_count_tier_item_df = build_unit_use_count_tier_item_df(unit_hashtable)

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

# sample_data_w_avg_tier = add_average_tier_on_unit_df(unit_use_count_tier_item_df)

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
            
    df['Average_Num_Item'] = df.apply(lambda row: calculate_average_num_item(row.Count, row.Item), axis=1)
    return df

# sample_data_w_avg_item = add_average_num_item_on_unit_df(unit_use_count_tier_item_df)
