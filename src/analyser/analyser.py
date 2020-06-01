from .units_plot import plot_units_df
from .helper import split_units_df_by_cost
import pandas as pd


class TFTDataAnalyser:
    def __init__(self, db, region='na'):
        self.db = db

    def get_match_data_from_db(self, region='na1'):
        regx = "^" + region.upper()
        match_data = list(self.db.collection.find( {'_id': {'$regex':regx} }))
        # match_data = match_data[:10]
        # test_data_ids = ["NA1_3436887139", "NA1_3436855922"]
        # match_data = list(self.db.collection.find({'_id': {'$in': test_data_ids }}))
        self.match_data = match_data

    def plot_all_units_graph(self, units_df):
        # Plot units_df
        plot_units_df(units_df, title='All_Units_Plot')
        
        # Plot units_df by cost of units
        units_df_by_cost = split_units_df_by_cost(set_name='set3', units_df=units_df)
        for key, df_data in units_df_by_cost.items():
            cost_unit_df = pd.DataFrame(df_data, columns = units_df.columns)
            plot_units_df(title=key, units_df=cost_unit_df)




