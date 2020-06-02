from .items_df import build_items_df
from .traits_df import build_traits_df
from .units_df import build_units_df
from .helper import split_match_data_win_lose

class TFTDataBuilder:
    """
    Builder class creates and stores DataFrame
    """
    def __init__(self, start_date, end_date, region='na1', match_data=None):
        self.region=region
        self.match_data = match_data
        self.start_date = start_date
        self.end_date = end_date
    
    def build_units_df(self, save=False):
        self.units_df = build_units_df(self.match_data)
        
        if save:
            self.units_df.to_csv(f'experiments/dataframe/units/units_df_{self.region}_{self.start_date}_{self.end_date}.csv')

    def build_items_df(self, save=False):
        self.items_df = build_items_df(self.units_df['Item'])
        
        if save:
            self.items_df.to_csv(f'experiments/dataframe/items/items_df_{self.region}_{self.start_date}_{self.end_date}.csv')
    
    def build_winner_loser_df(self, save=False):
        winner_match_data, loser_match_data = split_match_data_win_lose(self.match_data)
        
        # Build unit_df for winner & loser
        self.winner_units_df = build_units_df(winner_match_data)
        self.loser_units_df = build_units_df(loser_match_data)
        
        if save:
            self.winner_units_df.to_csv(f'experiments/dataframe/win_and_lose/units/winner_units_df_{self.region}_{self.start_date}_{self.end_date}.csv')
            self.loser_units_df.to_csv(f'experiments/dataframe/win_and_lose/units/loser_units_df_{self.region}_{self.start_date}_{self.end_date}.csv')

        # Build item_df for winner & loser
        self.winner_items_df = build_items_df(self.winner_units_df['Item'])
        self.loser_items_df = build_items_df(self.loser_units_df['Item'])

        if save:
            self.winner_items_df.to_csv(f'experiments/dataframe/win_and_lose/items/winner_items_df_{self.region}_{self.start_date}_{self.end_date}.csv')
            self.loser_items_df.to_csv(f'experiments/dataframe/win_and_lose/items/loser_items_df_{self.region}_{self.start_date}_{self.end_date}.csv')

        # Build trait_df for winner & loser
        self.winner_traits_df = build_traits_df(winner_match_data)
        self.loser_traits_df = build_traits_df(loser_match_data)

        if save:
            self.winner_traits_df.to_csv(f'experiments/dataframe/win_and_lose/traits/winner_traits_df_{self.region}_{self.start_date}_{self.end_date}.csv')
            self.loser_traits_df.to_csv(f'experiments/dataframe/win_and_lose/traits/loser_traits_df_{self.region}_{self.start_date}_{self.end_date}.csv')


    
    
