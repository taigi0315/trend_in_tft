import math
import json

with open('assets/TFT_set_data/set3/items.json') as f:
    ITEM_DATA = json.load(f)
    ITEM_NAMES = [item['name'] for item in ITEM_DATA]
    ITEM_IDS = [item['id'] for item in ITEM_DATA]

with open('assets/TFT_set_data/set3/items.json') as f:
    ITEM_ID_NAME_LIST = json.load(f)


def get_count_axis_ticker(max_count):
    max_num = int(math.ceil(max_count / 50.0)) * 50
    interval = int(max_num / 5)
    return list(range(0, max_num+interval, interval))


def split_df_by_champion_cost(set_name, df):
    """
    Based on champions_info, split unit_df by cos.
    Arguments:
        champions_info(List): list of champion informations from API doc
        unit_df(DataFrame)
        
    Returns:
        unit_df_by_cost(Dict): hashed unit_df by cost of unit
    """

    set_file_path = f'assets/TFT_set_data/{set_name}/champions.json'
    with open(set_file_path) as f:
        champions_info = json.load(f)

    df_by_champion_cost = {
        "cost_1_champions": [],
        "cost_2_champions": [],
        "cost_3_champions": [],
        "cost_4_champions": [],
        "cost_5_champions": [],
    }
    
    for index, row in df.iterrows():
        champ_cost = next(champ['cost'] for champ in champions_info if champ['championId'] == index)
        hash_key = f"cost_{champ_cost}_champions"
        df_by_champion_cost[hash_key].append(dict(row))
        
    return df_by_champion_cost


def find_item_name(item_id):
     for item in ITEM_ID_NAME_LIST:
            if str(item['id']) == str(item_id):
                return item['name']


