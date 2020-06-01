from .items_df import build_items_df
from .traits_df import build_traits_df
from .units_df import build_units_df
from .helper import split_match_data_win_lose

class TFTDataBuilder:
    def __init__(self, region='na1', match_data=None):
        self.region=region
        self.match_data = match_data
    
    def build_all_df(self):
        self.units_df = build_units_df(self.match_data)
        self.items_df = build_items_df(self.units_df['Item'])
        #self.traits_df = build_traits_df(self.match_data)
    
    def build_winner_loser_df(self):
        winner_match_data, loser_match_data = split_match_data_win_lose(self.match_data)

        # Build unit_df for winner & loser
        self.winner_units_df = build_units_df(winner_match_data)
        self.loser_units_df = build_units_df(loser_match_data)
        
        # Build item_df for winner & loser
        self.winner_items_df = build_items_df(self.winner_units_df['Item'])
        self.loser_items_df = build_items_df(self.loser_units_df['Item'])

        # Build trait_df for winner & loser
        self.winner_traits_df = build_traits_df(winner_match_data)
        self.loser_traits_df = build_traits_df(loser_match_data) 

    
    
