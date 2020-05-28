
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
