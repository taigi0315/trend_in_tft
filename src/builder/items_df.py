import pandas as pd
import json

def add_item_count_percent_on_df(item_df):
    """
    Enrich the dataFrame with item use count in percentage
    Argumnets:
        item_df(dataFrame)
    Returns:
        item_df(dataFrame): item_df enriched with 'Count(%)' column
    """
    total_item_cnt = sum(item_df['Count'])
    item_df['Count(%)'] = item_df.apply(lambda row: (row.Count/total_item_cnt) * 100, axis=1)

    return item_df


def build_items_df(item_in_unit_df):
    """
    Build a dataframe for item item usage analysis
    Arguments:
        item_in_unit_df(DataFrame): 'Item' Column in unit_df
    Returns:
        item_df(dataFrame): |name(String) | use_count(Int) | tiers(List) | items(List)|
    """  

    item_cnt = {}
    for row in item_in_unit_df:
        for item, cnt in row.items():
            if item not in item_cnt.keys():
                item_cnt[item] = cnt
            else:
                item_cnt[item] += cnt
    
    # Load item_id and item_name dict
    with open('builder/config/set3/items.json') as f:
        item_id_name = json.load(f)

    # Add item name to df
    for _id, cnt in item_cnt.items():
        for item in item_id_name:
            if str(item['id']) == str(_id):
                item['count'] = cnt
                break
    
    items_df = pd.DataFrame(item_id_name, columns=['id', 'name', 'count'])
    items_df.columns = ['Id', 'Name', 'Count']
    items_df = add_item_count_percent_on_df(items_df)
    
    return items_df
