import math
import json

def get_count_axis_ticker(max_count):
    max_num = int(math.ceil(max_count / 50.0)) * 50
    interval = int(max_num / 5)
    return list(range(0, max_num+interval, interval))


def split_units_df_by_cost(set_name, units_df):
    """
    Based on champions_info, split unit_df by cos.
    Arguments:
        champions_info(List): list of champion informations from API doc
        unit_df(DataFrame)
        
    Returns:
        unit_df_by_cost(Dict): hashed unit_df by cost of unit
    """

    set_file_path = f'assets/{set_name}/champions.json'
    with open(set_file_path) as f:
        champions_info = json.load(f)

    units_df_by_cost = {
        "cost_1_champions": [],
        "cost_2_champions": [],
        "cost_3_champions": [],
        "cost_4_champions": [],
        "cost_5_champions": [],
    }
    
    for index, row in units_df.iterrows():
        champ_cost = next(champ['cost'] for champ in champions_info if champ['championId'] == row['Champion_Id'])
        hash_key = f"cost_{champ_cost}_champions"
        units_df_by_cost[hash_key].append(dict(row))
        
    return units_df_by_cost