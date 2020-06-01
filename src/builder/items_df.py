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


def build_items_df(units_df_item_col):
    """
    Build a dataframe for item item usage analysis
    Arguments:
        units_df_item_col(DataFrame): Item hash table
        {item_name:{
            count: item used count,
            average_placement: average of placements with the item
        }}
    Returns:
        item_df(dataFrame): |name(String) | use_count(Int) | tiers(List) | items(List)|
    """  

    item_df_hash = {}
    
    for unit_item_hash in units_df_item_col:
        for item_id, item_data in unit_item_hash.items():
            if item_id not in item_df_hash.keys():
                item_df_hash[item_id] = {
                    'count': item_data['count'],
                    'average_placement': item_data['average_placement']
                }
            else:
                item_df_hash[item_id]['count'] += 1
                item_df_hash[item_id]['average_placement'] += item_data['average_placement']
    
    # Calculate average placement
    for item_data in item_df_hash.values():
        item_data['average_placement'] = item_data['average_placement'] / item_data['count']

    # Load item_id and item_name dict
    with open('assets/set3/items.json') as f:
        item_id_name = json.load(f)
    
    # Build data to build DataFrame
    for item_id, item_data in item_df_hash.items():
        for item in item_id_name:
            if str(item['id']) == str(item_id):
                item_data['id'] = item_id
                item_data['name'] = item['name']
                break
    
    items_df = pd.DataFrame(item_df_hash.values(), columns=['count', 'average_placement', 'id', 'name'])
    items_df.columns = ['Count', 'Average_placement', 'Id', 'Name']
    items_df = add_item_count_percent_on_df(items_df)
    
    return items_df
